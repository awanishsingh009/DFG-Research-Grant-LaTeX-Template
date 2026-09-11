# Official sources

Profile: research-grants-2026-09. Verified 10 September 2026.
Authoritative entry point: [Research Grants forms and guidelines](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/research-grants/forms-guidelines).

| Document | Verified revision | Source |
|---|---|---|
| Project description 53.01, English | 09/26 | [RTF](https://www.dfg.de/resource/blob/168206/53-01-en-elan.rtf) |
| Project description 53.01, German | 09/26 | [RTF](https://www.dfg.de/resource/blob/168204/53-01-de-elan.rtf) |
| Proposal instructions 54.01 | 09/26 | [English PDF](https://www.dfg.de/resource/blob/168314/54-01-en.pdf) |
| Research Grants 50.01 | 09/26 | [English PDF](https://www.dfg.de/resource/blob/168072/50-01-en.pdf) |
| Science Communication module 52.07 | 09/26 | Use the current link on the forms page |
| CV 53.200 | 07/25 | Use the current link on the forms page |
| Form changes | 09/26 | [Change register](https://www.dfg.de/resource/blob/334100/sachbeihilfe-info-vordrucksaenderungen.pdf) |

The profile JSON records the URLs and SHA-256 hashes of the English and German
RTFs inspected. It contains ordered heading IDs, translations and limits.
The generated .def file is included so compilation works without a generator.

Changing the printed version label is not a migration. Update the profile,
guidance, tests and migration notes together, then regenerate and inspect:

    python scripts/generate_profile.py
    python scripts/generate_profile.py --check

Check current personnel rates, cost thresholds and optional module instructions
at the time of application. Compilation does not download or switch profiles.
Third-party DFG documents and proprietary fonts are not distributed.
The optional download helper creates an ignored local snapshot only.
