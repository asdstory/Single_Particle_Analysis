###
This is to convert selected particles star file into coordination star file, for tracking where the particles are from and how it look like in raw image.

###

import os
from collections import defaultdict

input_star = "particles.star"
output_dir = "coordinate_star_files"
os.makedirs(output_dir, exist_ok=True)

with open(input_star, "r") as f:
    lines = f.readlines()

in_particles_block = False
in_loop = False

column_names = []
data_tokens = []

col_idx_x = -1
col_idx_y = -1
col_idx_mic = -1

micrographs = defaultdict(list)

for line in lines:
    stripped = line.strip()

    # Step 1: Detect and isolate data blocks
    if stripped.startswith("data_"):
        if stripped == "data_particles":
            in_particles_block = True
        else:
            in_particles_block = False
        in_loop = False
        continue

    # Skip comments, empty spaces, or other data blocks (like optics)
    if not in_particles_block or not stripped or stripped.startswith("#"):
        continue

    if stripped.startswith("loop_"):
        in_loop = True
        column_names = []
        continue

    # Step 2: Handle RELION 5 labels by isolating the first token string
    if in_loop and stripped.startswith("_rln"):
        parts = stripped.split()
        col_name = parts[0]  # Safely extracts string (e.g., '_rlnCoordinateX')
        column_names.append(col_name)

        if col_name == "_rlnCoordinateX":
            col_idx_x = len(column_names) - 1
        elif col_name == "_rlnCoordinateY":
            col_idx_y = len(column_names) - 1
        elif col_name == "_rlnMicrographName":
            col_idx_mic = len(column_names) - 1
        continue

    # Step 3: Stream row fields line-by-line to stitch multi-line rows
    if in_loop and len(column_names) > 0 and not stripped.startswith("_"):
        data_tokens.extend(stripped.split())

        # Once tokens reach the expected label count (25 fields), parse them out
        while len(data_tokens) >= len(column_names):
            row_tokens = data_tokens[:len(column_names)]
            data_tokens = data_tokens[len(column_names):]  # Shift array window forward

            x = row_tokens[col_idx_x]
            y = row_tokens[col_idx_y]
            mic = row_tokens[col_idx_mic]
            micrographs[mic].append((x, y))

# Step 4: Write clean RELION coordinate files
for mic_path, coords in micrographs.items():
    # Extract base filename out of subdirectories (e.g., '20260713/top3a0000.tif')
    mic_base = os.path.basename(mic_path)
    
    # Strip common image file extensions
    for ext in [".tif", ".mrc", ".mrcs"]:
        if mic_base.lower().endswith(ext):
            mic_base = mic_base[:-len(ext)]
            break

    out_file = os.path.join(output_dir, f"{mic_base}_pick.star")

    with open(out_file, "w") as out:
        out.write("\n# Created from RELION 5 particles.star\n\n")
        out.write("data_coordinates\n\nloop_\n")
        out.write("_rlnCoordinateX #1\n")
        out.write("_rlnCoordinateY #2\n")
        for x, y in coords:
            out.write(f" {x:<15} {y:<15}\n")

print(f"Success! Generated coordinate files for {len(micrographs)} micrographs inside '{output_dir}/'.")
