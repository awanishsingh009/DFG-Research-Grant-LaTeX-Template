# Reusable DFG Research Grant preflight checklist

**Maintainer:** Dr. Awanish Pratap Singh

**Template baseline:** 54.01 [06/26] and 53.01 elan [09/25]

**Local verification date:** 31 July 2026

Use this checklist for every project copied from `main.tex`.

## 1. Current-source gate

- [ ] Recheck the official Research Grants forms page on the submission date.
- [ ] Update `guideline-versions.tex` if any form revision changed.
- [ ] Confirm that 53.01 elan remains the correct Project Description template.
- [ ] Confirm all requested module forms and current thresholds, rates and quotation rules.
- [ ] Record the source-check date in the project repository or submission ledger.

## 2. Template and page gate

- [ ] Use `\documentclass[current,submission]{dfgproposal}` for the release build.
- [ ] Keep the official section wording, order and numbering.
- [ ] Sections 1--3 occupy no more than 17 logical pages.
- [ ] Section 4 onward occupies no more than 8 logical pages.
- [ ] Total Project Description length is no more than 25 physical pages.
- [ ] Section 4 starts on supplement page 1.
- [ ] Body, headings, captions, tables and footnotes are Arial at least 11 pt.
- [ ] Body line spacing is at least 1.2; this template uses 11 pt/14.4 pt.
- [ ] Section 3 is Arial at least 9 pt.
- [ ] No manual margin, font-size, line-spacing or page-counter override defeats the class.

## 3. Sections 1--3

- [ ] Section 1 identifies the field state, exact gap, original contribution and preliminary work.
- [ ] Applicant work and third-party work are clearly distinguished.
- [ ] Section 2.1 states requested and total duration.
- [ ] Section 2.2 states objectives and explicitly addresses possible relevance beyond science.
- [ ] Section 2.3 identifies each applicant's responsibilities.
- [ ] Work packages contain methods, units, outcomes, analysis, validity controls, milestones, risks and alternatives.
- [ ] A schedule covers all planned experiments and major tasks.
- [ ] Requested staff and costs map to the work programme.
- [ ] Section 2.4 includes each participating institution's data-management contribution.
- [ ] Section 2.5 addresses all scientifically relevant sex, gender and diversity dimensions.
- [ ] Every work cited in sections 1--2 appears in section 3; section 3 contains no uncited work.
- [ ] All section 3 entries are public, except accepted manuscripts with the required manuscript and editor confirmation.
- [ ] Full titles and DOI, persistent identifier or stable URL are supplied where available.
- [ ] No more than ten applicant works are highlighted across all applicants.
- [ ] No journal impact factors, h-indices or similar metrics are used.

## 4. Section 4

- [ ] Ethical, legal, safety and approval statements are project-specific.
- [ ] Human investigations cover selection, sample size, risks, information/consent, data protection and ethics status.
- [ ] Animal investigations cover model choice, group numbers, statistical design, 3Rs, welfare, severity, endpoints and authorisation.
- [ ] Genetic-resource and access-and-benefit-sharing relevance is assessed.
- [ ] DURC, foreign-trade law, export control and international-cooperation risks are assessed separately.
- [ ] Ecological sustainability is addressed without compromising research quality.
- [ ] Employment status is complete for every applicant.
- [ ] First-time applicant status is stated.
- [ ] Project-group members, German collaborators, foreign collaborators and previous three-year collaborators are complete.
- [ ] Required cooperation declarations and commitments are available.
- [ ] Commercial cooperation and participation are disclosed or explicitly not applicable.
- [ ] Available major equipment and computing resources are identified.
- [ ] Related submissions and overlap are disclosed.
- [ ] Any mandatory proposal-preparation disclosure required by the current form 54.01 is included.

## 5. Section 5 and elan consistency

- [ ] Every requested amount is attributed to an applicant and justified.
- [ ] Section 5 totals match elan after elan's rounding behaviour is considered.
- [ ] Staff category, FTE, duration, start timing and tasks are consistent.
- [ ] Direct-cost quantities, unit costs and totals reconcile with the work programme.
- [ ] Animal numbers, weeks and current form 55.03 rates reconcile across sections 2.3, 4.1.3 and 5.1.2.4.
- [ ] Only project-specific incremental animal costs are requested; institutional baseline and authority fees are excluded.
- [ ] Core-facility costs use transparent, verifiable service units under current form 55.04.
- [ ] Required itemised facility estimates and commercial quotations are attached.
- [ ] Instrumentation requests explain existing alternatives, market comparison, utilisation and host follow-up costs.
- [ ] The sequencing-services total was classified against the current 54.020 boundary.
- [ ] If 54.020 applies, section 5.9, the infrastructural co-applicant, that applicant's CV and the detailed cost estimate are present.
- [ ] Unrequested modules say `Not requested` without renumbering the retained template.

## 6. Part A and attachments

- [ ] German and English summaries in elan match the final Project Description.
- [ ] One current form 53.200 CV is supplied for every applicant.
- [ ] Ethics statements, accepted manuscripts and editor confirmations are attached where required.
- [ ] Cooperation commitments, institutional statements and quotations are attached where required.
- [ ] Attachment filenames follow the current DFG naming protocol.

## 7. Automated and visual release gate

- [ ] Run `make strict SOURCE=main.tex` or `scripts/build.ps1 -Strict` successfully.
- [ ] The source contains no `\DFGInstruction`, `\DFGDecisionRequired`, placeholder metadata, TODO or FIXME marker.
- [ ] XeLaTeX log has no overfull/underfull box, missing-character, undefined-control-sequence, LaTeX, package or class warning requiring resolution.
- [ ] PDF is A4, no more than 10 MB, unencrypted, readable, copyable and printable.
- [ ] PDF metadata title, author and subject are populated.
- [ ] Arial is embedded; Liberation Sans fallback and Type 3 fonts are absent.
- [ ] Text extraction is non-empty and correct.
- [ ] Figures and tables remain legible at normal review zoom and in an A4 print check.
- [ ] Applicant names, project title, page headers and both visible page-limit notices are correct.
