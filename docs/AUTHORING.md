# Authoring guide

## Files you edit

Metadata contains the project title, applicant list and keywords.
The section files contain your scientific and administrative text.
The .bib file contains literature; figures/ holds your artwork.
The class and generated form profile normally require no author edits.

    \DFGSetProjectTitle{A project title}
    \DFGAddApplicant{pi1}{First Last}{City}
    \DFGAddApplicant{pi2}{Second Last}{Another city}

Applicant IDs must be unique. Use \DFGApplicantWork{pi1} to identify an applicant's
work programme. Preserve TeX escapes such as \&, \%, \_ and \# in metadata.
Names with accented characters are supported by the Unicode compilers.

## Headings and references

Official headings use semantic IDs, for example:

    \DFGHeading{objectives}
    \label{sec:objectives}
    The approach follows section~\ref{sec:objectives}.

The displayed heading number and language come from the checked profile.
Automatic labels are also available: \ref{dfg:objectives}.
Use \DFGWorkPackage{WP1}{Work-package title} for an unnumbered work-package heading.
Avoid inventing or renumbering official headings. Keep required headings even
when the subject is not relevant.

Ordinary \input, \label, \ref, figure, table and equation environments work.
Paths in nested \input files are resolved from the project root, as in LaTeX.

## Literature

The default style uses BibLaTeX and Biber. Add entries to references.bib and cite:

    Prior work~\cite{yourkey}.

\DFGPrintReferences prints section 3. Sections 1 and 2 are in their own
bibliography refsection, which ends at \DFGStartSupplement. Citations used only
in the supplement therefore do not enter the main publication list.

To highlight relevant applicant works:

    \DFGHighlightPublications{key1,key2}

Select at most ten distinct works across all applicants. Duplicate keys do not
consume the limit twice. Mark actual applicant publications, not arbitrary
example references. The template does not verify authorship or publication status.
Check full titles, persistent links and bibliography details yourself.

For a manual bibliography, use the manualbibliography class option, remove
\addbibresource and \DFGPrintReferences, and put a manually authored list between:

    \DFGHeading{publications}
    \DFGStartReferences
    Your manual bibliography here.
    \DFGEndReferences

Keep the main/supplement commands. Manual lists cannot receive automated
citation-key matching and highlight counting.

## Prompts, applicability and ethics

Replace \DFGTodo{...} with your actual text. It is a visible drafting prompt and
an error in submission mode. \DFGInstruction remains a compatibility alias.
Do not hide prompts as a way to complete the application.

    \DFGNotApplicable{A project-specific explanation.}
    \DFGNotRequested{A project-specific explanation.}

These helpers do not establish eligibility or factual non-applicability.
The ethics section requires a deliberate assessment:

    \DFGEthicsStatement{yes}

or no. The starter uses pending. The checker verifies an explicit choice,
not the scientific or legal adequacy of the assessment.

## Figures, tables and schedules

Prefer PDF artwork for vector figures and PNG for raster images.
Use a figure caption and a label, then \ref{fig:yourlabel}.
The fictional example contains a vector drawing made with native LaTeX,
an equation, a schedule and a funding table.

Body text, captions and table text retain the normal 11-point size.
Do not shrink a large table until it fits; restructure it.
Keep figure labels legible at their final printed size. Automated paragraph
inspection cannot fully assess image text, mathematical scripts or line spacing.

## Optional services

The profile includes an optional final services heading:

    \DFGHeading{services}

Use it only when the current sequencing-services instructions apply. Verify
eligibility, scope, financial thresholds and the required additional applicant
information in form 54.020. This is not a switch that grants eligibility.
