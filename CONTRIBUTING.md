# Contributing

The repository is maintained by **Dr. Awanish Pratap Singh**.

Contributions should improve accuracy, portability, accessibility or
documentation without introducing project-specific proposal material.

Before opening a pull request:

1. compare structural changes with the current official DFG sources;
2. build `main.tex` successfully with XeLaTeX;
3. run `python scripts/validate_dfg_pdf.py main.tex build/main.pdf --allow-guidance`;
4. inspect the compiled PDF visually;
5. keep third-party DFG documents, proposal data and generated files out of the
   commit;
6. explain the reason and official source for any compliance-related change.

By submitting a contribution, you agree that it may be distributed under the
MIT License.
