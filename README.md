# DFG Research Grant LaTeX Template

[English](README.md) · [Deutsch](README.de.md)

Write a DFG Research Grants project description with a short main document,
separate research sections, working citations and clear build checks.
Created and maintained by **Dr. Awanish Pratap Singh** ([awanishsingh009](https://github.com/awanishsingh009)). Unofficial; MIT licensed.

**Form profile:** 53.01 and 54.01, September 2026. Sources checked 10 September 2026.
Supports Research Grants (Sachbeihilfe). Other programmes require their own verified templates.

## Start writing

1. Download the [English starter](https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template/releases/download/v2.0.0/dfg-starter-en.zip) or [German starter](https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template/releases/download/v2.0.0/dfg-starter-de.zip), or use this repository as a GitHub template.
2. Edit [metadata.tex](metadata.tex) (English) or [metadata-de.tex](metadata-de.tex) (German).
3. Write in [sections/en](sections/en) or [sections/de](sections/de).
4. Add your literature to [bibliography/references.bib](bibliography/references.bib).
5. Compile.

On **Overleaf**, upload the project ZIP, choose XeLaTeX, and set the main document
to main.tex or main-de.tex. No Python is required for Overleaf compilation.
The local Python/PDF checks do not run automatically on Overleaf.
[Overleaf instructions](docs/OVERLEAF.md).

On **your computer**, install a TeX distribution with XeLaTeX and Biber, plus
Python 3.10 or newer. No pip packages or Perl are needed by the supplied builder.

    python scripts/doctor.py
    python scripts/build.py

For German, in the bilingual repository:

    python scripts/build.py --language german

On macOS/Linux use python3 if python is unavailable. PDF inspection additionally
uses Poppler. Missing optional inspection tools are reported as “not checked”
in a draft; they block a release build. [Installation and troubleshooting](docs/SETUP.md).

## Learn from a working example

Compile [example.tex](example.tex) or [example-de.tex](example-de.tex):

    python scripts/build.py --source example.tex
    python scripts/build.py --source example-de.tex --language german

The fictional examples demonstrate multiple applicants, citations, numbered
cross-references, an equation, a figure, a schedule and a funding table. They
are formatting demonstrations, not research proposals or approved declarations.
[Preview PDFs and starter ZIPs are available in the v2.0.0 release](https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template/releases/tag/v2.0.0).
You can also prepare them locally with the packaging command below.

## Prepare a submission copy

Replace all writing prompts and placeholder metadata. Assess and complete the
ethics-statement choice in the research-context section. Then run:

    python scripts/build.py --release

This selects submission mode without editing your source and requires Arial,
a complete build, resolved citations/references, the current profile's effective
heading sequence, the 17/8 page limits and the PDF inspection tools.

Draft: build/draft/english/xelatex/main.pdf

Submission: build/release/english/xelatex/main.pdf

The adjacent .checks.json file lists each check, warnings and items not checked.
The PDF and input hashes identify the checked build. **Formatting checks do not
assess scientific content, ethics approvals, eligibility or all figure labels.**
Review the final PDF and the [submission checklist](CURRENT_DFG_COMPLIANCE_CHECKLIST.md).
Recheck the [official DFG forms](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/research-grants/forms-guidelines)
before submitting.

## Useful commands

    python scripts/build.py --language all
    python scripts/build.py --engine pdflatex
    python scripts/build.py --portable
    python scripts/build.py --engine lualatex --release
    powershell -File scripts/build.ps1 -Language german -Strict

pdfLaTeX and portable fonts are for drafting. The builder runs Biber when needed
and repeats TeX until references settle. latexmk is optional; its configuration
is included for editors and Overleaf. On MiKTeX it needs Perl.

## Documentation

- [Authoring: applicants, references, figures and modules](docs/AUTHORING.md)
- [Setup and troubleshooting](docs/SETUP.md)
- [Overleaf](docs/OVERLEAF.md)
- [Upgrade from version 1](docs/MIGRATION.md)
- [Official sources and verified profile](docs/OFFICIAL_DFG_SOURCES.md)
- [Contributing and tests](CONTRIBUTING.md)
- [What has been tested](docs/VALIDATION.md)
- [Preparing release assets](docs/PUBLISHING_CHECKLIST.md)

To create local language-specific starter packages and example PDFs:

    python scripts/package_starters.py

The output is in dist/. Packaging builds and checks the shipped examples; it
does not publish anything or modify GitHub settings.

## License and citation

Original code and documentation: [MIT License](LICENSE).
DFG names, official forms and linked documents retain their respective rights.
No proprietary font files or official DFG documents are distributed.
Repository citation metadata is provided in [CITATION.cff](CITATION.cff);
citing the template in your actual proposal is optional.
