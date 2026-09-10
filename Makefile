PYTHON ?= python3
.PHONY: all english german bilingual strict english-strict german-strict pdflatex-draft doctor test
all: bilingual
english:
	$(PYTHON) scripts/build.py --language english
german:
	$(PYTHON) scripts/build.py --language german
bilingual:
	$(PYTHON) scripts/build.py --language all
strict: english-strict
english-strict:
	$(PYTHON) scripts/build.py --language english --release
german-strict:
	$(PYTHON) scripts/build.py --language german --release
pdflatex-draft:
	$(PYTHON) scripts/build.py --language all --engine pdflatex
doctor:
	$(PYTHON) scripts/doctor.py
test:
	$(PYTHON) -m unittest discover -s tests -v
