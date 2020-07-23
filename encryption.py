import subprocess
from pathlib import Path


def encrypt(path):
    with open(f'{path}encryptedfiles.txt', 'r', encoding='utf-8') as encrypted_files_list_handle:
        for line in encrypted_files_list_handle.readlines():
            file_location = line.rstrip().replace('\\', '/')
            location_file_to_encrypt = f'{path}{file_location}'
            file_to_encrypt_path = Path(location_file_to_encrypt)
            if file_to_encrypt_path.is_file():
                target_file = f'{path}{file_location}.encrypted'
                target_file_path = Path(target_file)
                if target_file_path.is_file():
                    print(f'{target_file} already exists, skipping.')
                else:
                    print(f'Running gpg for {location_file_to_encrypt}')
                    subprocess.run(['gpg', '--output', target_file, '--symmetric',  '--cipher-algo',  'AES256', location_file_to_encrypt])                
            else:
                print(f'{location_file_to_encrypt} does not exist')

