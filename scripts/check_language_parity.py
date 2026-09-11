"""Check effective bilingual structure using completed compilation traces."""
from pathlib import Path
import argparse
import json
from checks import ROOT, Report, check_trace

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('english',type=Path,help='English .dfg-audit trace')
    p.add_argument('german',type=Path,help='German .dfg-audit trace')
    args=p.parse_args()
    profile=json.loads((ROOT/'profiles/research-grants-2026-09.json').read_text(encoding='utf-8'))
    report=Report()
    for lang,path in [('english',args.english),('german',args.german)]:
        try: check_trace(path.read_text(encoding='utf-8'),profile,lang,False,report)
        except OSError as exc: report.add(lang+' trace','failed',str(exc))
    return report.emit()

if __name__=='__main__': raise SystemExit(main())
