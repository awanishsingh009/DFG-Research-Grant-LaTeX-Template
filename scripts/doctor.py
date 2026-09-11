"""Check the local build environment without changing or installing anything."""
import argparse
import shutil
import subprocess
import sys
from checks import PDF_TOOLS

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',choices=['xelatex','lualatex','pdflatex'],default='xelatex')
    p.add_argument('--release',action='store_true')
    args=p.parse_args()
    failed=False
    print(f'Python: {sys.version.split()[0]}')
    for name in [args.engine,'biber',*PDF_TOOLS]:
        found=shutil.which(name)
        required=name in (args.engine,'biber') or args.release
        print(f'{"OK" if found else "MISSING" if required else "OPTIONAL"}: {name}'+(f' — {found}' if found else ''))
        failed=failed or (required and not found)
    if shutil.which(args.engine):
        try:
            result=subprocess.run([args.engine,'--version'],capture_output=True,timeout=20)
            if result.returncode: print('FAILED: compiler version probe'); failed=True
        except (OSError,subprocess.TimeoutExpired): print('FAILED: compiler is not usable'); failed=True
    if shutil.which('latexmk'):
        try:
            r=subprocess.run(['latexmk','-v'],capture_output=True,timeout=20)
            print('OPTIONAL: latexmk '+('works.' if not r.returncode else 'cannot run; on MiKTeX check Perl. The Python builder does not need it.'))
        except (OSError,subprocess.TimeoutExpired): print('OPTIONAL: latexmk did not respond; the Python builder does not need it.')
    print('Arial availability is checked by the TeX class during an actual release build.')
    print('Setup instructions: docs/SETUP.md. No tools were installed.')
    return int(failed)

if __name__=='__main__': raise SystemExit(main())
