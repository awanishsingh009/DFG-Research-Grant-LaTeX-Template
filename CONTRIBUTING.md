# Contributing

Maintainer: Dr. Awanish Pratap Singh.

Use fictional examples, not real proposal material. Preserve original author
attribution. Changes are contributed under the MIT license.

For a change:

1. Explain the user-facing problem.
2. Ground form changes in the current official sources.
3. Update the profile and generated file together.
4. Run unit tests, builds and relevant integration tests.
5. Inspect both example PDFs visually.
6. Include a migration note when changing author-facing behavior.

    python scripts/generate_profile.py --check
    python -m unittest discover -s tests -v
    python scripts/build.py --language all
    python scripts/build.py --source example.tex --release
    python scripts/build.py --source example-de.tex --language german --release

Set DFG_RUN_TEX_TESTS=1 to include the compiler integration tests. Those tests
use a portable draft font unless they explicitly exercise a submission error,
so the portable CI job does not claim to verify Arial release typography.
Test artifacts are confined to build/.

The generated profile is checked in; users do not need Python to regenerate
anything for editor or Overleaf compilation. Source and PDF checks are separate
from scientific or administrative approval.
