#!/usr/bin/env python3
"""Preflight a current-form DFG project-description source and PDF."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

__author__ = "Dr. Awanish Pratap Singh"


REQUIRED_SOURCE_MARKERS = (
    r"\DFGMainPageLimitNotice",
    r"\DFGSection{1}{Starting Point}",
    r"\DFGSection{2}{Objectives and work programme}",
    r"\DFGStackedSubsection{2.1}{Anticipated total duration of the project}",
    r"\DFGSubsection{2.2}{Objectives}",
    r"\DFGSubsection{2.3}{Work programme incl. proposed research methods}",
    r"\DFGSubsection{2.4}{Handling of research data}",
    r"\DFGSubsection{2.5}{Relevance of sex, gender and/or diversity in the research project}",
    r"\DFGSection{3}{Project- and subject-related list of publications}",
    r"\DFGStartReferences",
    r"\DFGEndReferences",
    r"\DFGStartSupplement",
    r"\DFGSection{4}{Supplementary information on the research context}",
    r"\DFGSupplementPageLimitNotice",
    r"\DFGStackedSubsection{4.1}{Ethical and/or legal aspects of the project}",
    r"\DFGStackedSubsubsection{4.1.1}{General ethical aspects}",
    r"\DFGSubsubsection{4.1.2}{Descriptions of proposed investigations on humans, human materials or identifiable data}",
    r"\DFGSubsubsection{4.1.3}{Descriptions of proposed investigations involving experiments on animals}",
    r"\DFGSubsubsection{4.1.4}{Descriptions of projects involving genetic resources (or associated traditional knowledge) from a foreign country}",
    r"\DFGSubsubsection{4.1.5}{Explanations regarding any possible safety-related aspects}",
    r"\DFGDeepSubsubsection{4.1.5.1}{``Dual Use Research of Concern''; foreign trade law}",
    r"\DFGDeepSubsubsection{4.1.5.2}{Risks in international cooperation}",
    r"\DFGSubsubsection{4.1.6}{Considerations on aspects of ecological sustainability in the planning and implementation of the project}",
    r"\DFGSubsection{4.2}{Employment status information}",
    r"\DFGSubsection{4.3}{First-time proposal data}",
    r"\DFGSubsection{4.4}{Composition of the project group}",
    r"\DFGSubsection{4.5}{Researchers in Germany with whom you have agreed to cooperate on this project}",
    r"\DFGSubsection{4.6}{Researchers abroad with whom you have agreed to cooperate on this project}",
    r"\DFGSubsection{4.7}{Researchers with whom you have collaborated scientifically within the past three years}",
    r"\DFGSubsection{4.8}{Project-relevant cooperation with commercial enterprises}",
    r"\DFGSubsection{4.9}{Project-relevant participation in commercial enterprises}",
    r"\DFGSubsection{4.10}{Scientific equipment}",
    r"\DFGSubsection{4.11}{Other submissions}",
    r"\DFGSubsection{4.12}{Other information}",
    r"\DFGSection{5}{Requested modules}",
    r"\DFGStackedSubsection{5.1}{Basic Module}",
    r"\DFGStackedSubsubsection{5.1.1}{Funding for Staff}",
    r"\DFGSubsubsection{5.1.2}{Direct Project Costs}",
    r"\DFGStackedDeepSubsubsection{5.1.2.1}{Equipment up to €10,000, Software and Consumables}",
    r"\DFGDeepSubsubsection{5.1.2.2}{Travel}",
    r"\DFGDeepSubsubsection{5.1.2.3}{Visiting Researchers (excluding Mercator Fellows)}",
    r"\DFGDeepSubsubsection{5.1.2.4}{Expenses for Laboratory Animals}",
    r"\DFGDeepSubsubsection{5.1.2.5}{Other Costs}",
    r"\DFGDeepSubsubsection{5.1.2.6}{Project-related Publication Expenses}",
    r"\DFGSubsubsection{5.1.3}{Instrumentation}",
    r"\DFGStackedDeepSubsubsection{5.1.3.1}{Equipment Exceeding €10,000}",
    r"\DFGDeepSubsubsection{5.1.3.2}{Major Instrumentation Exceeding €50,000}",
    r"\DFGSubsection{5.2}{Module Temporary Position for Principal Investigator}",
    r"\DFGSubsection{5.3}{Module Replacements}",
    r"\DFGSubsection{5.4}{Module Temporary Substitutes for Clinicians}",
    r"\DFGSubsection{5.5}{Module Mercator Fellows}",
    r"\DFGSubsection{5.6}{Module Project-Specific Workshops}",
    r"\DFGSubsection{5.7}{Module Public Relations}",
    r"\DFGSubsection{5.8}{Module Standard Allowance for Equity and Diversity}",
)


class Report:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def ok(self, message: str) -> None:
        self.passed.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def emit(self) -> int:
        print(f"DFG QA: {len(self.passed)} passed, {len(self.warnings)} warnings, {len(self.errors)} errors")
        for message in self.warnings:
            print(f"WARN: {message}")
        for message in self.errors:
            print(f"ERROR: {message}")
        return 1 if self.errors else 0


def strip_tex_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        cleaned.append(line[:cut])
    return "\n".join(cleaned)


def collect_tex(path: Path, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    resolved = path.resolve()
    if resolved in seen:
        return ""
    seen.add(resolved)
    text = strip_tex_comments(path.read_text(encoding="utf-8"))

    def expand_input(match: re.Match[str]) -> str:
        child_name = match.group(1)
        child = path.parent / child_name
        if not child.suffix:
            child = child.with_suffix(".tex")
        if child.is_file():
            return collect_tex(child, seen)
        return match.group(0)

    return re.sub(r"\\(?:input|include)\s*\{([^}]+)\}", expand_input, text)


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"required tool not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout).strip()
        raise RuntimeError(f"{' '.join(command)} failed: {detail}") from exc
    return result.stdout


def parse_pdfinfo(output: str) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in output.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def validate_source(source: Path, allow_guidance: bool, report: Report) -> None:
    try:
        text = collect_tex(source)
    except (OSError, UnicodeError) as exc:
        report.fail(f"cannot read source: {exc}")
        return
    compact = re.sub(r"\s+", " ", text)

    class_match = re.search(r"\\documentclass\[([^]]*)\]\{dfgproposal\}", compact)
    if not class_match:
        report.fail("source does not load dfgproposal with explicit options")
    else:
        options = {item.strip() for item in class_match.group(1).split(",")}
        if "current" not in options:
            report.fail("dfgproposal class is not in current mode")
        elif not allow_guidance and "submission" not in options:
            report.fail("strict QA requires \\documentclass[current,submission]{dfgproposal}")
        else:
            report.ok("class mode")

    missing = [marker for marker in REQUIRED_SOURCE_MARKERS if marker not in compact]
    if missing:
        report.fail(f"missing or renamed current-form structure ({len(missing)} markers)")
    else:
        report.ok("current 53.01 structure")

    boundary_markers = (
        r"\DFGMainPageLimitNotice",
        r"\DFGSection{1}{Starting Point}",
        r"\DFGSection{3}{Project- and subject-related list of publications}",
        r"\DFGStartReferences",
        r"\DFGEndReferences",
        r"\DFGStartSupplement",
        r"\DFGSection{4}{Supplementary information on the research context}",
        r"\DFGSupplementPageLimitNotice",
        r"\DFGStackedSubsection{4.1}{Ethical and/or legal aspects of the project}",
    )
    boundary_positions = [compact.find(marker) for marker in boundary_markers]
    if any(position < 0 for position in boundary_positions):
        report.fail("cannot verify the 17/8 boundary because a boundary marker is missing")
    elif boundary_positions != sorted(boundary_positions):
        report.fail("page-limit notices or the 17/8 section boundary are out of official order")
    else:
        report.ok("17/8 source boundary and notice order")

    unresolved = []
    if r"\DFGInstruction" in compact:
        unresolved.append("DFGInstruction")
    if r"\DFGDecisionRequired" in compact:
        unresolved.append("DFGDecisionRequired")
    for token in ("[First name", "[Project title]", "[last name", "[Text]", "TODO", "FIXME"):
        if token in compact:
            unresolved.append(token)
    if unresolved and not allow_guidance:
        report.fail("unresolved template markers: " + ", ".join(sorted(set(unresolved))))
    elif unresolved:
        report.ok("guidance markers allowed for master template")
    else:
        report.ok("no unresolved template markers")

    if not allow_guidance and re.search(r"\\DFGNotApplicable\s*\{\s*\}", compact):
        report.warn("an empty DFGNotApplicable reason remains")


def validate_pdf(pdf: Path, allow_guidance: bool, report: Report) -> None:
    if not pdf.is_file():
        report.fail(f"PDF not found: {pdf}")
        return
    if pdf.stat().st_size > 10 * 1024 * 1024:
        report.fail("PDF exceeds 10 MB")
    else:
        report.ok("PDF size")

    try:
        info = parse_pdfinfo(run(["pdfinfo", str(pdf)]))
    except RuntimeError as exc:
        report.fail(str(exc))
        return

    try:
        pages = int(info.get("Pages", "0"))
    except ValueError:
        pages = 0
    if 1 <= pages <= 25:
        report.ok("physical page count")
    else:
        report.fail(f"physical page count is {pages}; expected 1--25")

    size_match = re.search(r"([0-9.]+)\s+x\s+([0-9.]+)\s+pts", info.get("Page size", ""))
    if not size_match:
        report.fail("cannot verify A4 page size")
    else:
        width, height = (float(value) for value in size_match.groups())
        if abs(width - 595.28) <= 2 and abs(height - 841.89) <= 2:
            report.ok("A4 page size")
        else:
            report.fail(f"page size is {width:.2f} x {height:.2f} pt, not A4")

    if info.get("Encrypted", "").lower().startswith("no"):
        report.ok("PDF unencrypted")
    else:
        report.fail("PDF is encrypted or its security status is unknown")
    if info.get("JavaScript", "no").lower().startswith("yes"):
        report.fail("PDF contains JavaScript")

    for field in ("Title", "Author", "Subject"):
        value = info.get(field, "")
        if not value:
            report.fail(f"PDF metadata {field} is empty")
        elif not allow_guidance and "[" in value:
            report.fail(f"PDF metadata {field} contains a placeholder")
    if not any(item.startswith("PDF metadata") for item in report.errors):
        report.ok("PDF metadata")

    try:
        font_output = run(["pdffonts", str(pdf)])
    except RuntimeError as exc:
        report.fail(str(exc))
        font_output = ""
    font_rows = []
    font_pattern = re.compile(
        r"^(\S+)\s+(.+?)\s+(\S+)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$"
    )
    for line in font_output.splitlines()[2:]:
        match = font_pattern.match(line.strip())
        if match:
            font_rows.append(match.groups())
    if not font_rows:
        report.fail("no PDF fonts could be inspected")
    else:
        names = [row[0] for row in font_rows]
        if not any("Arial" in name for name in names):
            report.fail("Arial is not present in the PDF")
        elif any("Liberation" in name for name in names):
            report.fail("Liberation Sans fallback is present")
        else:
            report.ok("Arial font")
        if any(row[3] != "yes" for row in font_rows):
            report.fail("one or more PDF fonts are not embedded")
        else:
            report.ok("embedded fonts")
        if any("Type 3" in row[1] for row in font_rows):
            report.fail("Type 3 fonts are present")
        if any(row[5] != "yes" for row in font_rows):
            report.warn("one or more fonts lack a Unicode map; inspect text extraction")

    try:
        extracted = run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"])
    except RuntimeError as exc:
        report.fail(str(exc))
        return
    if len(re.sub(r"\s+", "", extracted)) < 100:
        report.fail("PDF text extraction is empty or implausibly short")
        return
    report.ok("extractable text")

    physical_pages = extracted.split("\f")
    if physical_pages and not physical_pages[-1].strip():
        physical_pages.pop()
    header_pattern = re.compile(r"page\s+(\d+)\s+of\s+max\.?\s*(17|8)", re.IGNORECASE)
    headers = []
    for index, page_text in enumerate(physical_pages, start=1):
        match = header_pattern.search(page_text)
        if not match:
            report.fail(f"DFG page-limit header missing on physical page {index}")
            continue
        headers.append((index, int(match.group(1)), int(match.group(2))))
    if len(headers) != len(physical_pages):
        return

    supplement_positions = [position for position, item in enumerate(headers) if item[2] == 8]
    if not supplement_positions:
        report.fail("no 8-page supplement header sequence found")
        return
    split = supplement_positions[0]
    main_headers = headers[:split]
    supplement_headers = headers[split:]
    if any(item[2] != 17 for item in main_headers) or any(item[2] != 8 for item in supplement_headers):
        report.fail("17-page and 8-page header sequences are interleaved")
    elif [item[1] for item in main_headers] != list(range(1, len(main_headers) + 1)):
        report.fail("main-section page numbers are not sequential from 1")
    elif [item[1] for item in supplement_headers] != list(range(1, len(supplement_headers) + 1)):
        report.fail("supplement page numbers are not sequential from 1")
    elif len(main_headers) > 17 or len(supplement_headers) > 8:
        report.fail("a logical DFG page limit is exceeded")
    else:
        report.ok("17-page/8-page header sequences")

    first_supplement_text = re.sub(r"\s+", " ", physical_pages[split])
    if not re.search(r"\b4\s+Supplementary information on the research context\b", first_supplement_text):
        report.fail("section 4 does not begin on supplement page 1")
    else:
        report.ok("section 4 boundary")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="main project .tex file")
    parser.add_argument("pdf", type=Path, help="compiled project PDF")
    parser.add_argument(
        "--allow-guidance",
        action="store_true",
        help="allow master-template guidance and placeholder metadata",
    )
    args = parser.parse_args()

    report = Report()
    validate_source(args.source, args.allow_guidance, report)
    validate_pdf(args.pdf, args.allow_guidance, report)
    return report.emit()


if __name__ == "__main__":
    sys.exit(main())
