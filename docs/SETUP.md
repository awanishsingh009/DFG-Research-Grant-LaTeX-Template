# Setup and troubleshooting

## Requirements

The local Python builder needs Python 3.10+, a TeX distribution containing
XeLaTeX (or LuaLaTeX/pdfLaTeX), and Biber for the default bibliography.
It uses only Python's standard library. It does not depend on latexmk or Perl.
Direct TeX-editor and Overleaf compilation do not need Python.

Full PDF inspection needs Poppler's pdfinfo, pdffonts, pdftotext and pdftohtml
on PATH. Arial is required by this template's conservative submission mode.
Obtain fonts through a legitimate system installation; do not redistribute them.

    python scripts/doctor.py --release

The diagnostic checks tools without installing or changing anything. A compiler
version check does not establish that every LaTeX package or font is installed;
the first real compilation checks those.

## Windows

Install MiKTeX or TeX Live and Python 3.10+. Enable their command-line tools in PATH.
On MiKTeX, use its package manager to install missing packages, including Biber.
Install Poppler and add its bin directory to PATH for full inspection.
Reopen the terminal after changing PATH.

    python scripts/build.py

The optional wrapper also tries python3 and py:

    powershell -File scripts/build.ps1 -Language english

If PowerShell script execution is restricted, use the Python command directly;
changing the computer's execution policy is unnecessary.

MiKTeX's latexmk launcher requires Perl. The supplied Python builder does not,
even when the launcher exists but cannot run.

## macOS

Install MacTeX (or a TeX distribution with the listed packages), Python 3.10+
and Poppler using your preferred package manager. Check availability with:

    python3 scripts/doctor.py
    python3 scripts/build.py

## Linux

Install your distribution's TeX Live XeTeX, LaTeX extra, recommended fonts,
German language, Biber and Poppler utility packages, plus Python 3.10+.
For Ubuntu/Debian, the CI workflow documents the packages used for portable tests.
Use an Arial-capable installation for submission or portable mode for drafts:

    python3 scripts/build.py --portable

## Compilers and modes

- XeLaTeX is the documented default.
- LuaLaTeX is selectable with --engine lualatex.
- pdfLaTeX uses Helvetica and is drafting-only.
- --portable selects Liberation Sans or TeX Gyre Heros for drafting.
- --release overrides the source's draft setting and requires the release checks.
- In Overleaf, change the class option from draft to submission instead.

The English and German single-language ZIPs contain a project.json that selects
their default language and source. The bilingual repository defaults to English.

## Common errors

| Message | Action |
|---|---|
| Required tools missing | Run doctor.py, install the named tool and reopen your terminal |
| Arial is unavailable | Use a lawful Arial installation or draft with a fallback |
| Unresolved writing prompt | Replace each DFGTodo with your own text; do not hide unresolved decisions |
| Undefined citation | Check the citation key and .bib entry, then rebuild |
| Compilation did not converge | Inspect the last pass log for changing references or package warnings |
| Heading sequence | Compare the emitted .dfg-audit trace with the current profile |
| Source freshness | A source or the PDF changed after compilation; rebuild |
| Paragraph text sizes/fonts | Inspect the named page; mathematical scripts and figure artwork also need visual review |

The build directory contains compiler-pass logs, Biber output and the final
LaTeX log. An old PDF may remain after a failed build for recovery, but its
previous success report is invalidated and the command reports failure.
Only a successful current .checks.json belongs to a checked build.
