from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen

class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.media = set()
        self.img_size = 0
        self.img_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
        elif tag == 'img':
            for (attribute, value) in attrs:
                if attribute == 'src':
                    try:
                        url = parse.urljoin(self.base_url, value)
                        res = urlopen(url)
                        self.media.add(url)
                        self.img_count+=1
                        self.img_size += len(res.read())
                        res.close()
                    except Exception as e:
                        print(str(e))

    def getMedia(self):
        return self.media

    def getImgSize(self):
        return self.img_size

    def getImgCount(self):
        return self.img_count

    def page_links(self):
        return self.links

    def error(self, message):
        pass
