import configparser
import requests
import json

allfiles = []

def walk_dir(dir, session):
    print('walking ' + dir)
    postHeaders = {}
    payload = {
        'json':'{"dir":"' + dir + '"}'
    }
    response = session.post('https://www32.adrive.com/API', data=payload, headers=postHeaders)

    files_dict = json.loads(response.text)

    for file_line in files_dict['files']:
        if file_line[3] == 'D':
            walk_dir(f'{dir}{file_line[2]}/', session)
        elif file_line[3] == 'F':
            payload = {
                'json':'{"fid":"' + file_line[0] + '"}'
            }
            while True:
                try:
                    response = session.post('https://www32.adrive.com/API/calcMD5Sum', data=payload, headers=postHeaders)
                    break
                except:
                    print('exception, retrying...')
            md5_dict = json.loads(response.text)
            md5_digest = md5_dict['md5']
            print(f'id {file_line[0]} name {file_line[2]} type {file_line[3]} md5 {md5_digest}')
            allfiles.append((md5_digest, dir, file_line[2]))

def login():
    secretsconfig = configparser.ConfigParser()
    secretsconfig.read('secrets.ini')

    session = requests.Session()
    postHeaders = {}
    payload = {'login[referrer]':'',
        'login[email]':secretsconfig['adrive']['user'],
        'login[passwrd]':secretsconfig['adrive']['password']
        }
    session.post('https://www.adrive.com/login/login', data=payload, headers=postHeaders)
    return session


def login_and_walk_dir():
    session = login()

    walk_dir('/', session)

    with open('adrive_filelist.csv','w+',encoding='utf-8') as handle:
        for f in allfiles:
            handle.write(f'{f[0]};{f[1]};{f[2]}\n')
