from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from PIL import Image
import requests
import instaloader


class InstaLoader:
    def __init__(self, account):
        self.account = account
        self.directory = account

    def get_files(self):
        files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        images, posts = [], []
        for file in files:
            if '.jpg' in file or '.png' in file:
                images.append(file)
            elif '.txt' in file:
                posts.append(file)

        return images, posts

    def check_image(self):
        images, posts = self.get_files()
        rgbs = []
        for image in images:
            r1, g1, b1 = 0, 0, 0
            counter = 0
            myimage = Image.open('{}/{}'.format(self.directory, image))
            pixels = myimage.load()
            x, y = myimage.size
            for i in range(x):
                for j in range(y):
                    counter += 1
                    r, g, b = pixels[i, j]
                    r1 += r
                    g1 += g
                    b1 += b
            rgb = (r1 // counter, g1 // counter, b1 // counter)
            rgbs.append(rgb)
        return rgbs

    def all_words(self):
        images, posts = self.get_files()
        words = ''

        for file in posts:
            f = open('{}/{}'.format(self.directory, file), 'r', encoding="utf-8").read()
            words += f
        return words

    def get_info(self):
        url = 'https://www.instagram.com/{}/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }

        page = requests.get(url.format(self.account), headers)
        content = BeautifulSoup(page.content, 'html.parser')
        meta = content.find('meta', property="og:description")

        return str(meta)[15:len(str(meta)) - 29]

    def get_pictures(self):
        mod = instaloader.Instaloader()
        mod.download_profile(self.account)
