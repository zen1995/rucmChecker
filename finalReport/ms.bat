xelatex main.tex
bibtex main.tex
xelatex main.tex
xelatex main.tex

del *.aux *.log *.out *.thm *.toc

call main.pdf