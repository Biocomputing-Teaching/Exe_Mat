doc   = ExercicisResolts

all: $(doc).pdf

$(doc).pdf: $(doc).tex Ex*.tex
	lualatex $(doc)
	lualatex $(doc)

clean:
	rm -f $(doc)*.{bcf,run.xml,pro,aux,nav,out,log,idx,ind,ilg,toc,bbl,blg,tdo,lot,lof,glo,snm}
cleanall:
	rm -f $(doc)*.{bcf,run.xml,pro,aux,nav,out,log,idx,ind,ilg,toc,bbl,blg,tdo,lot,lof,glo,snm}
	rm -f $(doc)*.pdf
