#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import MeCab
import re


class Kscraper:
    def __init__(self):
        self.raw = ""
        self.title = []
        self.body = []
        self.wakati = MeCab.Tagger("-Owakati")

    def scrape(self, url):
        # raw
        self.raw = requests.get(url)
        soup = BeautifulSoup(self.raw.content, "html.parser")

        # title
        title = soup.select("h1")[0].get_text()
        self.title = self.wakati.parse(title).split()

        # body
        bodys = soup.find(class_="read__content").find_all("p")
        for body in bodys:
            bodyStr = str(body)
            # Baca juga まで読む
            if 'Baca juga' in bodyStr:
                break
            # html タグ除去
            bodyStr = BeautifulSoup(bodyStr, "lxml").text
            # 形態素解析
            parsed = self.wakati.parse(bodyStr).split()
            self.body.extend(parsed)


def debug():
    # 以下のページのタイトルを取得する
    url = 'https://nasional.kompas.com/read/2023/03/07/12361791/ppatk-ungkap-transaksi-ganjil-pejabat-pajak-selain-rafael-jumlahnya-rp-500?_ga=2.245943364.1589312895.1678169976-1637943181.1678169973'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.select("h1")[0].get_text()
    print(title)

    # 形態素解析を行う
    wakati = MeCab.Tagger("-Owakati")
    parsed = wakati.parse(title).split()
    print(parsed)


def main():
    # debug()
    ks = Kscraper()
    url = 'https://nasional.kompas.com/read/2023/03/07/12361791/ppatk-ungkap-transaksi-ganjil-pejabat-pajak-selain-rafael-jumlahnya-rp-500?_ga=2.245943364.1589312895.1678169976-1637943181.1678169973'
    ks.scrape(url)
    # title
    print('#### Title ####')
    print(ks.title)
    print('#### Body ####')
    print(ks.body)


if __name__ == '__main__':
    main()
