# Reads src/*.midx and generates files at import/delete_all_og_data/*.mpat which delete all pointers present in the mscr.
# This can be used for overwriting OG maps entirely without worrying about hitting space limits.

from glob import glob
import os
import re

blacklist_ptrs = ['$Start', '$End', '$Header', '$Script_Main', '$EntryList']

os.makedirs('import/delete_all_og_data', exist_ok=True)

patched_battles = False
patched_maps = False

for fname in glob('src/*.midx'):
    file_label = fname[4:-5]
    print(f"{file_label}...", end='')

    pointers = []

    with open(fname, 'r') as f:
        for line in f.readlines():
            match = re.search(r'^(\$[^#]+)', line)
            if match:
                pointer = match.group(1)

                if not pointer in blacklist_ptrs:
                    pointers.append(pointer)

    print(f" found {len(pointers)} pointers")

    with open(f'import/delete_all_og_data/{file_label}.mpat', 'w') as f:
        for pointer in pointers:
            f.write(f'#delete {pointer}\n')
    
    patched_maps = True

for fname in glob('src/*.bidx'):
    file_label = fname[4:-5]
    print(f"{file_label}...", end='')

    pointers = []

    with open(fname, 'r') as f:
        for line in f.readlines():
            match = re.search(r'^(\$[^#]+)', line)
            if match:
                pointer = match.group(1)

                if not pointer in blacklist_ptrs:
                    pointers.append(pointer)

    print(f" found {len(pointers)} pointers")

    with open(f'import/delete_all_og_data/{file_label}.bpat', 'w') as f:
        for pointer in pointers:
            f.write(f'#delete {pointer}\n')
    
    patched_battles = True

if not patched_battles and not patched_maps:
    print("Nothing to do. Is this script next to a src/ folder?")
    os.exit(1)

example_fname = "delete_all_og_data/file_label.mpat"
if patched_battles:
    example_fname = "delete_all_og_data/FILE.bpat"

print("Success.")
print(f"The following pointers are blacklisted and were not deleted: {blacklist_ptrs}")
print("Use `#import {example_fname}` in patches to apply deletions to the ROM.")
print("")
print("If on compilation you get a BufferOverflowException, you have found a known bug in Star Rod 0.2.0.")
print("To 'fix' it, edit the generated `import/delete_all_og_data/file_label.mpat` file and comment things")
print("out until SR stops throwing the error.")
