#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IMG_SRC_RE = re.compile(r"<img\b[^>]*\bsrc=['\"]([^'\">]+)['\"]", re.IGNORECASE)
SRCSET_RE = re.compile(r"\bsrcset=['\"]([^'\"]+)['\"]", re.IGNORECASE)
CSS_URL_RE = re.compile(r"url\(([^)]+)\)", re.IGNORECASE)
JS_IMG_STR_RE = re.compile(r"(['\"])([^'\"]+\.(?:png|jpe?g|gif|svg|webp))(\1)", re.IGNORECASE)


def normalize_ref(ref: str) -> str:
    ref = ref.strip().strip('"\'')
    ref = ref.split('#', 1)[0].split('?', 1)[0]
    return ref


def should_ignore_ref(ref: str) -> bool:
    return (
        not ref
        or ref.startswith(
            (
                "http://",
                "https://",
                "data:",
                "mailto:",
                "tel:",
                "#",
                "//",  # protocol-relative
            )
        )
    )


def check_path(base_dir: Path, ref: str, kind: str, owner_file: Path, missing: list) -> None:
    ref = normalize_ref(ref)
    if should_ignore_ref(ref):
        return

    target = (base_dir / ref).resolve()

    try:
        target.relative_to(ROOT)
    except Exception:
        missing.append((kind, owner_file.relative_to(ROOT).as_posix(), ref, "OUTSIDE_ROOT"))
        return

    if not target.exists():
        missing.append((kind, owner_file.relative_to(ROOT).as_posix(), ref, "MISSING"))


def main() -> int:
    html_files = list(ROOT.rglob("*.html"))
    css_files = list(ROOT.rglob("*.css"))
    js_files = list(ROOT.rglob("*.js"))

    missing: list[tuple[str, str, str, str]] = []
    leading_slash: list[tuple[str, str]] = []

    for f in html_files:
        txt = f.read_text(errors="ignore")

        # Leading-slash internal paths break on GitHub Pages project sites
        for m in re.finditer(r"\b(?:href|src)=['\"]/[^/][^'\"]*['\"]", txt, re.IGNORECASE):
            leading_slash.append((f.relative_to(ROOT).as_posix(), m.group(0)))

        for ref in IMG_SRC_RE.findall(txt):
            check_path(f.parent, ref, "HTML_IMG_SRC", f, missing)

        for srcset in SRCSET_RE.findall(txt):
            # srcset format: "a.jpg 1x, b.jpg 2x" -> extract URLs
            parts = [p.strip().split(" ")[0] for p in srcset.split(",") if p.strip()]
            for ref in parts:
                check_path(f.parent, ref, "HTML_SRCSET", f, missing)

    for f in css_files:
        txt = f.read_text(errors="ignore")
        for raw in CSS_URL_RE.findall(txt):
            check_path(f.parent, raw, "CSS_URL", f, missing)

    for f in js_files:
        txt = f.read_text(errors="ignore")
        for _, ref, _ in JS_IMG_STR_RE.findall(txt):
            check_path(f.parent, ref, "JS_IMG_STR", f, missing)

    print(f"HTML files: {len(html_files)} | CSS files: {len(css_files)} | JS files: {len(js_files)}")
    print(f"Leading-slash href/src findings: {len(leading_slash)}")
    print(f"Missing asset refs: {len(missing)}")

    if leading_slash:
        print("\nLEADING_SLASH (first 20):")
        for file_path, snippet in leading_slash[:20]:
            print(f" - {file_path} :: {snippet}")

    if missing:
        print("\nMISSING_ASSETS (first 50):")
        for kind, owner, ref, why in missing[:50]:
            print(f" - {kind} in {owner}: {ref} ({why})")

    return 1 if (leading_slash or missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
