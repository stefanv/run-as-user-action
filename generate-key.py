"""
Generate and install SSH key in ~/.ssh/authorized_keys
"""

import sys
import os
import subprocess
import shutil
import shlex


if not len(sys.argv) == 3:
    print('Usage: authorize-key.py [key-file-name] [user-name]')
    sys.exit(1)


_, key_fn, user = sys.argv


# Generate key, if it does not exist
if not os.path.exists(key_fn):
    cmd = [
        'ssh-keygen',
        '-b', '1024',
        '-t', 'rsa',
        '-f', key_fn,
        '-q',
        '-N', ''
    ]
    print('$', shlex.join(cmd))
    subprocess.run(cmd)


ssh_dir = os.path.expanduser(f'~{user}/.ssh')
if ssh_dir.startswith('~'):
    print(f'Cannot find user {user}. Aborting.')
    sys.exit(1)
authorized_keys_fn = os.path.join(ssh_dir, 'authorized_keys')

if not os.path.exists(ssh_dir):
    os.mkdir(ssh_dir)


# Install key in authorized_users
with open(f'{key_fn}.pub') as f:
    key = f.read()

if os.path.exists(authorized_keys_fn):
    authorized_keys = open(authorized_keys_fn).read()
else:
    authorized_keys = ''

if not key in authorized_keys:
    print(f'Installing [{key_fn}] into [{authorized_keys_fn}]')
    authorized_keys += key
    with open(authorized_keys_fn, 'w') as f:
        f.write(authorized_keys)
else:
    print(f'Existing key found in [{authorized_keys_fn}]')


# Set SSH file permissions
shutil.chown(ssh_dir, user=user, group=user)
os.chmod(ssh_dir, 0o700)
os.chmod(authorized_keys_fn, 0o644)
