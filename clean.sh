#clean garbage in git
for type in .dat .dvi .lua .table .swp .fls .log .aux .pro .auxlock .bbl .bcf .blg .idx .snm .nav .vrb .toc .ilg .ind .loe .out .aux .fdb_latexmk .xml .gz .pro .log .md5 FULLRESPOSTES.tex FULLRESPOSTES.pdf
do
 echo "Processing *$type"
 git rm -f *$type
 rm -f *$type
 echo "Processing */*$type"
 git rm -f */*$type
 rm -f */*$type
done
