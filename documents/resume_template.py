
from textwrap import dedent
resume = dedent(r'''---
header-includes:
    - \pagestyle{empty}
    - \usepackage{ragged2e}
    - \usepackage{fontawesome5}
    - \newcommand{\FullHRule}{\noindent\rule{\linewidth}{0.5pt}}
    - \usepackage{titlesec}
    - \titleformat{\section}[block]{\normalfont\fontsize{28}{32}\selectfont\centering}{\thesection}{1em}{}
    - \titleformat{\subsection}[block]{\normalfont\large\centering}{\thesubsection}{1em}{}
    - \titleformat{\subsubsection}[block]{\normalfont\large\bfseries}{\thesubsubsection}{1em}{}
    - \usepackage{tikz}
    - \usetikzlibrary{calc}
    - \usepackage{eso-pic}
    - \AddToShipoutPictureBG{\begin{tikzpicture}[remember picture,overlay]\draw[line width=1pt]($(current page.north west)+(0.35cm,-0.35cm)$) rectangle ($(current page.south east)+(-0.35cm,0.35cm)$);\end{tikzpicture}}

mainfont: "Arial Narrow"
fontsize: 12pt
papersize: letter
geometry: "top=0.5in, bottom=0.5in, left=0.5in, right=0.5in"
---

# A D E E L \hspace{0.25em} S U L T A N 
## SOFTWARE DEVELOPMENT ENGINEER
\FullHRule
                  
\begin{center}                  
\faIcon{map-marker-alt} Chicago, IL \hspace{0.75em} \faEnvelope{} adeel4sultan@gmail.com \hspace{0.75em}
\faPhone{} (920) 757-4504 \hspace{0.75em} \faIcon{linkedin} sultanadeel \hspace{0.75em} \faIcon{github} adeel-s
\end{center}    

### EXPERIENCE

**Fullstack Developer @ hired.ai**
*Chicago, IL | December 2024 - Present*

!@#$Placeholder

**Software Engineering Intern @ Oshkosh Corporation**
*Oshkosh, WI | January 2023 - May 2024*

!@#$Placeholder

**Lead Developer @ University of Wisconsin - Oshkosh**
*Oshkosh, WI | September 2023 - December 2023*

!@#$Placeholder


### SKILLS

* **Programming Languages**: Python, Java, Javascript, HTML/CSS, C#, C++, SQL
* **Frameworks**: Node.js, Flask, .NET Maui, Flutter
* **Tools**: Git/Hub, VS Code, Visual Studio, Docker, Android Studio, Pandas


### EDUCATION

**Bachelor of Science in Computer Science with Honors**
*University of Wisconsin - Oshkosh | 2020 - 2024 | GPA: 3.8 | Dean's List | Undergraduate Research Grant Recipient*
''')
