"""Build a DFG proposal with Biber and convergence checks. Python 3.10+, no pip packages."""
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from checks import PDF_TOOLS, digest, strip_comments, validate

ROOT=Path(__file__).resolve().parents[1]

def dependency_errors(engine,release,manual=False):
    required=[engine]+([] if manual else ['biber'])+(list(PDF_TOOLS) if release else [])
    return [name for name in required if not shutil.which(name)]

def compile_command(command,output,logname):
    proc=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                        text=True,encoding='utf-8',errors='replace',timeout=180)
    (output/logname).write_text(proc.stdout,encoding='utf-8')
    if proc.returncode:
        raise RuntimeError(f'{command[0]} failed. See {output/logname}\n'+proc.stdout[-1800:])

def build(source,language,engine='xelatex',release=False,portable=False,output=None):
    source=source.resolve()
    if not source.is_relative_to(ROOT) or not source.is_file():
        raise RuntimeError('Source must be an existing .tex file inside this project.')
    relative=source.relative_to(ROOT).as_posix()
    if source.suffix!='.tex' or any(c in relative for c in '%#{}\\') or not re.fullmatch(r'[A-Za-z0-9_-]+',source.stem):
        raise RuntimeError('Use a .tex filename with letters, digits, hyphens or underscores; avoid TeX-special path characters.')
    output=output or ROOT/'build'/('release' if release else 'draft')/language/engine
    output=output.resolve()
    if not output.is_relative_to(ROOT/'build'): raise RuntimeError('Build output must remain under this project’s build directory.')
    output.mkdir(parents=True,exist_ok=True)
    stem=output/source.stem
    # Invalidate prior success before doing any work; retain the old PDF for recovery.
    for suffix in ('.checks.json','.inputs.json'):
        stem.with_suffix(suffix).unlink(missing_ok=True)
    if release and (portable or engine=='pdflatex'):
        raise RuntimeError('Release builds require XeLaTeX/LuaLaTeX and Arial; portable/pdfLaTeX is drafting-only.')
    manual='manualbibliography' in strip_comments(source.read_text(encoding='utf-8'))
    missing=dependency_errors(engine,release,manual)
    if missing: raise RuntimeError('Required tools missing: '+', '.join(missing)+'. See docs/SETUP.md.')
    prefix=(r'\def\DFGForceSubmission{1}' if release else '')
    if portable: prefix+=r'\PassOptionsToClass{portable}{dfgproposal}'
    tex=prefix+r'\input{'+relative+'}'
    base=[engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder',
          '-no-shell-escape','-jobname='+source.stem,'-output-directory='+str(output),tex]
    prior=None; bcf_hash=None
    for pass_number in range(1,7):
        print(f'{language}: {engine} pass {pass_number}',flush=True)
        compile_command(base,output,source.stem+f'.pass-{pass_number}.txt')
        bcf=stem.with_suffix('.bcf')
        if not manual and bcf.exists() and digest(bcf)!=bcf_hash:
            print(f'{language}: resolving bibliography with Biber',flush=True)
            compile_command(['biber','--input-directory',str(output),'--output-directory',str(output),source.stem],
                            output,source.stem+'.biber.txt')
            bcf_hash=digest(bcf)
        state=tuple((ext,digest(stem.with_suffix(ext))) for ext in ('.aux','.bbl','.out','.toc')
                    if stem.with_suffix(ext).exists())
        if pass_number>=2 and state==prior: break
        prior=state
    else: raise RuntimeError('Compilation did not converge after six passes. Inspect the logs.')
    pdf=stem.with_suffix('.pdf')
    inputs={source}
    for line in stem.with_suffix('.fls').read_text(encoding='utf-8',errors='replace').splitlines():
        if line.startswith('INPUT '):
            p=Path(line[6:])
            if not p.is_absolute(): p=ROOT/p
            p=p.resolve()
            if p.is_relative_to(ROOT) and not p.is_relative_to(ROOT/'build') and p.is_file():
                inputs.add(p)
    # Biber reads .bib files separately; they do not appear in TeX's recorder.
    bcf=stem.with_suffix('.bcf')
    if not manual and bcf.exists():
        for node in ET.parse(bcf).getroot().iter('{https://sourceforge.net/projects/biblatex}datasource'):
            if node.text and node.attrib.get('type')=='file':
                bib=Path(node.text)
                if not bib.is_absolute(): bib=ROOT/bib
                if node.attrib.get('glob')=='true':
                    inputs.update(p.resolve() for p in bib.parent.glob(bib.name) if p.is_file())
                elif bib.is_file():
                    inputs.add(bib.resolve())
    inputs.add(ROOT/'profiles/research-grants-2026-09.json')
    manifest={'source':str(source),'pdf_sha256':digest(pdf),'engine':engine,'language':language,'release':release,
              'inputs':[{'path':str(p),'sha256':digest(p)} for p in sorted(inputs)]}
    stem.with_suffix('.inputs.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    report=validate(source,pdf,language,release)
    payload={'pdf':pdf.name,'pdf_sha256':digest(pdf),'mode':'submission' if release else 'draft',
             'passed':not report.failed,'checks':report.items}
    stem.with_suffix('.checks.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    code=report.emit()
    if code: raise RuntimeError(f'Checks failed. Inspect {stem.with_suffix(".checks.json")}')
    print(f'Built: {pdf}',flush=True)
    return pdf

def main():
    config_path=ROOT/'project.json'
    config=json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--language',choices=['english','german','all'],default=config.get('language','english'))
    p.add_argument('--engine',choices=['xelatex','lualatex','pdflatex'],default='xelatex')
    p.add_argument('--source',type=Path)
    p.add_argument('--release',action='store_true')
    p.add_argument('--portable',action='store_true')
    args=p.parse_args()
    if args.source and args.language=='all': p.error('--source requires one language.')
    if config and args.language != config.get('language'):
        p.error('This single-language starter supports '+config['language']+'. Use the bilingual repository for other languages.')
    try:
        for lang in (['english','german'] if args.language=='all' else [args.language]):
            source=args.source or Path(config.get('source') or ('main.tex' if lang=='english' else 'main-de.tex'))
            build(ROOT/source,lang,args.engine,args.release,args.portable)
    except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
        print('BUILD FAILED: '+str(exc),file=sys.stderr); return 1
    return 0

if __name__=='__main__': raise SystemExit(main())
