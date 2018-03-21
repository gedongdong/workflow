import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import sys
from workflow import Workflow
ICON_DEFAULT = 'icon.png'


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('.b_algo h2 a')
    r_list = []
    for i in result:
        r_list.append([i.attrs['href'], i.get_text()])
    return r_list


def main(wf):
    text = sys.argv[1]
    if len(text) <= 0:
        add_not_found(wf)
    else:
        url = 'https://cn.bing.com/search?q='+sys.argv[1]
        html = get_one_page(url)
        content = parse_one_page(html)
        if len(content) > 0:
            for i in content:
                sub = i[0]
                wf.add_item(title=i[1],
                            subtitle=sub,
                            arg=i[0],
                            valid=True,
                            icon=ICON_DEFAULT)
        else:
            add_not_found(wf)
    wf.send_feedback()


def add_not_found(wf):
    wf.add_item(
        title='Not found...',
        subtitle='Please verify the input...',
        arg='Not found',
        valid=True,
        icon='notfound.png'
    )


if __name__ == '__main__':
    wf = Workflow()
    logger = wf.logger
    sys.exit(wf.run(main))

