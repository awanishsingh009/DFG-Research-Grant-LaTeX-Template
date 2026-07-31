# Author: Dr. Awanish Pratap Singh
EN_SOURCE := main.tex
DE_SOURCE := main-de.tex
EN_BUILD := build/english
DE_BUILD := build/german

.PHONY: all bilingual english german draft strict english-strict german-strict clean

all: bilingual
bilingual: english german
	python scripts/check_language_parity.py $(EN_SOURCE) $(DE_SOURCE)
draft: english
strict: english-strict

english:
	mkdir -p $(EN_BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(EN_BUILD) $(EN_SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(EN_BUILD) $(EN_SOURCE)
	python scripts/validate_dfg_pdf.py $(EN_SOURCE) $(EN_BUILD)/main.pdf --language english --allow-guidance

german:
	mkdir -p $(DE_BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(DE_BUILD) $(DE_SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(DE_BUILD) $(DE_SOURCE)
	python scripts/validate_dfg_pdf.py $(DE_SOURCE) $(DE_BUILD)/main-de.pdf --language german --allow-guidance

english-strict:
	mkdir -p $(EN_BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(EN_BUILD) $(EN_SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(EN_BUILD) $(EN_SOURCE)
	python scripts/validate_dfg_pdf.py $(EN_SOURCE) $(EN_BUILD)/main.pdf --language english

german-strict:
	mkdir -p $(DE_BUILD)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(DE_BUILD) $(DE_SOURCE)
	xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(DE_BUILD) $(DE_SOURCE)
	python scripts/validate_dfg_pdf.py $(DE_SOURCE) $(DE_BUILD)/main-de.pdf --language german

clean:
	rm -f $(EN_BUILD)/*.aux $(EN_BUILD)/*.log $(EN_BUILD)/*.out $(EN_BUILD)/*.toc $(EN_BUILD)/*.fls $(EN_BUILD)/*.fdb_latexmk
	rm -f $(DE_BUILD)/*.aux $(DE_BUILD)/*.log $(DE_BUILD)/*.out $(DE_BUILD)/*.toc $(DE_BUILD)/*.fls $(DE_BUILD)/*.fdb_latexmk
