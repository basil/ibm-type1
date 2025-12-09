from pathlib import Path
import argparse
import contextlib
import sys

try:
    import fontforge
except ImportError:
    print(
        "ERROR: This script must be run with FontForge's Python interpreter.",
        file=sys.stderr,
    )
    print(
        "Run it like this: fontforge -script convert.py /path/to/fonts", file=sys.stderr
    )
    sys.exit(1)


def convert(type1, out_dir):
    with contextlib.closing(fontforge.open(str(type1))) as font:
        # Set Unicode encoding (map glyphs to Unicode where possible)
        font.encoding = "UnicodeFull"

        # Produce OTF, TTF, and WOFF2
        for ext in (".otf", ".ttf", ".woff2"):
            out_path = out_dir / (font.fontname + ext)
            print("Generating:", out_path)
            font.generate(str(out_path))


def main():
    ap = argparse.ArgumentParser(
        description="Convert font from Type 1 to OTF/TTF/WOFF2 using FontForge"
    )
    ap.add_argument(
        "indir", nargs="?", default=".", help="Input directory (default: current dir)"
    )
    ap.add_argument(
        "-o", "--outdir", default=None, help="Output directory (default: same as input)"
    )
    args = ap.parse_args()

    indir = Path(args.indir)
    outdir = Path(args.outdir) if args.outdir else indir

    if not indir.is_dir():
        print("Input directory does not exist:", str(indir), file=sys.stderr)
        sys.exit(1)

    outdir.mkdir(parents=True, exist_ok=True)

    found_any = False

    for p in indir.glob("*.pfa"):
        if p.is_file():
            found_any = True
            convert(p, outdir)

    for p in indir.glob("*.pfb"):
        if p.is_file():
            found_any = True
            convert(p, outdir)

    if not found_any:
        print("No .pfa or .pfb files found in", str(indir), file=sys.stderr)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
