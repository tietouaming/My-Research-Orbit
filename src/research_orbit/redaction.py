"""Local-only redaction auditing utilities."""

from __future__ import annotations

import re
from pathlib import Path

from research_orbit.memory_cards import collect_input_files
from research_orbit.schemas import RedactionFinding

WINDOWS_PATH = re.compile(r"\b[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*")
UNIX_PATH = re.compile(r"(?<![\w])/(?:home|Users|mnt|var|etc|opt|tmp|srv|root)/[^\s`),;]+")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password|passwd|authorization)\b"
    r"\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+=]{8,})"
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[- ]?)?(?:\d[- ]?){10,14}\d(?!\d)")
SENSITIVE_FILE = re.compile(
    r"(?i)(?:\b[\w.\-<>]+)?"
    r"(?:\.mphbin|\.mph|\.hdf5|\.h5|\.npz|\.vtu|\.xdmf|\.png|\.gif|"
    r"\.pem|\.key|\.token|\.env)"
    r"(?=\b|[`'\"),.;:\]]|$)"
)


def scan_text(text: str, source_path: str = "<memory>") -> list[RedactionFinding]:
    findings: list[RedactionFinding] = []
    patterns = [
        ("windows_path", WINDOWS_PATH, "high", "Possible Windows absolute path."),
        ("unix_path", UNIX_PATH, "high", "Possible Unix absolute path."),
        ("secret", SECRET_ASSIGNMENT, "high", "Possible key, token, password, or secret."),
        ("email", EMAIL, "medium", "Possible email address."),
        ("phone", PHONE, "medium", "Possible phone number."),
        (
            "sensitive_file",
            SENSITIVE_FILE,
            "high",
            "Sensitive, private, or large binary file extension mentioned.",
        ),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for finding_type, pattern, severity, message in patterns:
            for match in pattern.finditer(line):
                findings.append(
                    RedactionFinding(
                        source_path=source_path,
                        line_number=line_number,
                        finding_type=finding_type,
                        severity=severity,
                        message=message,
                        excerpt=_mask_excerpt(match.group(0)),
                    )
                )
    return findings


def scan_paths(paths: list[Path]) -> list[RedactionFinding]:
    findings: list[RedactionFinding] = []
    for path in collect_input_files(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(
                RedactionFinding(
                    source_path=path.as_posix(),
                    line_number=1,
                    finding_type="binary_or_non_utf8",
                    severity="high",
                    message="File is not UTF-8 text and should not be audited as public text.",
                    excerpt=path.name,
                )
            )
            continue
        findings.extend(scan_text(text, path.as_posix()))
    return findings


def render_redaction_report(findings: list[RedactionFinding]) -> str:
    lines = [
        "# Redaction Audit Report",
        "",
        "This report is generated locally. It does not upload files or call external APIs.",
        "",
        f"Total findings: {len(findings)}",
        "",
    ]
    if not findings:
        lines.append("No suspicious sensitive patterns were detected.")
        return "\n".join(lines) + "\n"

    for finding in findings:
        lines.extend(
            [
                f"## {finding.severity.upper()} - {finding.finding_type}",
                "",
                f"- source: `{finding.source_path}`",
                f"- line: {finding.line_number}",
                f"- message: {finding.message}",
                f"- excerpt: `{finding.excerpt}`",
                "",
            ]
        )
    return "\n".join(lines)


def _mask_excerpt(value: str) -> str:
    if len(value) <= 8:
        return value
    if "\\" in value or "/" in value:
        parts = re.split(r"([\\/])", value)
        tail = "".join(parts[-3:])
        return f"<path>...{tail}"
    return f"{value[:4]}...{value[-4:]}"
