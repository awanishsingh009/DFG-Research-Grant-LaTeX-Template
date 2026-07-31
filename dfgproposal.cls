\NeedsTeXFormat{LaTeX2e}
% Author: Dr. Awanish Pratap Singh
\ProvidesClass{dfgproposal}[2026/07/31 v1.1 reusable DFG project-proposal layout]

\newif\ifdfglegacy
\newif\ifdfgsubmission
\dfglegacyfalse
\dfgsubmissionfalse
\DeclareOption{dfg000}{\dfglegacytrue}
\DeclareOption{current}{\dfglegacyfalse}
\DeclareOption{guidance}{\dfgsubmissionfalse}
\DeclareOption{submission}{\dfgsubmissiontrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ExecuteOptions{current,guidance}
\ProcessOptions\relax

\LoadClass[11pt,a4paper]{article}

\RequirePackage{iftex}
\ifPDFTeX
  \ClassError{dfgproposal}{Use XeLaTeX, LuaLaTeX, or Tectonic}{This class uses fontspec so that Arial can be selected exactly.}
\fi

\RequirePackage{fontspec}
\IfFontExistsTF{Arial}{%
  \setmainfont{Arial}[Ligatures=TeX]
  \newcommand{\DFGResolvedFont}{Arial}%
}{%
  \setmainfont{Liberation Sans}[Ligatures=TeX]
  \newcommand{\DFGResolvedFont}{Liberation Sans (Arial-compatible fallback)}%
  \ifdfgsubmission
    \ClassError{dfgproposal}{Arial was not found in submission mode}{Install Arial and rebuild with XeLaTeX before submission. Liberation Sans is permitted only for drafting.}%
  \else
    \ClassWarningNoLine{dfgproposal}{Arial was not found. Using Liberation Sans for development; install Arial before a final DFG submission}%
  \fi
}

\ifdfglegacy
  % Calibrated against the historical DFG000 PDF; do not change.
  \RequirePackage[a4paper,top=24.06mm,left=25mm,right=20mm,bottom=15mm,
    headheight=12.2pt,headsep=9mm,footskip=12mm]{geometry}
\else
  % Current 53.01 RTF: 1418/1134/1418/851 twips = 25/20/25/15 mm.
  \RequirePackage[a4paper,top=25mm,left=25mm,right=20mm,bottom=15mm,
    headheight=12.2pt,headsep=9mm,footskip=12mm]{geometry}
\fi
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{fancyhdr}
\RequirePackage{microtype}
\RequirePackage{ragged2e}
\RequirePackage{etoolbox}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{textcomp}
\RequirePackage{enumitem}
\RequirePackage{array}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{tabularx}
\RequirePackage{colortbl}
\RequirePackage{multirow}
\RequirePackage{hhline}
\RequirePackage{caption}
\RequirePackage{xurl}
\RequirePackage[hidelinks,unicode,hypertexnames=false]{hyperref}

\definecolor{DFGBlue}{HTML}{00549F}

\makeatletter
\renewcommand\normalsize{%
  \ifdfglegacy
    \@setfontsize\normalsize{11pt}{14.55pt}%
  \else
    % Current 53.01 RTF uses 11 pt text with 14.4 pt line spacing.
    \@setfontsize\normalsize{11pt}{14.4pt}%
  \fi
  \abovedisplayskip 7pt plus 2pt minus 2pt%
  \belowdisplayskip 7pt plus 2pt minus 2pt%
  \abovedisplayshortskip 3pt plus 2pt%
  \belowdisplayshortskip 5pt plus 2pt minus 2pt%
}
\ifdfglegacy
  \renewcommand\small{\@setfontsize\small{9pt}{12.3pt}}
  \renewcommand\footnotesize{\@setfontsize\footnotesize{8pt}{9.6pt}}
\else
  % Current-form applicant content must not fall below 11 pt.
  \renewcommand\small{\@setfontsize\small{11pt}{14.4pt}}
  \renewcommand\footnotesize{\@setfontsize\footnotesize{11pt}{14.4pt}}
\fi
\makeatother
\normalsize

\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt plus 1pt minus 1pt}
\setlist{nosep,leftmargin=5mm,topsep=2pt}
\justifying
\setlength{\JustifyingParindent}{0pt}
\urlstyle{same}
\setlength{\emergencystretch}{2em}
\ifdfglegacy
  % Word-style no-hyphenation was measured in the historical DFG000 PDF.
  % Current proposals retain normal TeX hyphenation for robust reflow.
  \hyphenpenalty=10000
  \exhyphenpenalty=10000
\fi
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\ifdfglegacy
  \captionsetup{font=small,labelfont={bf,it},textfont=it,
    labelsep=space,justification=justified,singlelinecheck=false,skip=3pt}
\else
  % Captions are proposal content and therefore retain the 11 pt minimum.
  \captionsetup{font=normalsize,labelfont={bf,it},textfont=it,
    labelsep=space,justification=justified,singlelinecheck=false,skip=3pt}
\fi

\newcommand{\DFGFormLabel}{DFG form 53.01}
\newcommand{\DFGProjectDescriptionRevision}{09/25}
\newcommand{\DFGProposalInstructionsRevision}{06/26}
\newcommand{\DFGMainPageMaximum}{17}
\newcommand{\DFGSupplementPageMaximum}{8}
\ifdfglegacy
  \newcommand{\DFGFormVersion}{DFG form 53.01 -- 09/22}
\else
  \newcommand{\DFGFormVersion}{\DFGFormLabel\ -- \DFGProjectDescriptionRevision}
\fi
\newcommand{\DFGMaximumLabel}{max.}
\newcommand{\DFGPageMaximum}{\DFGMainPageMaximum}

\newcommand{\DFGDocumentTitle}{Project Description -- Project Proposals}
\newcommand{\DFGApplicantName}{[First name, last name, city]}
\newcommand{\DFGApplicantBirthNationality}{}
\newcommand{\DFGApplicantAffiliation}{}
\newcommand{\DFGApplicantContact}{}
\newcommand{\DFGProjectTitle}{[Project title]}
\newcommand{\DFGKeywords}{}

\newcommand{\DFGSetDocumentTitle}[1]{\renewcommand{\DFGDocumentTitle}{#1}}
\newcommand{\DFGSetApplicantName}[1]{\renewcommand{\DFGApplicantName}{#1}}
\newcommand{\DFGSetApplicants}[1]{\DFGSetApplicantName{#1}}
\newcommand{\DFGSetApplicantBirthNationality}[1]{\renewcommand{\DFGApplicantBirthNationality}{#1}}
\newcommand{\DFGSetApplicantAffiliation}[1]{\renewcommand{\DFGApplicantAffiliation}{#1}}
\newcommand{\DFGSetApplicantContact}[1]{\renewcommand{\DFGApplicantContact}{#1}}
\newcommand{\DFGSetProjectTitle}[1]{\renewcommand{\DFGProjectTitle}{#1}}
\newcommand{\DFGSetKeywords}[1]{\renewcommand{\DFGKeywords}{#1}}
\newcommand{\DFGSetFormLabel}[1]{\renewcommand{\DFGFormLabel}{#1}}
\newcommand{\DFGSetProjectDescriptionRevision}[1]{\renewcommand{\DFGProjectDescriptionRevision}{#1}}
\newcommand{\DFGSetProposalInstructionsRevision}[1]{\renewcommand{\DFGProposalInstructionsRevision}{#1}}
\newcommand{\DFGSetMainPageMaximum}[1]{\renewcommand{\DFGMainPageMaximum}{#1}}
\newcommand{\DFGSetSupplementPageMaximum}[1]{\renewcommand{\DFGSupplementPageMaximum}{#1}}

\newcommand{\DFGHeaderContent}{%
  \ifdfglegacy
    \fontsize{8.7pt}{10.4pt}\selectfont
    \makebox[\textwidth][l]{%
      \raisebox{-3.08pt}{\makebox[\dimexpr\textwidth-4mm\relax]{\DFGFormVersion\hfill page \thepage\ of \DFGMaximumLabel\ \DFGPageMaximum}}%
    }%
  \else
    \fontsize{8.5pt}{10.2pt}\selectfont
    \makebox[\textwidth][l]{%
      \raisebox{-3.08pt}{\makebox[\dimexpr\textwidth-5mm\relax]{\DFGFormVersion\hfill page \thepage\ of \DFGMaximumLabel\ \DFGPageMaximum}}%
    }%
  \fi
}

\newcommand{\DFGFooterContent}{%
  \makebox[\textwidth][l]{%
    \begin{minipage}[b]{0.76\textwidth}
      \fontsize{8.7pt}{12pt}\selectfont
      {\color{DFGBlue}Deutsche Forschungsgemeinschaft}\par
      Kennedyallee 40 · 53175 Bonn · postal address: 53170 Bonn\par
      phone: + 49 228 885-1 · fax: + 49 228 885-2777 · postmaster@dfg.de · www.dfg.de
    \end{minipage}%
    \hfill
    \begin{minipage}[b]{0.20\textwidth}
      \raggedleft\raisebox{16pt}{\color{DFGBlue}\fontsize{32pt}{32pt}\selectfont\bfseries DFG\hspace*{14pt}}
    \end{minipage}%
  }%
}

\fancypagestyle{dfgplain}{%
  \fancyhf{}
  \fancyhead[C]{\DFGHeaderContent}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

\fancypagestyle{dfgfirst}{%
  \fancyhf{}
  \fancyhead[C]{\DFGHeaderContent}
  \fancyfoot[C]{\raisebox{16mm}[0pt][0pt]{\DFGFooterContent}}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

\pagestyle{dfgplain}

\newif\ifdfgsupplementstarted
\dfgsupplementstartedfalse
\newcount\dfgmainpagecount

\newcommand{\DFGStartMainMatter}{%
  \clearpage
  \dfgsupplementstartedfalse
  \ifdfglegacy
    \renewcommand{\DFGFormVersion}{DFG form 53.01 -- 09/22}%
    \renewcommand{\DFGMaximumLabel}{max.}%
  \fi
  \setcounter{page}{1}%
  \renewcommand{\DFGPageMaximum}{\DFGMainPageMaximum}%
  \pagestyle{dfgplain}%
}

\newcommand{\DFGMakeProposalHeader}{%
  \thispagestyle{dfgfirst}%
  \enlargethispage{-27mm}%
  \begingroup
  \setlength{\parskip}{0pt}%
  \fontsize{11pt}{15.3pt}\selectfont
  {\bfseries \DFGDocumentTitle\par}
  \vspace{14.7pt}
  {\bfseries \DFGApplicantName\par}
  \ifdefempty{\DFGApplicantBirthNationality}{}{\DFGApplicantBirthNationality\par}%
  \ifdefempty{\DFGApplicantAffiliation}{}{\DFGApplicantAffiliation\par}%
  \ifdefempty{\DFGApplicantContact}{}{\DFGApplicantContact\par}%
  \vspace{18pt}
  {\bfseries \DFGProjectTitle\par}
  \vspace{22.7pt}
  \hrule height 0.5pt
  {\bfseries Project Description\par}
  \endgroup
  \vspace{10pt}
}

\newcommand{\DFGPageLimitNotice}[1]{%
  \par\begingroup
  \fontsize{9pt}{12.3pt}\selectfont\itshape #1\par
  \endgroup
}
\newcommand{\DFGMainPageLimitNotice}{%
  \DFGPageLimitNotice{Sections 1--3 must not exceed \DFGMainPageMaximum\ pages in total.}%
}
\newcommand{\DFGSupplementPageLimitNotice}{%
  \DFGPageLimitNotice{Section 4 et seq. must not exceed \DFGSupplementPageMaximum\ pages.}%
}

\newcommand{\DFGStartSupplement}{%
  \clearpage
  \ifdfglegacy\else
    \dfgmainpagecount=\value{page}\relax
    \advance\dfgmainpagecount by -1\relax
    \ifnum\dfgmainpagecount>\DFGMainPageMaximum\relax
      \ClassError{dfgproposal}{Sections 1--3 exceed the \DFGMainPageMaximum-page limit}{Shorten sections 1--3 before continuing.}%
    \else
      \ClassInfo{dfgproposal}{Sections 1--3 use \the\dfgmainpagecount\space of \DFGMainPageMaximum\ pages}%
    \fi
  \fi
  \ifdfglegacy
    % The supplied Word file changes punctuation in the repeated header when
    % the supplementary eight-page section begins; preserve that quirk only
    % in the historical benchmark mode.
    \renewcommand{\DFGFormVersion}{DFG-form 53-01 -- 09/22}%
    \renewcommand{\DFGMaximumLabel}{max}%
  \fi
  \setcounter{page}{1}%
  \renewcommand{\DFGPageMaximum}{\DFGSupplementPageMaximum}%
  \dfgsupplementstartedtrue
  \pagestyle{dfgplain}%
  \thispagestyle{dfgfirst}%
  \enlargethispage{-27mm}%
}

\newcommand{\DFGHeadingBase}[3]{%
  \par
  \begingroup
  \noindent\RaggedRight\bfseries
  \makebox[#1][l]{#2}#3\par
  \endgroup
  \nobreak\vspace{0pt}%
}
\newcommand{\DFGStackedHeadingBase}[3]{%
  \par\vspace{-\parskip}\vspace{0.67pt}%
  \begingroup
  \noindent\RaggedRight\bfseries
  \makebox[#1][l]{#2}#3\par
  \endgroup
  \nobreak\vspace{0pt}%
}
\ifdfglegacy
  \newcommand{\DFGSection}[2]{\DFGHeadingBase{21pt}{#1}{#2}}
  \newcommand{\DFGSubsection}[2]{\DFGHeadingBase{29pt}{#1}{#2}}
  \newcommand{\DFGSubsubsection}[2]{\DFGHeadingBase{36pt}{#1}{#2}}
  \newcommand{\DFGDeepSubsubsection}[2]{\DFGHeadingBase{44pt}{#1}{#2}}
  \newcommand{\DFGStackedSection}[2]{\DFGStackedHeadingBase{21pt}{#1}{#2}}
  \newcommand{\DFGStackedSubsection}[2]{\DFGStackedHeadingBase{29pt}{#1}{#2}}
  \newcommand{\DFGStackedSubsubsection}[2]{\DFGStackedHeadingBase{36pt}{#1}{#2}}
  \newcommand{\DFGStackedDeepSubsubsection}[2]{\DFGStackedHeadingBase{44pt}{#1}{#2}}
\else
  \newcommand{\DFGSection}[2]{\DFGHeadingBase{21.6pt}{#1}{#2}}
  \newcommand{\DFGSubsection}[2]{\DFGHeadingBase{28.9pt}{#1}{#2}}
  \newcommand{\DFGSubsubsection}[2]{\DFGHeadingBase{36pt}{#1}{#2}}
  \newcommand{\DFGDeepSubsubsection}[2]{\DFGHeadingBase{43.2pt}{#1}{#2}}
  \newcommand{\DFGStackedSection}[2]{\DFGStackedHeadingBase{21.6pt}{#1}{#2}}
  \newcommand{\DFGStackedSubsection}[2]{\DFGStackedHeadingBase{28.9pt}{#1}{#2}}
  \newcommand{\DFGStackedSubsubsection}[2]{\DFGStackedHeadingBase{36pt}{#1}{#2}}
  \newcommand{\DFGStackedDeepSubsubsection}[2]{\DFGStackedHeadingBase{43.2pt}{#1}{#2}}
\fi
\newcommand{\DFGUnnumberedHeading}[1]{%
  \par\begingroup\noindent\RaggedRight\bfseries #1\par\endgroup\nobreak
}
\newcommand{\DFGStackedUnnumberedHeading}[1]{%
  \par\vspace{-\parskip}\vspace{0.67pt}%
  \begingroup\noindent\RaggedRight\bfseries #1\par\endgroup\nobreak
}

\newcommand{\DFGStartReferences}{%
  \par\begingroup
  \fontsize{9pt}{12.3pt}\selectfont
  \setlength{\parskip}{0pt}%
  \setlength{\parindent}{0pt}%
  \setlength{\emergencystretch}{4em}%
  \Urlmuskip=0mu plus 1mu\relax
  \sloppy
}
\newcommand{\DFGEndReferences}{\par\endgroup}

\newcommand{\DFGInstruction}[1]{%
  \ifdfgsubmission
    \ClassError{dfgproposal}{Unresolved template guidance remains}{Remove or replace every \string\DFGInstruction before submission.}%
  \else
    \par\begingroup\color{black!62}\small\itshape
      [Template guidance: #1]\par
    \endgroup
  \fi
}

\newcommand{\DFGDecisionRequired}[2]{%
  \ifdfgsubmission
    \ClassError{dfgproposal}{Unresolved decision gate #1 remains}{Resolve the decision and remove the \string\DFGDecisionRequired command.}%
  \else
    \par\noindent\textbf{[DECISION REQUIRED #1:} #2\textbf{]}\par
  \fi
}

\newcommand{\DFGNotApplicable}[1]{%
  \par\noindent\textit{Not applicable.}\ifstrempty{#1}{}{ #1}\par
}
\newcommand{\DFGNotRequested}[1]{%
  \par\noindent\textit{Not requested.}\ifstrempty{#1}{}{ #1}\par
}
\ifdfglegacy
  \newenvironment{DFGfundtable}{%
    \small\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.08}%
  }{\normalsize}
\else
  \newenvironment{DFGfundtable}{%
    \normalsize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.08}%
  }{\normalsize}
\fi

\newcommand{\DFGCheckSupplementPageLimit}{%
  \ifdfglegacy\else
    \ifdfgsupplementstarted
      \ifnum\value{page}>\DFGSupplementPageMaximum\relax
        \ClassError{dfgproposal}{Section 4 onward exceeds the \DFGSupplementPageMaximum-page limit}{Shorten section 4 onward before submission.}%
      \else
        \ClassInfo{dfgproposal}{Section 4 onward uses \thepage\space of \DFGSupplementPageMaximum\ pages}%
      \fi
    \else
      \ClassWarningNoLine{dfgproposal}{\string\DFGStartSupplement was not called; the 8-page section could not be checked}%
    \fi
  \fi
}

\AtBeginDocument{%
  \normalsize\justifying
  \setlength{\JustifyingParindent}{0pt}\setlength{\parindent}{0pt}%
  \hypersetup{%
    pdftitle={\DFGProjectTitle},
    pdfauthor={\DFGApplicantName},
    pdfsubject={\DFGDocumentTitle},
    pdfkeywords={\DFGKeywords},
    pdfcreator={LaTeX with dfgproposal class}
  }%
}
\AtEndDocument{\DFGCheckSupplementPageLimit}
