# Migrating a version 1 proposal

Keep a backup or Git commit of your existing proposal before migrating.
Version 2 is a form and author-workflow update, not just a replacement class.
Do not overwrite an existing proposal directory with a starter ZIP.

1. Create a new v2 project beside the old proposal.
2. Transfer title and applicant details into its metadata file.
3. Transfer your research text into the corresponding section files.
4. Migrate ethics content against the September 2026 form.
5. Transfer bibliography entries and figure files; verify citations and references.
6. Build and inspect the resulting PDF before continuing.

## Ethics mapping

| Earlier structure | September 2026 structure |
|---|---|
| 4.1.1 general ethics | 4.1.1 general ethics and obligations, including the explicit ethics-statement choice |
| 4.1.2 human-investigations subsection | No separate subsection in the new RTF; retain relevant content in the appropriate ethics/methods discussion |
| 4.1.3 animals | 4.1.2 animals |
| 4.1.4 genetic resources | 4.1.3 genetic resources |
| 4.1.5 safety | 4.1.4 safety |
| 4.1.5.1 / 4.1.5.2 | 4.1.4.1 / 4.1.4.2 |
| 4.1.6 sustainability | 4.1.5 sustainability |
| 5.7 Public Relations | 5.7 Science Communication |

Do not automatically delete human-research content or infer ethics answers.
Recheck budgets and current module instructions where relevant.

## Compatibility and intentional changes

- current and guidance class options remain aliases; draft is the ordinary starter mode.
- Common v1 metadata setters and DFGInstruction remain available.
- Old two-argument DFGSection/DFGSubsection commands render, but their effective
  numbers and titles must match the current profile to pass checks.
- The old birth/nationality, contact and affiliation header setters are not
  carried into the generic v2 header. Put necessary information in the official
  location specified by the form.
- Historical dfg000 calibration is not part of v2. Use a pinned v1 checkout
  to reproduce historical documents.
- The default bibliography is now BibLaTeX/Biber. Choose manualbibliography
  explicitly if retaining a manually written list.
- Output paths now separate draft/release, language and compiler.
- The PowerShell wrapper delegates to Python. -Strict selects submission mode
  itself; Python must be available. The former -Clean switch was removed.
- The parity checker now consumes completed .dfg-audit traces rather than
  counting commands in source files.

Never update just the printed form date on an old document and assume the
contents are current.
