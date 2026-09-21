"""Build a deterministic, single-skill ZIP; never package personal records."""

from pathlib import Path
import hashlib
import zipfile

from skills_ref import read_properties
from validate import validate_skill


def main():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "learn-with-ai"
    validate_skill(skill)
    version = read_properties(skill).metadata["version"]
    output = root / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"learn-with-ai-v{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(skill.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(str(path.relative_to(skill.parent)).replace("\\", "/"))
                info.date_time = (2026, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                z.writestr(info, path.read_bytes())
    checksum = archive.with_suffix(".zip.sha256")
    checksum.write_text(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n", encoding="utf-8")
    print(f"Built {archive.name} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
