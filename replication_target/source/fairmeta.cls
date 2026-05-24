

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fairmeta}
\LoadClassWithOptions{article}

\RequirePackage[top=2.25cm, bottom=2.5cm, left=2.5cm, right=2.5cm, columnsep=0.65cm]{geometry}
\RequirePackage{microtype}
\RequirePackage{placeins}
\RequirePackage{hyphenat}
\RequirePackage{setspace}
\RequirePackage{parskip}
\RequirePackage{amsmath}
\RequirePackage[latin, english]{babel}
\RequirePackage{lipsum}
\RequirePackage{etoolbox}
\RequirePackage{array}
\RequirePackage{siunitx}
\sisetup{detect-weight=true,detect-family=true,group-minimum-digits=4}
\RequirePackage{iftex}

\DisableLigatures[f]{family=sf*} 

\RequirePackage{graphicx}
\RequirePackage{subcaption}

\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{tabularx}
\RequirePackage{nicematrix}
\RequirePackage{multirow}
\RequirePackage{bm}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}m{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}m{#1}}
\newcommand{\nm}[1]{#1}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}

\RequirePackage[most]{tcolorbox}
\RequirePackage{xcolor}
\definecolor{metablue}{HTML}{1877F2}
\definecolor{metafg}{HTML}{1F2A33}
\definecolor{metafgsoft}{HTML}{5C6670}
\definecolor{metabg}{HTML}{F1F4F7}
\definecolor{metaedge}{HTML}{DCE6F5}
\definecolor{apricotglaze}{HTML}{F7EBDD}
\colorlet{tablewarmrow}{apricotglaze!28!white}
\colorlet{tablewarmhead}{apricotglaze!60!white}

\RequirePackage{hyperref}
\RequirePackage[noabbrev,nameinlink]{cleveref}
\hypersetup{
  colorlinks,
  linkcolor=metablue,
  citecolor=metablue,
  urlcolor=metablue
}

\RequirePackage{amsmath,amssymb,mathtools}
\numberwithin{equation}{section}

\crefname{figure}{Fig.}{Figs.}
\Crefname{figure}{Figure}{Figures}
\crefname{table}{Table}{Tables}
\Crefname{table}{Table}{Tables}
\crefname{section}{Sec.}{Secs.}
\Crefname{section}{Section}{Sections}
\crefname{equation}{Eq.}{Eqs.}
\Crefname{equation}{Equation}{Equations}

\newcommand{\Secref}[1]{\Cref{#1}}% Section
\newcommand{\secref}[1]{\cref{#1}}% Sec.
\newcommand{\Figref}[1]{\Cref{#1}}% Figure
\newcommand{\figref}[1]{\cref{#1}}% Fig.
\newcommand{\Tabref}[1]{\Cref{#1}}% Table
\newcommand{\tabref}[1]{\cref{#1}}% Table (lower)
\newcommand{\Eqref}[1]{\cref{#1}}% Eq.

\crefname{section}{Section}{Sections}
\Crefname{section}{Section}{Sections}
\crefname{figure}{Figure}{Figures}
\Crefname{figure}{Figure}{Figures}
\crefname{table}{Table}{Tables}
\Crefname{table}{Table}{Tables}
\crefname{equation}{Eq.}{Eqs.}
\Crefname{equation}{Eq.}{Eqs.}

\crefformat{equation}{Eq.~(#2#1#3)}
\Crefformat{equation}{Equation~(#2#1#3)}
\crefname{figure}{Fig.}{Figs.}
\Crefname{figure}{Figure}{Figures}
\crefname{table}{Tab.}{Tabs.}
\Crefname{table}{Table}{Tables}
\crefname{section}{Sec.}{Secs.}
\Crefname{section}{Section}{Sections}
\crefname{appendix}{App.}{Apps.}
\Crefname{appendix}{Appendix}{Appendices}

\RequirePackage[round,authoryear]{natbib}
\def\bibfont{\small}

\RequirePackage{titlesec}
\titleformat*{\paragraph}{\itshape\color{metafg}}
\titleformat*{\section}{\Large\sffamily\bfseries\color{metafg}}
\titleformat*{\subsection}{\large\sffamily\bfseries\color{metafg}}
\titleformat*{\subsubsection}{\normalsize\sffamily\bfseries\color{metafg}}
\DeclareTextFontCommand{\textbf}{\bfseries\sffamily}

\RequirePackage{caption}
\DeclareCaptionLabelSeparator{custom}{}
\DeclareCaptionFormat{custom}{{\sffamily\textbf{\color{metafg}#1 #2}} {\color{metafg}#3}}
\captionsetup{singlelinecheck=false,format=custom,labelsep=custom,font=small,skip=6pt}
\captionsetup[sub]{singlelinecheck=true,format=custom,labelsep=custom,font=small,skip=4pt}

\RequirePackage{mathtools} % loads amsmath
\DeclarePairedDelimiter{\abs}{\lvert}{\rvert}
\DeclarePairedDelimiter{\norm}{\lVert}{\rVert}
\DeclarePairedDelimiter{\paren}{\lparen}{\rparen}
\DeclarePairedDelimiter{\bracket}{\lbrack}{\rbrack}
\DeclarePairedDelimiter{\bracep}{\lbrace}{\rbrace}

\newenvironment{tighttable}{\begingroup\small\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.15}\centering}{\par\endgroup}
\newenvironment{smallschemetable}[2]{%
  \begin{table}[htbp]
  \centering
  \small
  \caption{#1}
  \label{#2}
}{\end{table}}

\renewcommand*\ttdefault{cmvtt}

\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage{CJKutf8}
  \AtBeginDocument{\begin{CJK*}{UTF8}{gbsn}}
  \AtEndDocument{\end{CJK*}}

  \DeclareFontFamily{T1}{optimistic}{}
  \DeclareFontShape{T1}{optimistic}{m}{n}{<-> s * [0.88] assets/optimistic}{}
  \DeclareFontShape{T1}{optimistic}{b}{n}{<-> s * [0.88] assets/optimistic}{}
  \pdfmapline{+optimistic < assets/Optimistic.ttf <T1-WGL4.enc}
  \renewcommand{\sfdefault}{optimistic}
\else
  \RequirePackage{fontspec}
  \defaultfontfeatures{Ligatures=TeX}
  \setsansfont[Path=assets/,Extension=.ttf]{Optimistic}
  \ifXeTeX
    \RequirePackage{xeCJK}
  \fi
\fi

\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect 
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}

\newcommand\authorlist{}
\newcommand\authorformat[2][]{{\sffamily\bfseries\color{metafg} #2{$^{#1}$}}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\makeatletter
\newcommand{\authorbreak}{\g@addto@macro\authorlist{\unskip\par\vspace{0.3cm}}}
\makeatother

\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{{
  \normalsize
  \raisebox{0.22ex}{\scalebox{0.92}{#1}}\kern0.18em{\color{metafg}#2}
}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\contributionlist{}
\newcommand\contributionformat[2][]{{\normalsize\color{metafg}(#1~#2)}}
\newcommand\contribution[2][]{\addtolist[#1]{#2}{\contributionlist}{\contributionformat}{, }}

\newcommand\metadatalist{}
\newcommand\metadataformat[2][]{{\small {\sffamily\bfseries\color{metafg} #1:} {\color{metafgsoft}#2}}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

\renewcommand{\abstract}[1]{\def\abstractlist{{\color{metafg} #1}}}
\newcommand{\email}[1]{\href{mailto:#1}{\texttt{#1}}}

\renewcommand\date[1]{\metadata[Date]{#1}}
\newcommand\correspondence[1]{\metadata[Correspond]{#1}}

\renewcommand{\footnoterule}{%
  \kern -3pt
  {\color{metaedge}\hrule width 0.35\columnwidth height 0.4pt}
  \kern 2.6pt
}

\renewcommand{\title}[1]{\newcommand{\titlelist}{{\fontsize{29}{33}\selectfont\sffamily\bfseries\color{metafg} #1}}}

\newcommand{\beginappendix}{\appendix{\huge\sffamily Appendix\par}}

\newlength{\TitleAuthorSpace}
\setlength{\TitleAuthorSpace}{0.46cm} % space between title and author names
\newlength{\MetaLogoWidth}
\setlength{\MetaLogoWidth}{2cm} % width of the Meta logo in title box
\newlength{\MetaLogoXShift}
\setlength{\MetaLogoXShift}{1.2cm} % how much to move logo left from right edge
\newlength{\MetaLogoYShift}
\setlength{\MetaLogoYShift}{0.8cm} % how much to move logo up from bottom edge

\newcommand{\mymaketitle}{%
  \tcbset{enhanced,colframe=metaedge,boxrule=0.35pt}
  \tcbset{left=0.5cm}
  \tcbset{right=0.5cm}
  \tcbset{top=0.45cm}
  \tcbset{bottom=0.35cm}
  \tcbset{arc=12pt}
  \tcbset{colback=metabg}
  \tcbset{interior style={shade,shading angle=315,left color=white!96!metabg,right color=metablue!4!orange!3!metabg}}
  \tcbset{before skip=0pt}
  \tcbset{grow to left by=1.5pt}
  \tcbset{grow to right by=1.5pt}
  \tcbset{overlay={\node[
    anchor=south east,
    at= (frame.south east),
    xshift=-\MetaLogoXShift,
    yshift=\MetaLogoYShift] {\includegraphics[width=\MetaLogoWidth]{assets/logometa.pdf}};}}
  \begin{tcolorbox}
    \setlength{\parindent}{0cm}
    \setlength{\parskip}{0.5cm}
    {
      \setlength{\parskip}{0cm}
      \raggedright
      \nohyphens
      {
        \centering
        \vspace*{0.12cm}
        \setstretch{1.618}
        \titlelist\par
      }
      \vskip \TitleAuthorSpace
      \authorlist\par
      \vskip 0.26cm
      {\centering \affiliationlist\hspace{0.45em}\contributionlist\par}
    }
    \abstractlist\par
    \vskip 0.3cm
    {
      \setlength{\parskip}{0cm}
      \ifdefempty{\metadatalist}{\vspace*{0.65cm}}{\metadatalist\par}
    }
  \end{tcolorbox}
  \tcbset{reset}
  \FloatBarrier
}

\if@twocolumn%
\renewcommand{\maketitle}{
\twocolumn[%
  \mymaketitle
  \vskip 0.38cm
]
}%
\else%
\renewcommand{\maketitle}{
  \mymaketitle
}%
\fi
