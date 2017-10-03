# ===============================================================================
# Makefile for Thesis 
# Mostly copied from LHCb template
# ===============================================================================


# name of the main latex file
MAIN = main

# name of the target
TARGET = thesis_v0

# name of command to perform Latex (either pdflatex or latex)
LATEX = pdflatex

ifeq ($(LATEX),pdflatex)
    FIGEXT = .pdf
    MAINEXT= .pdf
    BUILDCOMMAND=rm -f $(MAIN).aux && $(LATEX) $(MAIN) && bibtex $(MAIN) && $(LATEX) $(MAIN) && $(LATEX) $(MAIN)
    MAKEMAINCOUNT= sed 's\#{wordcount}{false}\#{wordcount}{true}\#' main.tex > main-count.tex
    BUILDCOMMANDCOUNT= $(MAKEMAINCOUNT) && rm -f $(MAIN)-count.aux && $(LATEX) $(MAIN)-count && bibtex $(MAIN)-count >/dev/null; true && $(LATEX) $(MAIN)-count && ./wordcount.sh $(MAIN)-count && rm wordcount.pdf main-count* 
else
    FIGEXT = .eps
    MAINEXT= .pdf
    BUILDCOMMAND=rm -f $(MAIN).aux && $(LATEX) $(MAIN) && bibtex $(MAIN) && $(LATEX) $(MAIN) && $(LATEX) $(MAIN) && dvips -z -o $(MAIN).ps $(MAIN) && ps2pdf $(MAIN).ps && rm -f head.tmp body.tmp
    BUILDCOMMANDCOUNT=
endif

# list of all source files
TEXSOURCES = $(wildcard text/*.tex) $(wildcard bib/*.bib)
FIGSOURCES = $(wildcard figs/*$(FIGEXT))
SOURCES    = $(TEXSOURCES) $(FIGSOURCES)

# define output
OUTPUT = $(TARGET)$(MAINEXT)

# cp temporary main.pdf to target.
$(OUTPUT): $(MAIN)$(MAINEXT)
	cp $(MAIN)$(MAINEXT) $(OUTPUT)

# prescription how to make output (your favorite commands to process latex)
# do latex twice to make sure that all cross-references are updated 
$(MAIN)$(MAINEXT): $(SOURCES) Makefile
	$(BUILDCOMMAND)

# just so we can say "make all" without knowing the output name
all: $(OUTPUT)

# remove temporary files (good idea to say "make clean" before putting things back into repository)
.PHONY : clean
clean:
	rm -f *~ *.aux *.log *.bbl *.blg *.dvi *.tmp *.out *.blg *.bbl $(OUTPUT) $(MAIN)$(MAINEXT) $(MAIN).ps $(MAIN)-prl.ps $(MAIN)-prlNotes.bib

# remove output file
rmout: 
	rm $(OUTPUT) $(MAIN)$(MAINEXT)

# Do word count
count: 
	$(BUILDCOMMANDCOUNT)
	@echo ''
	@echo 'Figures:   Add 20+150/(aspect ratio) per figure'
	@echo 'Equations: Add 16 words per row (single column) '
	@echo 'Tables:    Add 13 words plus 6.5 words per line (single column)'
	@echo 