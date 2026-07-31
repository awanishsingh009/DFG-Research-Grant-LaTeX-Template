# LaTeX-Vorlage für DFG-Sachbeihilfeanträge

[English](README.md) | [Deutsch](README.de.md)

Eine wiederverwendbare zweisprachige LaTeX-Vorlage für deutsch- oder
englischsprachige Beschreibungen von DFG-Sachbeihilfevorhaben, gepflegt von
**Dr. Awanish Pratap Singh**.

Das Repository enthält zwei getrennt nutzbare, einsprachige
Antragsvorlagen. Formatierung, Seitenlogik, Prüfroutinen und Dokumentation
werden gemeinsam gepflegt.

> [!IMPORTANT]
> Dies ist eine unabhängige, inoffizielle Vorlage. Sie wird nicht von der
> Deutschen Forschungsgemeinschaft (DFG) veröffentlicht, bestätigt oder
> gepflegt. Maßgeblich sind immer die aktuellen DFG-Vordrucke, die
> elan-Vorlage und die Programminformationen.

## Aktueller Stand

Das Repository wurde am 31. Juli 2026 geprüft gegen:

- DFG-Vordruck 54.01, deutscher und englischer Leitfaden `[06/26]`
- DFG-Vordruck 53.01 elan, deutsche und englische Vorlage `[09/25]`
- Programm- und Modulmerkblätter in
  [`docs/OFFICIAL_DFG_SOURCES.md`](docs/OFFICIAL_DFG_SOURCES.md)

Prüfen Sie am Tag der Einreichung erneut die
[offizielle Seite der DFG-Formulare und Merkblätter](https://www.dfg.de/de/foerderung/foerdermoeglichkeiten/programme/einzelfoerderung/antragspakete/formulare-merkblaetter).

## Eigenschaften

- vollständige aktuelle Gliederung der Beschreibung des Vorhabens;
- getrennte deutsche und englische Vorlagen;
- offizieller Überschriftenwortlaut in beiden Sprachen;
- Entwurfs- und strenger Einreichungsmodus;
- getrennte 17-Seiten- und 8-Seiten-Logik;
- Arial-Prüfung für die Einreichungsfassung;
- DFG-ähnliche Überschriften, Seitenköpfe und Fußzeilen;
- wiederverwendbare Hilfen für Tabellen, Abbildungen und nicht zutreffende Angaben;
- automatisierte Quelltext- und PDF-Prüfungen;
- Build-Befehle für PowerShell und `make`;
- offizielles Quellenregister ohne Weiterverteilung fremder Dokumente.

## Schnellstart

Voraussetzungen:

- XeLaTeX aus MiKTeX oder TeX Live;
- Arial für die strenge Einreichungsfassung;
- Python 3;
- Poppler-Befehle `pdfinfo`, `pdffonts` und `pdftotext`.

Vorlagendateien:

- `main.tex`: Englisch
- `main-de.tex`: Deutsch

Deutschen Entwurf erstellen:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Language german
```

Englischen Entwurf erstellen:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Language english
```

Beide Fassungen erstellen:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Language all
```

Mit `make` stehen `make german`, `make english` und `make bilingual` zur
Verfügung.

Die PDFs werden geschrieben nach:

- `build/german/main-de.pdf`
- `build/english/main.pdf`

## Einreichungsmodus

Entfernen Sie vor der Einreichung alle Vorlagenhinweise und Platzhalter.
Ändern Sie in `main-de.tex`:

```tex
\documentclass[current,guidance,german]{dfgproposal}
```

zu:

```tex
\documentclass[current,submission,german]{dfgproposal}
```

Danach:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -Language german -Strict
```

oder:

```bash
make german-strict
```

Arbeiten Sie zusätzlich
`CURRENT_DFG_COMPLIANCE_CHECKLIST.de.md` vollständig ab und prüfen Sie jede
PDF-Seite visuell.

Ein einzureichendes PDF soll durchgehend eine Sprache verwenden. Das
Repository ist zweisprachig; die einzelne Beschreibung des Vorhabens ist es
nicht.

## Offizielle Dokumente

DFG-Dokumente werden nicht im Repository gespeichert. Das Quellenregister
enthält deutsche und englische Links. Eine lokale, von Git ignorierte Kopie
kann mit folgendem Befehl erstellt werden:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_official_sources.ps1
```

## Zitation

Für die Zitation stehen die Metadaten in `CITATION.cff` zur Verfügung:

> Singh, A. P. (2026). *DFG Research Grant LaTeX Template* (Version 1.1.0).

## Lizenz und Kennzeichen

Der eigenständige Vorlagencode und die Dokumentation stehen unter der
MIT-Lizenz. Namen, Vordrucke, Gestaltungselemente und verlinkte Dokumente der
DFG verbleiben bei den jeweiligen Rechteinhabern und sind nicht Bestandteil
dieser Lizenz.

## Autor und Maintainer

**Dr. Awanish Pratap Singh**

[GitHub-Profil](https://github.com/awanishsingh009)
