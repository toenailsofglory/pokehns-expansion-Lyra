#!/usr/bin/env python3
"""
Extract palette from an indexed PNG and save as a .pal file
for use with pokeemerald decomp projects.

Usage: python3 extract_palette.py input.png output.pal
"""

import sys
from PIL import Image

def extract_palette(png_path, pal_path):
    img = Image.open(png_path)

    if img.mode != 'P':
        print(f"Error: image is not indexed (mode is {img.mode}). Convert to indexed first.")
        sys.exit(1)

    raw = img.getpalette()
    used_indices = set(img.getdata())
    num_colors = max(used_indices) + 1
    print(f"Found {num_colors} colors in use.")

    output_colors = max(num_colors, 16)

    with open(pal_path, 'w', newline='\r\n') as f:
        f.write("JASC-PAL\n")
        f.write("0100\n")
        f.write(f"{output_colors}\n")
        for i in range(output_colors):
            if raw and i * 3 + 2 < len(raw):
                r = raw[i * 3]
                g = raw[i * 3 + 1]
                b = raw[i * 3 + 2]
            else:
                r, g, b = 0, 0, 0
            f.write(f"{r} {g} {b}\n")

    print(f"Palette written to {pal_path} with {output_colors} colors.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_palette.py input.png output.pal")
        sys.exit(1)
    extract_palette(sys.argv[1], sys.argv[2])
