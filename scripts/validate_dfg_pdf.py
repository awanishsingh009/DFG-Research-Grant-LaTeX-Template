"""Recheck an existing build. Release checks require its trace, log and input manifest."""
from pathlib import Path
import argparse
from checks import validate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('pdf',type=Path)
    p.add_argument('--language',choices=['english','german'],default='english')
    p.add_argument('--allow-guidance',action='store_true')
    p.add_argument('--allow-draft-font',action='store_true',help='Compatibility flag; draft builds already allow supported fallback fonts.')
    args=p.parse_args()
    if args.allow_draft_font and not args.allow_guidance: p.error('Draft fonts cannot be used with submission checks.')
    return validate(args.source.resolve(),args.pdf.resolve(),args.language,not args.allow_guidance).emit()

if __name__=='__main__': raise SystemExit(main())
