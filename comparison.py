
def get_md5_set(filename):
    md5_list = list()
    print(f'Reading {filename}.')
    with open(filename,'r', encoding='utf-8') as file_handle:
        for line in file_handle.readlines():
            md5_list.append(line.split(';')[0])    
    md5_set = set(md5_list)
    if len(md5_list) != len(md5_set):
        print(f'There are files with same md5 checksum in {filename}')
    return md5_set

def are_all_local_files_in_remote():
    local_md5 = get_md5_set('local_filelist.csv')
    remote_md5 = get_md5_set('adrive_filelist.csv')

    diff = local_md5 - remote_md5
    if len(diff) == 0:
        print('All local files are in remote.')
    else:
        print('The difference is:')
        print(diff)

