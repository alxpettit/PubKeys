#!/bin/env python3

from pathlib import Path
from subprocess import run

import shutil

for path in Path('/etc/ssh/id').glob('*'):
    name = path.stem
    new_file_name = name + '.pub'
    try:
        shutil.copy(path / "id_rsa.pub", Path('ssh') / new_file_name)
    except:
        print(f'Warning! Failed to copy {path}')


for path in Path('ssh').glob('*'):
    print(f'Examining {path}')
    p = run(['file', path], capture_output=True)
    output = p.stdout.decode('utf-8')
    if 'private' in output:
        print(f'WARNING! {path} contains a private key! Do not commit.')
    elif 'public' in output:
        print(f'Public key as expected.')
    else:
        print(f'Unknown output: {output}')
