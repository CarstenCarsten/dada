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

def are_identical(leftfile, rightfile):
    left_md5 = get_md5_set(leftfile)
    right_md5 = get_md5_set(rightfile)
    if collections.Counter(left_md5) == collections.Counter(right_md5):
        print('filelists contain same hashes')
    else:
        print('filelists have different hashes!')
        show_difference(left_md5, right_md5, leftfile, rightfile)

def move_file_into_mem(filename):
    thelist = []
    with open(filename, 'r', encoding='utf-8') as file_handle:
        for line in file_handle.readlines():
            splits = line.split(';')
            thelist.append((splits[0], splits[1], splits[2].rstrip('\n').rstrip('\r\n')))
    return thelist


def are_left_in_right(leftfile, rightfile):
    leftlist = move_file_into_mem(leftfile)
    rightlist = move_file_into_mem(rightfile)
    i = 0
    for entry in leftlist:
        i = i + 1
        found = False
        for candidate in rightlist:
            if candidate[0] == entry[0] and candidate[1] == entry[1] and candidate[2] == entry[2]:
                found = True
                break
        if not found:
            print(f' Missing : {entry[0]}  {entry[1]}  {entry[2]}')
    print(f'Processed {i} entries')


def find_needle_in_haystack():
    # https://stackoverflow.com/questions/26712949/python-best-way-to-find-similar-images-in-a-directory
    # https://github.com/jterrace/pyssim
    # 
	None
