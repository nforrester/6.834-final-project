all: paper.pdf

paper.pdf: paper.tex
	pdflatex -halt-on-error paper.tex
	# run twice to get section numbers and other cross-references right on the first try.
	pdflatex -halt-on-error paper.tex

clean:
	rm *.pdf *.toc *.aux *.log
