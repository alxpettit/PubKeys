#!/bin/env python3

from subprocess import run
from pathlib import Path
from typing import List

def recurse_over_dir(path: Path) -> List[Path]:
    result = []
    if path.stem == '.git':
        return []
    for f in path.iterdir():
        if f.is_dir():
            result += recurse_over_dir(f)
        else:
            result += [f]
    return result

for path in recurse_over_dir(Path('.')):
    if path.is_file():
        print(f'Examining {path}')
        p = run(['file', path], capture_output=True)
        output = p.stdout.decode('utf-8').lower()
        if 'private key' in output:
            print(f'!!! WARNING! {path} contains a private key! Do not commit.')
            exit(1)
        elif 'public key' in output:
            print(f'Public key as expected.')
        elif 'ascii' in output:
            pass
        else:
            print(f'Unknown output: {output}')

