\NeedsTeXFormat{LaTeX2e}[2020-10-01]
\ProvidesClass{dfgproposal}[2026/09/10 v2.0 DFG Research Grants starter]
% Maintainer: Dr. Awanish Pratap Singh. MIT licensed; unofficial template.
\newif\ifdfgsubmission
\newif\ifdfggerman
\newif\ifdfgportable
\newif\ifdfgmanualbib
\DeclareOption{current}{}
\DeclareOption{guidance}{\dfgsubmissionfalse}
\DeclareOption{draft}{\dfgsubmissionfalse}
\DeclareOption{english}{\dfggermanfalse}
\DeclareOption{german}{\dfggermantrue}
\DeclareOption{portable}{\dfgportabletrue}
\DeclareOption{manualbibliography}{\dfgmanualbibtrue}
\DeclareOption{submission}{\dfgsubmissiontrue}
\DeclareOption{dfg000}{\ClassError{dfgproposal}{Historical dfg000 mode is not supported in v2}{Use a pinned v1 checkout for historical reproduction; see docs/MIGRATION.md.}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ExecuteOptions{english,draft}
\ProcessOptions\relax
\ifdefined\DFGForceSubmission\dfgsubmissiontrue\fi
\LoadClass[11pt,a4paper]{article}
\@removeelement{german}{\@classoptionslist}\@classoptionslist
\@removeelement{english}{\@classoptionslist}\@classoptionslist
\@removeelement{draft}{\@classoptionslist}\@classoptionslist
\@removeelement{guidance}{\@classoptionslist}\@classoptionslist
\@removeelement{submission}{\@classoptionslist}\@classoptionslist
\@removeelement{portable}{\@classoptionslist}\@classoptionslist
\@removeelement{current}{\@classoptionslist}\@classoptionslist
\@removeelement{manualbibliography}{\@classoptionslist}\@classoptionslist
\ifdefined\@raw@classoptionslist
  \@removeelement{draft}{\@raw@classoptionslist}\@raw@classoptionslist
  \@removeelement{german}{\@raw@classoptionslist}\@raw@classoptionslist
  \@removeelement{english}{\@raw@classoptionslist}\@raw@classoptionslist
\fi
\RequirePackage{iftex}
\ifdfgsubmission
  \ifdfgportable\ClassError{dfgproposal}{Portable fonts are drafting-only}{Remove portable and use Arial for submission.}\fi
\fi
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage{helvet}
  \renewcommand{\familydefault}{\sfdefault}
  \def\DFGResolvedFont{Helvetica}
  \ifdfgsubmission\ClassError{dfgproposal}{pdfLaTeX is drafting-only}{Use XeLaTeX or LuaLaTeX with Arial.}\fi
\else
  \RequirePackage{fontspec}
  \def\DFGChoosePortableFont{%
    \IfFontExistsTF{Liberation Sans}{\def\DFGResolvedFont{Liberation Sans}}{\def\DFGResolvedFont{TeX Gyre Heros}}%
  }
  \ifdfgportable\DFGChoosePortableFont\else
    \IfFontExistsTF{Arial}{\def\DFGResolvedFont{Arial}}{\DFGChoosePortableFont
      \ifdfgsubmission\ClassError{dfgproposal}{Arial is unavailable}{Install Arial lawfully or use an Arial-capable environment. Draft builds may use a fallback.}\fi}%
  \fi
  \setmainfont{\DFGResolvedFont}[Ligatures=TeX]
  \setsansfont{\DFGResolvedFont}[Ligatures=TeX]
\fi
\ifdfggerman\RequirePackage[ngerman]{babel}\else\RequirePackage[english]{babel}\fi
\RequirePackage[a4paper,top=25mm,left=25mm,right=20mm,bottom=15mm,headheight=12.2pt,headsep=9mm,footskip=12mm]{geometry}
\RequirePackage[final]{graphicx,microtype}
\RequirePackage{xcolor,fancyhdr,ragged2e,etoolbox}
\RequirePackage{amsmath,amssymb,enumitem}
\RequirePackage{array,booktabs,longtable,tabularx,colortbl}
\RequirePackage{caption,needspace,xurl}
\RequirePackage[final,hidelinks,unicode,hypertexnames=false]{hyperref}
\ifdfgmanualbib\else\RequirePackage{dfg-bibliography}\fi
\definecolor{DFGBlue}{HTML}{00549F}
\renewcommand\normalsize{%
  \@setfontsize\normalsize{11pt}{14.4pt}%
  \abovedisplayskip 7pt plus 2pt minus 2pt\belowdisplayskip 7pt plus 2pt minus 2pt
  \abovedisplayshortskip 3pt plus 2pt\belowdisplayshortskip 5pt plus 2pt minus 2pt}
\renewcommand\small{\@setfontsize\small{11pt}{14.4pt}}
\renewcommand\footnotesize{\@setfontsize\footnotesize{11pt}{14.4pt}}
\normalsize
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt plus 1pt minus 1pt}
\setlist{nosep,leftmargin=5mm,topsep=2pt}
\justifying\setlength{\JustifyingParindent}{0pt}
\setlength{\emergencystretch}{2em}
\urlstyle{same}
\captionsetup{font=normalsize,labelfont=bf,labelsep=period,skip=3pt}

% The profile is generated once; authors do not need a generator.
\newcommand{\DFGDeclareHeading}[5]{%
  \expandafter\def\csname dfgnum@#1\endcsname{#2}%
  \expandafter\def\csname dfgtitle@#1\endcsname{\ifdfggerman #4\else #3\fi}%
  \expandafter\def\csname dfgid@#2\endcsname{#1}%
  \expandafter\def\csname dfgdepth@#1\endcsname{#5}%
}
\input{dfg-research-grants-2026-09.def}
\newcommand{\DFGProjectDescriptionRevision}{\DFGProfileRevision}
\newcommand{\DFGProposalInstructionsRevision}{09/26}
\newcommand{\DFGFormLabel}{\ifdfggerman DFG-Vordruck 53.01\else DFG form 53.01\fi}
\newcommand{\DFGFormVersion}{\DFGFormLabel\ -- \DFGProjectDescriptionRevision}
\newcommand{\DFGPageMaximum}{\DFGMainPageMaximum}
\newcommand{\DFGDocumentTitle}{\ifdfggerman Beschreibung des Vorhabens -- Projektanträge\else Project Description -- Project Proposals\fi}
\newcommand{\DFGMainMatterTitle}{\ifdfggerman Beschreibung des Vorhabens\else Project Description\fi}
\newcommand{\DFGProjectTitle}{[Project title]}
\newcommand{\DFGApplicantName}{[Applicant name]}
\newcommand{\DFGKeywords}{}
\newcommand{\DFGSetProjectTitle}[1]{\renewcommand{\DFGProjectTitle}{#1}}
\newcommand{\DFGSetApplicantName}[1]{\renewcommand{\DFGApplicantName}{#1}\def\dfgapplicantcount{1}}
\newcommand{\DFGSetApplicants}[1]{\DFGSetApplicantName{#1}}
\newcommand{\DFGSetKeywords}[1]{\renewcommand{\DFGKeywords}{#1}}
\newcommand{\DFGSetDocumentTitle}[1]{\renewcommand{\DFGDocumentTitle}{#1}}
\newcommand{\DFGSetMainMatterTitle}[1]{\renewcommand{\DFGMainMatterTitle}{#1}}
\newcommand{\DFGSetFormLabel}[1]{\renewcommand{\DFGFormLabel}{#1}}
\newcommand{\DFGSetProjectDescriptionRevision}[1]{\renewcommand{\DFGProjectDescriptionRevision}{#1}}
\newcommand{\DFGSetProposalInstructionsRevision}[1]{\renewcommand{\DFGProposalInstructionsRevision}{#1}}
\newcommand{\DFGSetMainPageMaximum}[1]{\renewcommand{\DFGMainPageMaximum}{#1}}
\newcommand{\DFGSetSupplementPageMaximum}[1]{\renewcommand{\DFGSupplementPageMaximum}{#1}}
\def\dfgapplicantcount{0}
\newcommand{\DFGAddApplicant}[3]{%
  \ifcsname dfgapplicant@#1\endcsname
    \ClassError{dfgproposal}{Duplicate applicant ID #1}{Use a distinct ID for each applicant.}%
  \fi
  \expandafter\def\csname dfgapplicant@#1\endcsname{#2}%
  \ifnum\dfgapplicantcount=0\renewcommand{\DFGApplicantName}{#2, #3}%
  \else\appto\DFGApplicantName{; #2, #3}\fi
  \edef\dfgapplicantcount{\number\numexpr\dfgapplicantcount+1\relax}%
}
\newcommand{\DFGApplicantWork}[1]{%
  \ifcsname dfgapplicant@#1\endcsname
    \DFGUnnumberedHeading{\ifdfggerman Antragsteller*in:\else Applicant:\fi\space\csname dfgapplicant@#1\endcsname}%
  \else\ClassError{dfgproposal}{Unknown applicant ID #1}{Add this ID in the metadata file.}\fi
}

% Effective execution trace: inactive or duplicated headings cannot masquerade
% as the required structure just by appearing in a source file.
\newwrite\dfgaudit
\newcommand{\DFGAudit}[1]{\immediate\write\dfgaudit{#1}}
\newcounter{dfgheading}
\newcount\dfgmainpages
\newcount\dfgsupplementpages
\newif\ifdfgsupplementstarted
\newif\ifdfgmainstarted
\newif\ifdfgethicsdeclared
\AddToHook{shipout/before}{%
  \ifdfgmainstarted
    \ifdfgsupplementstarted\global\advance\dfgsupplementpages by 1
    \else\global\advance\dfgmainpages by 1\fi
  \fi
}
\newcommand{\DFGPrintHeading}[2]{%
  \par\addvspace{7pt}\Needspace{5\baselineskip}%
  \refstepcounter{dfgheading}\def\@currentlabel{#1}%
  \begingroup\RaggedRight\bfseries
  \settowidth{\@tempdima}{#1\quad}%
  \hangindent=\@tempdima\hangafter=1\noindent #1\quad #2\par
  \endgroup\nobreak\vspace{1pt}\nobreak
}
\newcommand{\DFGHeading}[1]{%
  \ifcsname dfgnum@#1\endcsname
    \edef\dfgthisnumber{\csname dfgnum@#1\endcsname}%
    \DFGAudit{heading|#1|\dfgthisnumber}%
    \DFGPrintHeading{\dfgthisnumber}{\csname dfgtitle@#1\endcsname}%
    \edef\@currentlabel{\dfgthisnumber}\label{dfg:#1}%
    \pdfbookmark[\csname dfgdepth@#1\endcsname]{\dfgthisnumber\space\csname dfgtitle@#1\endcsname}{dfg.#1}%
  \else\ClassError{dfgproposal}{Unknown heading ID #1}{See the profile or docs/AUTHORING.md.}\fi
}
\newcommand{\DFGSection}[2]{\DFGAudit{legacy-heading|#1|\detokenize{#2}}\DFGPrintHeading{#1}{#2}}
\let\DFGSubsection\DFGSection
\let\DFGSubsubsection\DFGSection
\let\DFGDeepSubsubsection\DFGSection
\let\DFGStackedSection\DFGSection
\let\DFGStackedSubsection\DFGSection
\let\DFGStackedSubsubsection\DFGSection
\let\DFGStackedDeepSubsubsection\DFGSection
\newcommand{\DFGUnnumberedHeading}[1]{\par\Needspace{4\baselineskip}{\RaggedRight\bfseries #1\par}\nobreak}
\let\DFGStackedUnnumberedHeading\DFGUnnumberedHeading
\newcommand{\DFGWorkPackage}[2]{\DFGUnnumberedHeading{#1: #2}}
\newcommand{\DFGTodo}[1]{%
  \DFGAudit{todo|unresolved}%
  \ifdfgsubmission\ClassError{dfgproposal}{Unresolved writing prompt}{Replace every DFGTodo/DFGInstruction with your own text.}%
  \else\par{\color{black!65}\itshape #1\par}\fi
}
\let\DFGInstruction\DFGTodo
\newcommand{\DFGDecisionRequired}[2]{\DFGTodo{#1: #2}}
\newcommand{\DFGNotApplicable}[1]{\par\textit{\ifdfggerman Nicht zutreffend.\else Not applicable.\fi}\space #1\par}
\newcommand{\DFGNotRequested}[1]{\par\textit{\ifdfggerman Nicht beantragt.\else Not requested.\fi}\space #1\par}
\newcommand{\DFGEthicsStatement}[1]{%
  \dfgethicsdeclaredtrue\DFGAudit{ethics|#1}%
  \ifstrequal{#1}{yes}{\def\dfgethicsanswer{\ifdfggerman ja\else yes\fi}}{%
    \ifstrequal{#1}{no}{\def\dfgethicsanswer{\ifdfggerman nein\else no\fi}}{%
      \def\dfgethicsanswer{[\ifdfggerman bitte ausfüllen\else choose yes or no\fi]}%
      \DFGTodo{\ifdfggerman Prüfen Sie die Erforderlichkeit einer Ethikstellungnahme.\else Assess whether an ethics committee statement is required.\fi}%
    }%
  }%
  \par\ifdfggerman Die Stellungnahme einer Ethikkommission ist notwendig:\else A statement by an ethics committee is required:\fi\space\textbf{\dfgethicsanswer}\par
}
\newenvironment{DFGfundtable}{\normalsize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.15}}{}
\newcommand{\DFGStartReferences}{\par\begingroup\fontsize{9pt}{12.3pt}\selectfont\setlength{\parskip}{0pt}\sloppy}
\newcommand{\DFGEndReferences}{\par\endgroup}
\newcommand{\DFGPrintReferences}{%
  \DFGHeading{publications}\DFGStartReferences
  \ifdfgmanualbib\ClassError{dfgproposal}{Automatic references requested in manual mode}{Use DFGStartReferences and DFGEndReferences around your manual list.}%
  \else\renewcommand{\bibfont}{\fontsize{9pt}{12.3pt}\selectfont}\printbibliography[heading=none]\fi
  \DFGEndReferences
}
\newcommand{\DFGStartMainMatter}{%
  \clearpage\dfgmainstartedtrue\dfgsupplementstartedfalse
  \setcounter{page}{1}\renewcommand{\DFGPageMaximum}{\DFGMainPageMaximum}%
  \DFGAudit{boundary|main}%
  \ifdfgmanualbib\else\begin{refsection}\fi
}
\newcommand{\DFGStartSupplement}{%
  \ifdfgmanualbib\else\end{refsection}\fi
  \clearpage\dfgsupplementstartedtrue\setcounter{page}{1}%
  \renewcommand{\DFGPageMaximum}{\DFGSupplementPageMaximum}%
  \DFGAudit{boundary|supplement}\thispagestyle{dfgfirst}\enlargethispage{-27mm}%
}
\newcommand{\DFGHeaderContent}{%
  \fontsize{8.5pt}{10.2pt}\selectfont\DFGFormVersion\hfill
  \ifdfggerman Seite \thepage\ von max.\else page \thepage\ of max.\fi\space\DFGPageMaximum
}
\newcommand{\DFGFooterContent}{%
  \begin{minipage}[b]{.78\textwidth}\fontsize{8.7pt}{12pt}\selectfont
  {\color{DFGBlue}Deutsche Forschungsgemeinschaft}\par
  Kennedyallee 40 · 53175 Bonn · \ifdfggerman Postanschrift:\else postal address:\fi\space 53170 Bonn\par
  +49 228 885-1 · postmaster@dfg.de · www.dfg.de
  \end{minipage}\hfill{\color{DFGBlue}\fontsize{32pt}{32pt}\selectfont\bfseries DFG}%
}
\fancypagestyle{dfgplain}{\fancyhf{}\fancyhead[C]{\DFGHeaderContent}\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}}
\fancypagestyle{dfgfirst}{\fancyhf{}\fancyhead[C]{\DFGHeaderContent}\fancyfoot[C]{\raisebox{16mm}[0pt][0pt]{\DFGFooterContent}}\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}}
\pagestyle{dfgplain}
\newcommand{\DFGMakeProposalHeader}{%
  \thispagestyle{dfgfirst}\enlargethispage{-27mm}%
  {\bfseries\DFGDocumentTitle\par}\vspace{9pt}
  {\bfseries\DFGApplicantName\par}\vspace{12pt}
  {\bfseries\DFGProjectTitle\par}\vspace{12pt}\hrule
  {\bfseries\DFGMainMatterTitle\par}\vspace{6pt}%
}
\newcommand{\DFGPageLimitNotice}[1]{\par{\fontsize{9pt}{12pt}\selectfont\itshape #1\par}}
\newcommand{\DFGMainPageLimitNotice}{\DFGPageLimitNotice{\ifdfggerman Kapitel 1--3, insgesamt maximal 17 Seiten.\else Sections 1--3 must not exceed 17 pages in total.\fi}}
\newcommand{\DFGSupplementPageLimitNotice}{\DFGPageLimitNotice{\ifdfggerman Kapitel 4ff., insgesamt maximal 8 Seiten.\else Section 4 et seq. must not exceed 8 pages.\fi}}
\AtBeginDocument{%
  \immediate\openout\dfgaudit=\jobname.dfg-audit
  \DFGAudit{profile|\DFGProfileID}\DFGAudit{language|\ifdfggerman german\else english\fi}%
  \DFGAudit{mode|\ifdfgsubmission submission\else draft\fi}\DFGAudit{font|\DFGResolvedFont}%
  \DFGAudit{limits|\DFGMainPageMaximum|\DFGSupplementPageMaximum}%
  \normalsize\justifying
  \hypersetup{pdftitle={\DFGProjectTitle},pdfauthor={\DFGApplicantName},pdfsubject={\DFGDocumentTitle},pdfkeywords={\DFGKeywords},pdfcreator={dfgproposal v2.0}}%
}
\AtEndDocument{%
  \clearpage % Flush final floats before counting shipped pages.
  \DFGAudit{pages|\the\dfgmainpages|\the\dfgsupplementpages}%
  \ifdfgethicsdeclared\else\DFGAudit{ethics|missing}\fi
  \ifnum\dfgmainpages>\DFGMainPageMaximum
    \ifdfgsubmission\ClassError{dfgproposal}{Main part exceeds page limit}{Shorten sections 1--3.}\else\ClassWarningNoLine{dfgproposal}{Main part exceeds page limit}\fi\fi
  \ifnum\dfgsupplementpages>\DFGSupplementPageMaximum
    \ifdfgsubmission\ClassError{dfgproposal}{Supplement exceeds page limit}{Shorten sections 4 onward.}\else\ClassWarningNoLine{dfgproposal}{Supplement exceeds page limit}\fi\fi
  \DFGAudit{complete|yes}\immediate\closeout\dfgaudit
}
