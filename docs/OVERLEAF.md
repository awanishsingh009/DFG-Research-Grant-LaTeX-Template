# Overleaf

1. Upload a language-specific starter ZIP, or the repository ZIP.
2. Choose XeLaTeX in project settings.
3. Select main.tex. In the bilingual repository, choose main-de.tex for German.
4. Compile once before editing; the starter includes a working bibliography.
5. Edit metadata, research sections and references.bib.

The main document, class, bibliography style and latexmkrc are kept at the root.
Biber is selected by the bibliography configuration. No shell-escape or custom
Python execution is required to compile.

Arial appears in Overleaf's published font list. If the selected environment
cannot resolve it, drafting can use the supported fallback. Submission mode
requires Arial and reports an error if it is missing.

When ready, replace draft with submission in the documentclass options.
Unresolved prompts, unsupported submission fonts and page-limit overruns
are class-level errors. The full structural/source/PDF checks require a local
build with the exported sources:

    python scripts/build.py --release

Do not interpret a successful Overleaf compilation as completion of the local
checks or approval of a proposal's substantive content.

**Verification status:** local XeLaTeX, pdfLaTeX and LuaLaTeX results are recorded
in [the verification record](VALIDATION.md). A local ZIP test is not an actual Overleaf cloud test. Record
the Overleaf TeX Live version and results after importing before claiming that
the release has been verified there.

Sources:

- [Main document](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)
- [Project dependencies](https://docs.overleaf.com/managing-projects-and-files/adding-latex-dependencies)
- [latexmkrc](https://docs.overleaf.com/managing-projects-and-files/the-latexmkrc-file)
- [Fonts](https://www.overleaf.com/learn/latex/Questions/Which_OTF_or_TTF_fonts_are_supported_via_fontspec%3F)
