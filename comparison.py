import collections

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

def show_missing(has_less, has_more, less_filename, more_filename):
    difference = has_more - has_less
    with open(more_filename, 'r', encoding='utf-8') as file_handle:
        for line in file_handle.readlines():
            if line.split(';')[0] in has_more:
                if line.endswith('\r\n') or line.endswith('\n'):
                    print(line, end='')
                else:
                    print(line)

def show_difference(local_md5, remote_md5, local_filename, remote_filename):
    if len(local_md5) > len(remote_md5):
        show_missing(remote_md5, local_md5, remote_filename, local_filename)
    elif len(remote_md5) > len(local_md5):
        show_missing(local_md5, remote_md5, local_filename, remote_filename)
    else:
        print('Both filelists have same length')

def are_all_local_files_in_remote():
    local_md5 = get_md5_set('local_filelist.csv')
    remote_md5 = get_md5_set('adrive_filelist.csv')

    diff = local_md5 - remote_md5
    if len(diff) == 0:
        print('All local files are in remote.')
    else:
        print('The difference is:')
        print(diff)

def are_identical():
    local_filename = 'local_filelist.csv'
    remote_filename = 'adrive_filelist.csv'
    local_md5 = get_md5_set(local_filename)
    remote_md5 = get_md5_set(remote_filename)
    if collections.Counter(local_md5) == collections.Counter(remote_md5):
        print('filelists contain same hashes')
    else:
        print('filelists have different hashes!')
        show_difference(local_md5, remote_md5, local_filename, remote_filename)
	