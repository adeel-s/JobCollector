from textwrap import dedent
template = dedent(r'''---
header-includes:
    - \pagestyle{empty}
    - \usepackage{ragged2e}
    - \usepackage{fontawesome5}
    - \newcommand{\FullHRule}{\noindent\rule{\linewidth}{0.5pt}}
    - \usepackage{titlesec}
    - \titleformat{\section}[block]{\normalfont\fontsize{28}{32}\selectfont\centering}{\thesection}{1em}{}
    - \titleformat{\subsection}[block]{\normalfont\large\centering}{\thesubsection}{1em}{}
    - \usepackage{tikz}
    - \usetikzlibrary{calc}
    - \usepackage{eso-pic}
    - \AddToShipoutPictureBG{\begin{tikzpicture}[remember picture,overlay]\draw[line width=1pt]($(current page.north west)+(0.35cm,-0.35cm)$) rectangle ($(current page.south east)+(-0.35cm,0.35cm)$);\end{tikzpicture}}

mainfont: "Arial Narrow"
fontsize: 12pt
papersize: letter
geometry: "top=0.5in, bottom=0.5in, left=1in, right=1in"
---

# A D E E L \hspace{0.25em} S U L T A N 
## SOFTWARE DEVELOPMENT ENGINEER
\FullHRule
                  
\begin{center}                  
\faIcon{map-marker-alt} Chicago, IL \hspace{0.75em} \faEnvelope{} adeel4sultan@gmail.com \hspace{0.75em}
\faPhone{} (920) 757-4504 \hspace{0.75em} \faIcon{linkedin} sultanadeel \hspace{0.75em} \faIcon{github} adeel-s
\end{center}   
\                    

                  
!@#$PlaceholderDate

!@#$PlaceholderCompany

Dear Hiring Manager,
\

!@#$PlaceholderLetter

Sincerely,  
Adeel Sultan

''')