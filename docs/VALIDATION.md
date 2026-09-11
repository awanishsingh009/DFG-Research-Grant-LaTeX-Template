# Local verification — 10 September 2026

This record covers the local verification performed before publication of v2.0.0.
The verified form profile is Research Grants 53.01 / 54.01, September 2026.
See [the source record](OFFICIAL_DFG_SOURCES.md) for official links and hashes.

## Environment and results

Windows; Python 3.11.3; MiKTeX 25.4; Biber 2.21; Arial available.
Compiler versions: MiKTeX-XeTeX 4.15, MiKTeX-pdfTeX 4.21 and LuaHBTeX 1.22.0.
PDF inspection used pdfinfo, pdffonts, pdftotext and pdftohtml.

| Verification | Result |
|---|---|
| Generated TeX profile matches its JSON source | Passed |
| Unit and real compiler regression suite | 34 tests passed; none skipped locally |
| English and German XeLaTeX starters | Passed draft checks |
| English and German pdfLaTeX starters | Passed draft checks |
| English and German completed XeLaTeX examples | Passed submission checks |
| English completed LuaLaTeX example | Passed submission checks |
| Clean ZIP extraction into directories containing spaces | Both languages built successfully |
| Completed examples from extracted ZIPs | Both passed submission checks |
| Four delivered previews | Five pages each; all 20 pages rendered and visually inspected |

The starter PDFs contain intentional prompts, placeholder metadata and a pending
ethics choice. Their reports warn about these; they are draft previews.
The completed examples contain explicitly fictional content and declarations.
Passing their format checks is not approval of a real proposal.

The regressions exercise actual heading execution, inactive and duplicate
headings, real section references, bibliography scope, Biber input tracking,
page limits including a final queued float, missing characters/citations,
undersized paragraph text, unresolved submission prompts and highlight limits.

## Reproduce locally

    python scripts/generate_profile.py --check
    python -m unittest discover -s tests -v
    python scripts/package_starters.py

Set the environment variable DFG_RUN_TEX_TESTS=1 for the eight real compiler
tests; otherwise they are explicitly skipped. The other 26 tests do not compile
documents. Extract each starter ZIP into its own fresh directory, then run:

    python scripts/build.py
    python scripts/build.py --source example.tex --release

The Python commands worked with the existing Windows script policy. That policy
blocked the optional PowerShell wrapper; no execution-policy change was needed
for the documented Python route. MiKTeX's optional latexmk launcher could not
run without Perl; the Python builder ran TeX and Biber directly.

## Verification limits

Remote workflow results are available in [GitHub Actions](https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template/actions/workflows/build.yml).
No macOS, Linux or Overleaf cloud result is claimed by this local verification record.
Arial submission typography requires a separate Arial-capable environment
when the portable CI job is used.

Automatic checks do not establish scientific accuracy, funding eligibility,
ethics approval, the adequacy of explanations, all figure labels, mathematical
script sizes or exact line spacing. Authors must inspect their final PDF and
recheck the current official instructions before submission.
