"""Build and package self-contained language starters locally; never publishes."""
from pathlib import Path
import argparse
import json
import shutil
import zipfile
from build import ROOT, build
from checks import digest

def package(language,portable=False):
    german=language=='german';suffix='-de' if german else '';short='de' if german else 'en'
    main=ROOT/('main'+suffix+'.tex');example=ROOT/('example'+suffix+'.tex')
    draft_pdf=build(main,language,portable=portable)
    example_pdf=build(example,language,release=not portable,portable=portable)
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    files={}
    for name in ('dfgproposal.cls','dfg-bibliography.sty','dfg-research-grants-2026-09.def',
                 'latexmkrc','LICENSE','NOTICE.md','AUTHORS.md','CITATION.cff'):
        files[name]=(ROOT/name).read_bytes()
    files['main.tex']=main.read_text(encoding='utf-8').replace('metadata'+suffix+'.tex','metadata.tex').encode('utf-8')
    files['metadata.tex']=(ROOT/('metadata'+suffix+'.tex')).read_bytes()
    files['example.tex']=example.read_bytes()
    files['examples/metadata'+suffix+'.tex']=(ROOT/('examples/metadata'+suffix+'.tex')).read_bytes()
    files['project.json']=(json.dumps({'language':language,'source':'main.tex'},indent=2)+'\n').encode()
    files['CHECKLIST.md']=(ROOT/('CURRENT_DFG_COMPLIANCE_CHECKLIST'+('.de' if german else '')+'.md')).read_bytes()
    for directory in ('sections/'+short,'examples/'+short,'bibliography','profiles','figures'):
        for p in (ROOT/directory).rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.tex','.bib','.json','.md','.png','.pdf'):
                files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
    for name in ('SETUP.md','AUTHORING.md','OVERLEAF.md','MIGRATION.md','OFFICIAL_DFG_SOURCES.md','VALIDATION.md'):
        files['docs/'+name]=(ROOT/'docs'/name).read_bytes()
    for name in ('build.py','build.ps1','checks.py','doctor.py','validate_dfg_pdf.py'):
        files['scripts/'+name]=(ROOT/'scripts'/name).read_bytes()
    files['README.md']=(f'# DFG Research Grants starter — {language}\n\n'
        'Unofficial template by Dr. Awanish Pratap Singh. Form profile: September 2026.\n\n'
        '1. Edit metadata.tex.\n2. Write in sections/'+short+'/.\n'
        '3. Add literature to bibliography/references.bib.\n'
        '4. On Overleaf select XeLaTeX and main.tex, then compile.\n\n'
        'Local build (Python 3.10+, TeX distribution and Biber):\n\n'
        '    python scripts/doctor.py\n    python scripts/build.py\n\n'
        'Compile the fictional example:\n\n    python scripts/build.py --source example.tex\n\n'
        'After completing your text:\n\n    python scripts/build.py --release\n\n'
        'Full local inspection also needs Poppler. See docs/SETUP.md and docs/AUTHORING.md.\n'
        'project.json selects this starter’s language automatically.\n'
        'Example content is fictional. Review CHECKLIST.md and the current DFG instructions.\n'
        'See docs/OVERLEAF.md for the cloud verification status.\n').encode('utf-8')
    if german:
        files['README.md']=(
            '# DFG-Sachbeihilfe: LaTeX-Vorlage\n\n'
            'Inoffizielle Vorlage von Dr. Awanish Pratap Singh. Formularstand: September 2026.\n\n'
            '1. Projekttitel und Antragstellende in metadata.tex eintragen.\n'
            '2. Die Texte in sections/de/ bearbeiten.\n'
            '3. Literatur in bibliography/references.bib ergänzen.\n'
            '4. In Overleaf XeLaTeX und main.tex auswählen und kompilieren.\n\n'
            'Lokaler Build (Python 3.10+, TeX-Distribution und Biber):\n\n'
            '    python scripts/doctor.py\n    python scripts/build.py\n\n'
            'Vollständiges fiktives Formatierungsbeispiel:\n\n'
            '    python scripts/build.py --source example.tex\n\n'
            'Nach Fertigstellung des eigenen Textes:\n\n'
            '    python scripts/build.py --release\n\n'
            'Für die vollständige lokale PDF-Prüfung wird zusätzlich Poppler benötigt.\n'
            'project.json wählt automatisch die deutsche Vorlage.\n'
            'CHECKLIST.md vor der Einreichung durcharbeiten und aktuelle DFG-Vorgaben prüfen.\n'
            'Weitere Anleitungen (Englisch): docs/SETUP.md und docs/AUTHORING.md.\n'
            'Den Stand der Overleaf-Prüfung beschreibt docs/OVERLEAF.md.\n'
        ).encode('utf-8')
    archive=dist/f'dfg-starter-{short}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,9,10,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,data)
    for label,pdf in [('starter',draft_pdf),('example',example_pdf)]:
        shutil.copy2(pdf,dist/f'dfg-{label}-{short}.pdf')
    return {'language':language,'archive':archive.name,'sha256':digest(archive),
            'file_count':len(files),'example_checks':'portable draft' if portable else 'submission',
            'example_pdf_sha256':digest(example_pdf)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--portable',action='store_true',help='Create draft-only previews without an Arial release claim.')
    args=p.parse_args()
    records=[package(lang,args.portable) for lang in ('english','german')]
    (ROOT/'dist/package-manifest.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print('Local packages prepared in '+str(ROOT/'dist'))

if __name__=='__main__': main()
