"""Formatting checks, deliberately separate from scientific/administrative review."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PDF_TOOLS = ('pdfinfo', 'pdffonts', 'pdftotext', 'pdftohtml')
PLACEHOLDERS = ('[Project title]', '[Projekttitel]', '[First Last]', '[City]',
                '[Ort]', '[Vorname Nachname]', '[Applicant name]', '[Text]')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(command):
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                            errors='replace', timeout=90)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout)[-2000:])
    return result.stdout

def strip_comments(text):
    return '\n'.join(re.split(r'(?<!\\)(?:\\\\)*%', line, maxsplit=1)[0]
                     for line in text.splitlines())

def normal(text):
    return re.sub(r'\s+', ' ', text).strip()

class Report:
    def __init__(self):
        self.items = []
    def add(self, name, status, detail):
        self.items.append(dict(check=name, status=status, detail=detail))
    def check(self, name, condition, good, bad):
        self.add(name, 'passed' if condition else 'failed', good if condition else bad)
    @property
    def failed(self):
        return any(x['status']=='failed' for x in self.items)
    def emit(self):
        for item in self.items:
            print(f"{item['status'].upper()}: {item['check']}: {item['detail']}")
        print('Formatting checks only. Review scientific content, approvals, figures and final layout separately.')
        return int(self.failed)

def check_trace(trace, profile, language, release, report):
    events=[line.split('|') for line in trace.splitlines() if line.strip()]
    def single(key):
        rows=[e[1:] for e in events if e[0]==key]
        return rows[0] if len(rows)==1 else []
    report.check('completed compilation',single('complete')==['yes'],
                 'Compilation trace is complete.','Missing or duplicate completion record.')
    report.check('form profile',single('profile')==[profile['id']],
                 profile['id'],'Unexpected or missing form profile.')
    report.check('language',single('language')==[language],language,'Language does not match the requested build.')
    report.check('build mode',not release or single('mode')==['submission'],
                 'Submission mode active.' if release else 'Draft checks selected.','Submission mode was not active.')
    limits=[str(profile['main_pages']),str(profile['supplement_pages'])]
    report.check('configured limits',single('limits')==limits,'17/8 profile limits retained.','Page limits were overridden.')
    required=profile['headings']
    by_number={h['number']:h for h in required+profile['optional_headings']}
    actual=[]
    legacy_valid=True
    region='before'
    boundaries=[]
    boundary_valid=True
    for event in events:
        if event[0]=='boundary':
            region=event[1]; boundaries.append(region)
        if event[0]=='heading':
            actual.append(event[1])
            h=next((h for h in required+profile['optional_headings'] if h['id']==event[1]),None)
            if not h or event[2:] != [h['number']]: legacy_valid=False
        elif event[0]=='legacy-heading':
            h=by_number.get(event[1])
            if not h or normal('|'.join(event[2:])) != normal(h[language]):
                legacy_valid=False
            actual.append(h['id'] if h else '?')
        else:
            continue
        h=next((h for h in required+profile['optional_headings'] if h['id']==actual[-1]),None)
        if h and region != ('main' if int(h['number'].split('.')[0])<=3 else 'supplement'):
            boundary_valid=False
    expected=[h['id'] for h in required]
    valid_sequences=[expected,expected+[profile['optional_headings'][0]['id']]]
    report.check('heading sequence',actual in valid_sequences and legacy_valid,
                 f'{len(actual)} effective headings in the required order.',
                 'Missing, duplicate, inactive, renamed or reordered heading. Compare the trace with the profile.')
    report.check('section boundary',boundaries==['main','supplement'] and boundary_valid,
                 'Sections 1–3 precede the supplement.','Incorrect main/supplement boundary.')
    ethics=[e[1] for e in events if e[0]=='ethics']
    completed_ethics=len(ethics)==1 and ethics[0] in ('yes','no')
    report.add('ethics declaration','passed' if completed_ethics else ('failed' if release else 'warning'),
               'One explicit yes/no selection recorded; substantive assessment is not checked.' if completed_ethics
               else 'Complete exactly one DFGEthicsStatement{yes} or {no} after assessment.')
    todos=sum(e[0]=='todo' for e in events)
    report.add('writing prompts','passed' if not todos else ('failed' if release else 'warning'),
               f'{todos} unresolved prompt(s).')
    counts=single('pages')
    valid_counts=len(counts)==2 and all(c.isdigit() for c in counts)
    pages=tuple(map(int,counts)) if valid_counts else (0,0)
    report.check('shipped pages',valid_counts and 1<=pages[0]<=17 and 1<=pages[1]<=8,
                 f'Main {pages[0]}/17; supplement {pages[1]}/8, including flushed floats.',
                 f'Invalid shipped-page counts: {pages}.')
    font=single('font')
    report.check('selected font',bool(font) and (not release or font==['Arial']),
                 ' / '.join(font),'Submission must resolve the configured body font to Arial.')
    return pages

def check_log(log, release, report):
    errors=[]
    for pattern,description in [
        (r"(?:Citation|Reference) .+ undefined", 'Undefined citation or reference'),
        (r'There were undefined references', 'Undefined references remain'),
        (r'Empty bibliography', 'Empty bibliography'),
        (r'Please \(re\)run Biber', 'Biber/rerun required'),
        (r'Missing character:', 'Missing character'),
        (r'Label\(s\) may have changed|Rerun to get|Please rerun LaTeX', 'Compilation did not converge'),
    ]:
        if re.search(pattern,log,re.I): errors.append(description)
    report.check('citations and reruns',not errors,'No unresolved citations, references or rerun requests.',
                 '; '.join(errors))
    boxes=len(re.findall(r'Overfull \\[hv]box',log))
    report.add('layout warnings','warning' if boxes else 'passed',
               f'{boxes} overfull box warning(s); inspect the build log and PDF.')

def check_inputs(manifest, source, pdf, release, report):
    if not manifest.is_file():
        report.add('source freshness','failed' if release else 'not checked',
                   'No build input manifest; use scripts/build.py for a reproducible checked build.')
        return
    try:
        data=json.loads(manifest.read_text(encoding='utf-8'))
        valid=data['pdf_sha256']==digest(pdf) and Path(data['source']).resolve()==source.resolve()
        for entry in data['inputs']:
            p=Path(entry['path'])
            valid=valid and p.is_file() and digest(p)==entry['sha256']
        report.check('source freshness',valid,'PDF and recorded inputs match the completed build.',
                     'PDF or an input changed after compilation. Rebuild.')
        unresolved=[]
        for entry in data['inputs']:
            p=Path(entry['path'])
            if p.suffix=='.tex':
                text=strip_comments(p.read_text(encoding='utf-8'))
                if any(token in text for token in PLACEHOLDERS) or re.search(r'\b(?:TODO|FIXME)\b',text):
                    unresolved.append(p.name)
        report.add('source placeholders','passed' if not unresolved else ('failed' if release else 'warning'),
                   'No known placeholder tokens.' if not unresolved else 'Complete placeholders in: '+', '.join(unresolved))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        report.add('source freshness','failed',str(exc))

def check_pdf(pdf, profile, language, release, pages, report):
    missing=[tool for tool in PDF_TOOLS if not shutil.which(tool)]
    if missing:
        report.add('PDF inspection','failed' if release else 'not checked','Missing tools: '+', '.join(missing))
        return
    info=dict(re.findall(r'^([^:\n]+):\s*(.*)$',run(['pdfinfo',str(pdf)]),re.M))
    report.check('PDF size',pdf.stat().st_size<=10_000_000,'At most 10 MB.','PDF exceeds 10 MB.')
    report.check('PDF security',info.get('Encrypted','').lower().startswith('no') and
                 not info.get('JavaScript','no').lower().startswith('yes'),
                 'Unencrypted; no document JavaScript.','PDF is encrypted or contains JavaScript.')
    count=int(info.get('Pages','0'))
    report.check('physical page count',count==sum(pages) and 2<=count<=25,
                 f'{count} physical pages agree with the trace.','PDF page count differs from the trace or exceeds limits.')
    for field in ('Title','Author','Subject'):
        value=info.get(field,'')
        valid=bool(value.strip()) and not any(t in value for t in PLACEHOLDERS)
        report.add('metadata '+field,'passed' if valid else ('failed' if release else 'warning'),
                   'Populated.' if valid else 'Missing or placeholder metadata.')
    font_output=run(['pdffonts',str(pdf)])
    rows=[]
    pattern=r'^(\S+)\s+(.+?)\s+(\S+)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$'
    for line in font_output.splitlines()[2:]:
        match=re.match(pattern,line.strip())
        if match: rows.append(match.groups())
    report.check('font embedding',bool(rows) and all(row[3]=='yes' and 'Type 3' not in row[1] for row in rows),
                 'Inspected fonts are embedded; no Type 3 fonts.','Missing, unembedded or Type 3 font.')
    text=run(['pdftotext','-layout','-enc','UTF-8',str(pdf),'-'])
    chunks=text.rstrip('\f\n\r ').split('\f')
    header=(r'Seite\s+(\d+)\s+von\s+max\.\s*(17|8)' if language=='german'
            else r'page\s+(\d+)\s+of\s+max\.\s*(17|8)')
    actual=[]
    for chunk in chunks:
        m=re.search(header,chunk)
        actual.append(tuple(map(int,m.groups())) if m else None)
    expected=[(n,17) for n in range(1,pages[0]+1)]+[(n,8) for n in range(1,pages[1]+1)]
    report.check('visible page sequences',actual==expected,'Visible page headers agree with the 17/8 counts.',
                 'Missing or inconsistent page headers.')
    report.check('extractable text',len(re.sub(r'\s','',text))>100,'PDF text can be extracted.','PDF text is empty.')
    xml=ET.fromstring(run(['pdftohtml','-xml','-zoom','1','-hidden','-i','-stdout',str(pdf)]))
    fontspec={f.attrib['id']:f.attrib for f in xml.iter('fontspec')}
    bad_sizes=[]; bad_fonts=[]; refs=False
    title=next(h[language] for h in profile['headings'] if h['id']=='publications')
    for index,page in enumerate(xml.findall('page'),1):
        w=float(page.attrib['width']); h=float(page.attrib['height'])
        if abs(w-595)>2 or abs(h-842)>2:
            report.add('page dimensions','failed',f'Page {index} is not portrait A4.')
        if index>pages[0]: refs=False
        for node in page.findall('text'):
            content=normal(''.join(node.itertext()))
            if title in content: refs=True; continue
            y=float(node.attrib['top'])
            font=fontspec.get(node.attrib.get('font',''),{})
            # Target paragraph-like runs; image labels and mathematical scripts
            # still require visual review. Exclude official page furniture.
            if y<70 or y>745 or len(re.findall(r'[^\W\d_]',content))<18 or len(content.split())<3:
                continue
            if any(s in content for s in ('Sections 1','Section 4 et','Kapitel 1','Kapitel 4')): continue
            if 'Deutsche Forschungsgemeinschaft' in content or 'Kennedyallee' in content: continue
            minimum=9 if refs and index<=pages[0] else 11
            if float(font.get('size','0')) < minimum-0.5:
                bad_sizes.append(f'page {index}: {font.get("size")} pt: {content[:65]}')
            if release and 'Arial' not in font.get('family',''):
                bad_fonts.append(f'page {index}: {font.get("family")}: {content[:50]}')
    report.add('paragraph text sizes','failed' if bad_sizes else 'passed',
               '; '.join(bad_sizes[:6]) if bad_sizes else 'Inspected paragraph runs meet 11/9 pt thresholds; figure labels and math require visual review.')
    report.add('paragraph fonts','failed' if bad_fonts else 'passed',
               '; '.join(bad_fonts[:6]) if bad_fonts else ('Inspected paragraph runs use Arial.' if release else 'Draft font policy accepted.'))

def validate(source,pdf,language='english',release=False):
    report=Report()
    profile=json.loads((ROOT/'profiles/research-grants-2026-09.json').read_text(encoding='utf-8'))
    stem=pdf.with_suffix('')
    try:
        pages=check_trace(stem.with_suffix('.dfg-audit').read_text(encoding='utf-8'),profile,language,release,report)
        check_log(stem.with_suffix('.log').read_text(encoding='utf-8',errors='replace'),release,report)
        check_inputs(stem.with_suffix('.inputs.json'),source,pdf,release,report)
        check_pdf(pdf,profile,language,release,pages,report)
    except (OSError,ValueError,KeyError,IndexError,ET.ParseError,RuntimeError,subprocess.TimeoutExpired) as exc:
        report.add('inspection','failed',str(exc))
    return report
