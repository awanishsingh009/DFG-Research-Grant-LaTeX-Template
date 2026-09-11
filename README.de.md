# LaTeX-Vorlage für DFG-Sachbeihilfeanträge

[English](README.md) · [Deutsch](README.de.md)

Kurzes Hauptdokument, getrennte Kapiteldateien, funktionierende Literaturangaben
und nachvollziehbare Prüfungen. Gepflegt von **Dr. Awanish Pratap Singh**.
Unabhängige, inoffizielle Vorlage unter MIT-Lizenz.

**Quellenstand:** Vordrucke 53.01 und 54.01 [09/26], geprüft am 10. September 2026.
Andere Förderprogramme benötigen gesondert geprüfte Vorlagen.

## Einstieg

1. Das [deutsche Starter-ZIP herunterladen](https://github.com/awanishsingh009/DFG-Research-Grant-LaTeX-Template/releases/download/v2.0.0/dfg-starter-de.zip) oder das Repository als GitHub-Vorlage verwenden.
2. Im zweisprachigen Repository metadata-de.tex bearbeiten.
3. Den eigenen Text in sections/de/ schreiben.
4. Literatur in bibliography/references.bib ergänzen.
5. Kompilieren.

**Overleaf:** ZIP hochladen, XeLaTeX auswählen und main-de.tex als Hauptdokument
festlegen. Im einsprachigen Starter heißt die Hauptdatei main.tex.
Python ist zum Kompilieren auf Overleaf nicht erforderlich.

**Lokal:** TeX-Distribution mit XeLaTeX und Biber sowie Python 3.10+ installieren.
Der Python-Build benötigt weder pip-Pakete noch Perl.

    python scripts/doctor.py
    python scripts/build.py --language german

Unter macOS/Linux gegebenenfalls python3 verwenden. Für die PDF-Prüfungen
wird zusätzlich Poppler benötigt. Fehlende optionale Werkzeuge werden im Entwurf
als nicht geprüft angezeigt; bei Einreichungsprüfungen führen sie zum Abbruch.
[Installation](docs/SETUP.md) · [Overleaf](docs/OVERLEAF.md)

## Beispiel und Einreichungsfassung

    python scripts/build.py --source example-de.tex --language german

Das fiktive Beispiel zeigt mehrere Antragstellende, Literatur, Querverweise,
Gleichungen, Abbildungen und Tabellen. Es ist kein Forschungsantrag.

Ersetzen Sie alle Schreibhinweise und Platzhalter. Treffen Sie nach fachlicher
Prüfung die Auswahl zur Erforderlichkeit einer Ethikstellungnahme.

    python scripts/build.py --language german --release

Der Schalter wählt den Einreichungsmodus automatisch. Arial, vollständige
Kompilation, korrekte Literaturverweise, Kapitelstruktur und PDF-Prüfungen
werden verlangt. Ergebnisse liegen unter build/release/german/xelatex/.
Der Bericht .checks.json dokumentiert die einzelnen Prüfungen.

**Automatische Formatprüfungen ersetzen keine wissenschaftliche oder
administrative Prüfung.** Kontrollieren Sie die PDF visuell und verwenden Sie
die [Checkliste](CURRENT_DFG_COMPLIANCE_CHECKLIST.de.md).
Prüfen Sie vor der Einreichung die aktuellen offiziellen DFG-Unterlagen.

[Anwendung](docs/AUTHORING.md) · [Migration von Version 1](docs/MIGRATION.md) ·
[Quellen](docs/OFFICIAL_DFG_SOURCES.md) · [Mitwirken](CONTRIBUTING.md)
