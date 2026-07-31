# DFG Research Grant LaTeX Template

A reusable English LaTeX template for DFG Research Grant project descriptions,
maintained by **Dr. Awanish Pratap Singh**.

The package reproduces the practical typography and section hierarchy needed
for a DFG-style project description while keeping the source editable,
version-controlled and suitable for collaborative scientific writing.

> [!IMPORTANT]
> This is an independent, unofficial template. It is not published, endorsed
> or maintained by the Deutsche Forschungsgemeinschaft (DFG). The current DFG
> forms, elan template and programme instructions always take precedence.

## Current baseline

The repository was checked on 31 July 2026 against:

- DFG form 54.01, Project Proposal Instructions `[06/26]`
- DFG form 53.01 elan, Project Description `[09/25]`
- Research Grant programme and module documents listed in
  [`docs/OFFICIAL_DFG_SOURCES.md`](docs/OFFICIAL_DFG_SOURCES.md)

Always recheck the
[official Research Grant forms page](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/research-grants/forms-guidelines)
on the submission date.

## Features

- complete current project-description section structure;
- drafting and strict submission modes;
- 17-page and 8-page logical page-limit handling;
- Arial release-mode enforcement;
- DFG-style headings, page headers and footer treatment;
- reusable table, figure and not-applicable helpers;
- automated source and PDF preflight checks;
- Windows PowerShell and portable Makefile build commands;
- official-source register without redistributed third-party documents.

## Quick start

Requirements:

- XeLaTeX from MiKTeX or TeX Live;
- Arial for the strict release build;
- Python 3;
- Poppler commands `pdfinfo`, `pdffonts` and `pdftotext`.

Clone the repository, edit the metadata and guidance blocks in `main.tex`, then
build a drafting copy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1
```

On systems with `make`:

```bash
make draft
```

The PDF is written to `build/main.pdf`.

Before submission, remove all instructions and placeholders and change:

```tex
\documentclass[current,guidance]{dfgproposal}
```

to:

```tex
\documentclass[current,submission]{dfgproposal}
```

Then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Strict
```

or:

```bash
make strict
```

Complete `CURRENT_DFG_COMPLIANCE_CHECKLIST.md` and visually inspect every page.

For repository publication and release checks, follow
[`docs/PUBLISHING_CHECKLIST.md`](docs/PUBLISHING_CHECKLIST.md).

## Repository structure

```text
.
|-- main.tex
|-- dfgproposal.cls
|-- guideline-versions.tex
|-- CURRENT_DFG_COMPLIANCE_CHECKLIST.md
|-- bibliography/
|-- figures/
|-- docs/
|-- scripts/
|-- CITATION.cff
`-- LICENSE
```

Third-party DFG files are not stored in the repository. The source register
provides official links, and the download helper can create an ignored local
snapshot:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_official_sources.ps1
```

## Citation

If this template supports a proposal, cite the repository metadata in
`CITATION.cff`:

> Singh, A. P. (2026). *DFG Research Grant LaTeX Template* (Version 1.0.0).

## License and trademarks

The original template code and documentation are released under the MIT
License. DFG names, forms, branding and linked documents remain the property of
their respective rights holders and are not covered by this repository's
license.

## Author and maintainer

**Dr. Awanish Pratap Singh**

[GitHub profile](https://github.com/awanishsingh009)
