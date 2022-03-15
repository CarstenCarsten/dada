import os
import config
import hashlib
import datetime

def find_files_with_unwanted_chars_in_name(dirName):
    configset = set(config.configuration['valid_chars'])
    
    for (dirpath, _, filenames) in os.walk(dirName):
        for fileName in filenames:
            if not set(fileName).issubset(configset):
                print(os.path.join(dirpath, fileName))

def create_md5_file_list(dirname):
    filename = 'local_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '_filelist.csv'
    with open(filename, 'w+',encoding='utf-8') as filelisthandle:
        # Second parameter are the foldernames
        for (dirpath, _, filenames) in os.walk(dirname):
            for filename in filenames:
                file_with_path = os.path.join(dirpath, filename)
                md5_hash = hashlib.md5()
                with open(file_with_path, "rb") as handle:
                    while True:
                        block = handle.read(10485760)
                        if block:
                            md5_hash.update(block)
                        else:
                            break
                digest = md5_hash.hexdigest()
                localdirpath = dirpath[len(dirname)-1:].replace('\\','/')
                if localdirpath[-1] != '/':
                    localdirpath = localdirpath + '/'
                filelisthandle.write(f'{digest};{localdirpath};{filename}\n')

#            print(os.path.join(dirpath, fileName))

