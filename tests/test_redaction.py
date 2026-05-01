from research_orbit.redaction import scan_text


def test_scan_text_detects_sensitive_patterns() -> None:
    text = """
    path: C:\\Users\\Researcher\\secret\\model.mph
    api_key = placeholder-value
    contact: user@example.com
    """
    findings = scan_text(text, "sample.md")
    finding_types = {finding.finding_type for finding in findings}
    assert "windows_path" in finding_types
    assert "secret" in finding_types
    assert "email" in finding_types
    assert "sensitive_file" in finding_types
    assert all("placeholder-value" not in finding.excerpt for finding in findings)


def test_scan_text_detects_standalone_sensitive_extensions() -> None:
    findings = scan_text("Do not upload `.mph`, `.mphbin`, or `.npz` artifacts.", "sample.md")
    excerpts = {finding.excerpt for finding in findings}
    assert {".mph", ".mphbin", ".npz"}.issubset(excerpts)
