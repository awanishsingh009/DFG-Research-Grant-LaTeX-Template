# Author: Dr. Awanish Pratap Singh
SOURCE ?= main.tex
BUILD ?= build
PDF := $(BUILD)/$(basename $(notdir $(SOURCE))).pdf

.PHONY: all draft strict clean

all: draft

draft:
	mkdir -p $(BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILD) $(SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILD) $(SOURCE)
	python scripts/validate_dfg_pdf.py $(SOURCE) $(PDF) --allow-guidance

strict:
	mkdir -p $(BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILD) $(SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILD) $(SOURCE)
	python scripts/validate_dfg_pdf.py $(SOURCE) $(PDF)

clean:
	rm -f $(BUILD)/*.aux $(BUILD)/*.log $(BUILD)/*.out $(BUILD)/*.toc $(BUILD)/*.fls $(BUILD)/*.fdb_latexmk
