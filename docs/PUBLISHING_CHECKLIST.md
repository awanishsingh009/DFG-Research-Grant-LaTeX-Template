# Preparing a release

This process prepares reviewable local artifacts before publication.

1. Recheck the current official DFG forms and update the profile if necessary.
2. Run profile, unit and compiler integration tests.
3. Build the English and German starters and completed fictional examples.
4. Run strict checks on both examples in an Arial-capable environment.
5. Render and inspect every released preview page.
6. Build the language-specific ZIPs:

       python scripts/package_starters.py

7. Extract both ZIPs into clean directories and compile them independently.
8. Inspect ZIP contents: no personal proposals, fonts, official documents,
   test artifacts, Git metadata or machine-specific input manifests.
9. Record actual platform/compiler versions and any untested environments.
10. Review the diff, migration guide, changelog, author metadata and license.

After the release has been reviewed, publishing can include enabling GitHub's
template-repository setting, creating the version tag and uploading starter ZIPs
and example PDFs as release assets. These are external actions; the packaging
script performs none of them.

An Overleaf verification claim requires an actual import/build there and the
tested TeX Live version. Local ZIP tests alone are insufficient.
