


def are_all_local_files_in_remote():
    local_md5_values = list()
    with open('local_filelist.csv','r', encoding='utf-8') as local_file_handle:
        for line in local_file_handle.readlines():
            local_md5_values.append(line.split(';')[0])
    print(local_md5_values)

