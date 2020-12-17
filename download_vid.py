import requests
import re
from urllib import parse

from bs4 import BeautifulSoup


URL_BASE  = "https://sas.zoom.us/rec/play/A-1ukwuBhLcoE_SImJhNwVHGtPlOzbWIv7St" \
            "vWJSCI33BUmGvUvMMpo-BLygBQUYVdwkY2zATIPaUKG9.CQu9kjxMjT2wR8S6?continueMode=true" \
            "&_x_zm_rtaid=V2IYpjoKQPSHUhtE3eC0Zw.1608031401246" \
            ".d485b92161a6ee6a103fc55a9211a378&_x_zm_rhtaid=14"


s = requests.Session()
s.headers.update({
    "User-Agent":"Mozilla/5.0 (Macintosh; "
                "Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/86.0.4240.198 Safari/537.36",
    "Refer":"https://sas.zoom.us/",
    "Accept":"*/*",
        })


def download_file(s, url):
    local_filename = "d1_vid.mp4"
    params  = dict(parse.parse_qsl(parse.urlsplit(url).query))
    r = s.get(url, stream=True, params = params)
    if r.status_code == 200:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1920 * 1200):
                f.write(chunk)
        return f"Путь к скаченному файлу: {local_filename}"
    return f"Ошибка {r.status_code}"


def get_vid_url(s: requests.session, url: str) -> str:
    r = s.get(url)
    pattern = re.compile(r"viewMp4Url: '(.*)',\ngallaryMp4Url")
    url = pattern.findall(r.text)[0]
    return url


def main():
    global s, URL_BASE
    url = get_vid_url(s, URL_BASE)
    print(download_file(s, url))


if __name__ == '__main__':
    main()
