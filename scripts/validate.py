"""Check the distributable skill and optionally the exact release archive."""

import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

from skills_ref import read_properties, validate

EXPECTED = {
    "SKILL.md", "LICENSE", "agents/openai.yaml",
    "references/ten-step-workflow.md", "references/practice-and-resume.md",
    "references/evidence-review.md", "references/worked-example.md",
    "assets/learning-record.md",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_skill(skill):
    problems = validate(skill)
    require(not problems, f"Agent Skills validation: {problems}")
    props = read_properties(skill)
    require(len(props.description) <= 200, "Use <=200 characters for Claude upload compatibility")
    require(props.license == "MIT", "Missing MIT metadata")
    require(re.fullmatch(r"\d+\.\d+\.\d+", props.metadata.get("version", "")), "Invalid release version")
    paths = list(skill.rglob("*"))
    require(not any(p.is_symlink() for p in paths), "No symlinks in portable package")
    files = {p.relative_to(skill).as_posix() for p in paths if p.is_file()}
    require(files == EXPECTED, f"Unexpected package contents: {files ^ EXPECTED}")
    require(len((skill / "SKILL.md").read_text(encoding="utf-8").splitlines()) < 500, "Entrypoint too long")
    for relative in files:
        path = skill / relative
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"/Users/|/private/tmp/|file://", text), f"Local machine path in {relative}")
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            linked = (path.parent / unquote(parsed.path)).resolve()
            require(linked.is_relative_to(skill.resolve()), f"Reference escapes skill: {relative} -> {target}")
            require(linked.is_file(), f"Broken reference: {relative} -> {target}")
    print("PASS: Agent Skills format, Claude description length, resources, portability")


def validate_archive(archive, skill):
    expected = {"learn-with-ai/" + p for p in EXPECTED}
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "Duplicate archive entries")
        require(set(names) == expected, "Archive must contain only one skill folder and exactly the expected files")
        for name in names:
            part = PurePosixPath(name)
            require(not part.is_absolute() and ".." not in part.parts, "Unsafe archive path")
            require(z.read(name) == (skill / part.relative_to("learn-with-ai")).read_bytes(), f"Archive drift: {name}")
        with tempfile.TemporaryDirectory() as scratch:
            z.extractall(scratch)
            validate_skill(Path(scratch) / "learn-with-ai")
    expected_digest = archive.with_suffix(".zip.sha256").read_text(encoding="utf-8").strip()
    actual = f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}"
    require(actual == expected_digest, "SHA-256 mismatch")
    print("PASS: ZIP layout, byte parity, extracted skill validation, SHA-256")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, help="release ZIP to check")
    parser.add_argument("--built", action="store_true",
                        help="check dist/learn-with-ai-v<version>.zip as built by package.py")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "learn-with-ai"
    validate_skill(skill)
    require((root / "LICENSE").read_bytes() == (skill / "LICENSE").read_bytes(), "License files differ")
    archive = args.archive
    if args.built:
        require(archive is None, "Use either --archive or --built")
        version = read_properties(skill).metadata["version"]
        archive = root / "dist" / f"learn-with-ai-v{version}.zip"
        require(archive.is_file(), f"Run scripts/package.py first: {archive.name} not found")
    if archive:
        validate_archive(archive, skill)


if __name__ == "__main__":
    main()
