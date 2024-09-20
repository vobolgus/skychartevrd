% -============================-
%  Based on Astroedu Lab Class
% -============================-

%\documentclass[]{SAS-class-a4}
%
%\begin{document}
%
%\thispagestyle{firstpagestyle}
%\newgeometry{left = 1in, right = 1in, top = 0.75in, textheight = 22.5cm}
%\afterpage{\aftergroup\restoregeometry}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{SAS-class-a4}[2022-09-30 SAS Personal Template, v1.0]
\LoadClass[a4paper, 10pt]{extarticle}

% Characters and language
\RequirePackage{cmap}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[english, russian]{babel}
\RequirePackage{textcomp}

% Geometry and spacing
\RequirePackage[margin=1in]{geometry}
    \setlength\headsep{0.25in}
\RequirePackage[onehalfspacing]{setspace}
\setlength{\parindent}{0ex}
% \setlength{\parskip}{1ex plus .5ex minus .3ex}
\setlength{\skip\footins}{.5cm}

% Maths
\RequirePackage{mathtools}
% 	\mathtoolsset{showonlyrefs}
\RequirePackage[all,warning]{onlyamsmath}
    \AtBeginDocument{\catcode`\$=3}
\RequirePackage{mathrsfs}
\RequirePackage{cancel}
\RequirePackage{marvosym}
\RequirePackage{amssymb, wasysym}
\RequirePackage{icomma}

% Graphics
\RequirePackage{color}
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{wrapfig}
	\setlength{\intextsep}{0pt}
\RequirePackage{tikz}
    \RequirePackage{tikz-3dplot}
    \RequirePackage{tkz-fct}  
	\RequirePackage{tkz-euclide}
	\usetikzlibrary{calc}
	\usetikzlibrary{positioning}
	\usetikzlibrary{patterns,angles,quotes}
    \usetikzlibrary{backgrounds,shapes,arrows,snakes,fit}
    \usetikzlibrary{intersections}
    \usetikzlibrary{matrix,fit}
    \usetikzlibrary{decorations.pathreplacing,tikzmark}
\RequirePackage{pgfplots}
    \pgfplotsset{compat=newest}
    \usepgfplotslibrary{polar}
    
% Decorations
\RequirePackage{todonotes}
\RequirePackage{tcolorbox}
\RequirePackage{mdframed}
    \newmdenv[
        topline=false,
        bottomline=false,
        rightline=false,
        skipabove=\topsep / 2,
        skipbelow=\topsep / 2
        ]{leftsiderule}
\RequirePackage{fancyhdr}

\def\dotfill#1{\cleaders\hbox to #1{.}\hfill}
\newcommand\dotline[2][0.5em]{\leavevmode\hbox to #2{\dotfill{#1}\hfil}}

\RequirePackage{lastpage}
\RequirePackage{afterpage}
    \fancypagestyle{SASstyle}{
        \fancyhead[L]{\textsf{\hwnum}}
        \fancyhead[R]{\textsf{\subject}}
        \fancyfoot[]{}
        \rfoot{\textsf{\rotatebox{180}{\skykey}}}
        \renewcommand{\footrulewidth}{0pt}
        \renewcommand{\headrulewidth}{0.5pt}
        \lfoot{}}

\pagestyle{SASstyle}


% Tables
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{dcolumn}
    \newcolumntype{d}[1]{D{.}{.}{#1}}
\RequirePackage{tablefootnote}
\RequirePackage{longtable}
% \RequirePackage{nicematrix}

% Lists
\RequirePackage{enumitem}
	\setlist[enumerate]
	   {label=(\arabic*),
		leftmargin=!,
		topsep=0mm,
		itemsep=0mm,
		labelsep=1ex,
		itemindent=5ex,
        align=left}
    \setlist[itemize]
	   {leftmargin=!,
		topsep=0mm,
		itemsep=0mm,
		labelsep=1ex,
		itemindent=5ex,
        align=left}

% Hyphenation
\pretolerance=9999
\tolerance=9999
\hyphenpenalty=9999
\emergencystretch=2cm

% \tolerance=1000

% Fonts and style
\RequirePackage{newpxmath}
\RequirePackage{paratype}

%\setmainfont{AntiquaPSCyr}[
%    Path=./fonts/AntiquaPSCyr/,
%    Extension = .ttf,
%    UprightFont=*-Regular,
%    BoldFont=*-Bold,
%    ItalicFont=*-Italic,
%    BoldItalicFont=*-BoldItalic
%]
%
%\setsansfont{TextbookPSCyr}[
%    Path=./fonts/TextbookPSCyr/,
%    Extension = .ttf,
%    UprightFont=*-Regular,
%    BoldFont=*-Bold,
%    ItalicFont=*-Italic
%]

\newcommand{\boldsans}[1]{\textbf{\textsf{#1}}}

% Multicols
\RequirePackage{paracol}
\RequirePackage{multicol}
    \setlength{\columnsep}{1cm}
    
% Files
\RequirePackage{filecontents}
\RequirePackage{subfiles}
\RequirePackage{hyperref}

% Testing
\RequirePackage{lipsum}

% Table Of Contents
\RequirePackage[titles]{tocloft}
\renewcommand{\cftsecleader}{\cftdotfill{3}}

% color

% \usepackage[usenames, dvipsnames]{color} 
% \usepackage[dvipsnames]{xcolor}

