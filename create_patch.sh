#!/bin/bash
echo "Syncing with upstream..."
git fetch upstream
git merge upstream/main

echo "Building pokehns..."
make hns

BASE_ROM="Pokemon - Emerald Version.gba"
MODIFIED_ROM="pokehns.gba"
OUTPUT_PATCH="patches/PokeHnS-X.X.X-Lyra_patch.bps"
if [ ! -f "$BASE_ROM" ]; then
    echo "Error: base ROM not found at $BASE_ROM"
    exit 1
fi
if [ ! -f "$MODIFIED_ROM" ]; then
    echo "Error: modified ROM not found. Have you run make hns?"
    exit 1
fi
echo "Building..."
make hns
echo "Creating patch..."
flatpak run com.github.Alcaro.Flips --create --bps "$BASE_ROM" "$MODIFIED_ROM" "$OUTPUT_PATCH"
echo "Done! Patch saved to $OUTPUT_PATCH"
echo "Applying patch for testing..."
flatpak run com.github.Alcaro.Flips --apply "$OUTPUT_PATCH" "$BASE_ROM" "PokeHnS-X.X.X-Lyra_test.gba"
echo "Done applying patch. Please test 'PokeHnS-X.X.X-Lyra_test.gba', then rename patch file with current version number"
