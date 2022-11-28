import argparse
import os

import enlighten
import requests
from bandcamp_dl.bandcamp import Bandcamp
from bandcamp_dl.bandcampdownloader import BandcampDownloader
from bs4 import BeautifulSoup

args = argparse.ArgumentParser()
args.add_argument("--after", default=None)
opts = args.parse_args()

base_url = "https://goosetheband.bandcamp.com"
content = requests.get(base_url).content

soup = BeautifulSoup(requests.get(base_url).content, "html.parser")
all_urls = [
    f"{base_url}{x['href']}" for x in soup.select("li.music-grid-item > a:nth-child(1)")
]

urls = []
if not opts.after:
    urls = all_urls
else:
    for url in all_urls:
        if opts.after in url:
            break

        urls.append(url)


dl = BandcampDownloader(
    template="%{artist}/%{album}/%{track} - %{title}",
    directory=os.getcwd(),
    overwrite=False,
    embed_lyrics=False,
    grouping=False,
    embed_art=False,
    no_slugify=False,
    ok_chars="-_~",
    space_char="-",
    ascii_only=False,
    keep_space=True,
    keep_upper=True,
    debugging=False,
    urls=urls,
)

manager = enlighten.get_manager()
pbar = manager.counter(total=len(urls))

bc = Bandcamp()
for url in urls:
    dl.start(bc.parse(url))
    pbar.update()

manager.stop()
