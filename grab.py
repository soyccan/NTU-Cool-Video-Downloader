import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from getpass import getpass

sess = requests.session()

course_id = 1804

def video_filter(link_name):
    '''
    Determine whether `link_name` is a video link.
    Should return `False` if `link_name` is a link of pdf, external resources, etc.
    '''
    return link_name


def login():
    global course_id
    course_id = input('Course ID: ')

    page = sess.get('https://cool.ntu.edu.tw/login/saml').text
    soup = BeautifulSoup( page[page.find('<form'):page.find('</form>')+7], 'html.parser' )
    payload = {}
    for data in soup.find_all('input'):
        if 'UsernameTextBox' in data.get('name'):
            payload[data.get('name')] = input('Username: ').strip()
        elif 'PasswordTextBox' in data.get('name'):
            payload[data.get('name')] = getpass('Password: ')
        else:
            payload[data.get('name')] = data.get('value')

    url = 'https://adfs.ntu.edu.tw' + soup.form.get('action')
    soup = BeautifulSoup( sess.post(url, data=payload).text, 'html.parser' )
    payload = {'SAMLResponse': soup.input.get('value')}
    url = 'https://cool.ntu.edu.tw/login/saml'
    sess.post(url, data=payload)


def download():
    urls_vid = []

    soup = BeautifulSoup( sess.get(f'https://cool.ntu.edu.tw/courses/{course_id}/modules').text, 'html.parser' )
    idx = 0
    for block in soup.findAll('li', id=lambda s: s and s.startswith('context_module_item')):
        if block.span['title'] == 'External Tool':
            item_type = 'ext_tool'
        elif block.span['title'] == 'Attachment':
            item_type = 'attachment'
        else:
            item_type = None

        if item_type:
            for aaa in block.findAll('a', title=video_filter):
                urls_vid.append({'url': aaa.attrs['href'], 'title': aaa.text.strip('\n '), 'index': idx, 'type': item_type})
                idx += 1

    print('index. #type [title](URL)')
    for item in urls_vid:
        print('{:2}. #{:10} [{:^20}]({})'.format(item['index'], item['type'], item['title'], item['url']))
    chosen = list(map(int, input('Enter indices of items you want to download, separated by spaces: ').split(' ')))

    get_url = lambda x: f'https://lti.dlc.ntu.edu.tw/api/v1/courses/{course_id}/videos/{x}'
    for item in urls_vid:
        if item['index'] not in chosen:
            continue
        url = item['url']
        soup = BeautifulSoup( sess.get('https://cool.ntu.edu.tw'+url).text, 'html.parser' )
        if item['type'] == 'ext_tool':
            # assume it's a video
            payload = { data.get('name') : data.get('value') for data in soup.find_all('input') }
            vid = int( sess.post(soup.form.get('action'), data=payload, allow_redirects=False).headers['location'].split('?')[0].split('/')[-1] )
            j = json.loads(sess.get(get_url(vid)).text)
            print(f'Start Downloading {j["video"]["title"]}.mp4 ... ...    ', end='', flush=True)
            with open(j['video']['title'].replace('/','-') + '.mp4', 'wb') as f:
                f.write(sess.get(j['video']['url']).content)
            print('Finished !', flush=True)

        elif item['type'] == 'attachment':
            content = soup.find(id='content')
            a = content.find('a')
            title = content.find('h2').text
            print(f'Start Downloading {title} ... ...    ', end='', flush=True)
            with open(title, 'wb') as f:
                f.write(sess.get('https://cool.ntu.edu.tw' + a.attrs['href']).content)
            print('Finished !', flush=True)
        # input('Press Enter To Continue ...')


if __name__ == '__main__':
    login()
    download()
