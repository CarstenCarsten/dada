import os
import config
import hashlib

def find_files_with_unwanted_chars_in_name(dirName):
    configset = set(config.configuration['valid_chars'])
    
    for (dirpath, _, filenames) in os.walk(dirName):
        for fileName in filenames:
            if not set(fileName).issubset(configset):
                print(os.path.join(dirpath, fileName))

def create_md5_file_list(dirname):
    with open('local_filelist.csv', 'w+') as filelisthandle:
        # Second parameter are the foldernames
        for (dirpath, _, filenames) in os.walk(dirname):
            for filename in filenames:
                file_with_path = os.path.join(dirpath, filename)
                md5_hash = hashlib.md5()
                with open(file_with_path, "rb") as handle:
                    md5_hash.update(handle.read())
                digest = md5_hash.hexdigest()
                localdirpath = dirpath[len(dirname)-1:].replace('\\','/') + '/'
                filelisthandle.write(f'{digest};{localdirpath};{filename}\n')

#            print(os.path.join(dirpath, fileName))

