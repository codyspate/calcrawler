from urllib.request import urlopen
from urllib.parse import quote
from link_finder import LinkFinder
from socket import timeout
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    summary_file = ''
    errors_file = ''
    #ext_link_errors_file = ''
    num_pdf = 0
    num_html = 0
    num_media = 0
    num_other = 0
    num_errors = 0
    #num_broken_ext_links = 0
    total_size = 0
    pages = 0
    queue = set()
    crawled = set()
    media = set()

    '''
        links are stored in a tuple as (page_it_was_on, the_link_itself)
    '''

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = ("ROOT", base_url)
        Spider.domain_name = domain_name
        Spider.queue_file = 'projects/' + Spider.project_name + '/queue.txt'
        Spider.crawled_file = 'projects/' + Spider.project_name + '/crawled.txt'
        Spider.summary_file = 'projects/' + Spider.project_name + '/summary.txt'
        Spider.errors_file = 'projects/' + Spider.project_name + '/errors.txt'
        Spider.media_file = 'projects/' + Spider.project_name + '/media.txt'
        #Spider.ext_link_errors_file = 'projects/' + Spider.project_name + '/ext_link_errors.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir("projects/" + Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url[1])
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.media = file_to_set(Spider.media_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url[1] not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url[1])
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            try:
                Spider.queue.discard(page_url)
            except KeyError as e:
                print(str(e))
            Spider.crawled.add(page_url)
            Spider.update_files()

    def data(self):
        return ({
            "queue": len(Spider.queue),
            "crawled": len(Spider.crawled),
            "pdf": Spider.num_pdf,
            "webpage": Spider.pages,
            "media": Spider.num_media,
            "error": Spider.num_errors
        })

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        Spider.pages += 1
        html_string = ''
        try:
            response = urlopen(page_url[1], timeout=10)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                if not "/#" in page_url[1]:
                    Spider.total_size += (len(html_bytes)/1000)
                html_string = html_bytes.decode("utf-8", errors='ignore')
            finder = LinkFinder(Spider.base_url[1], page_url[1])
            finder.feed(html_string)

            if 'pdf' in response.info()['Content-Type']:
                Spider.num_pdf += 1
            media_types = ['.mp3', '.jpg', '.png', '.mpeg', '.ico', '.wmv', '.avi', '.mov', '.mng', '.gif', '.bmp', '.jpeg']
            for t in media_types:
                if t in page_url[1].lower():
                    Spider.num_media += 1
                    break
            html_types = ['.html', '.htm', '.xhtml', '.asp', '.aspx', '.php', '.mhtml']
            for t in html_types:
                if t in page_url[1].lower() or (not page_url[1][-4] == '.' and not page_url[1][-5] == '.'):
                    Spider.num_html += 1
                    break

            response.close()
        except Exception as e:
            print(str(e))
            append_to_file(Spider.errors_file, str(e) + '\n\tON PAGE: ' + page_url[0] + '\n\tLink: ' + page_url[1] + "\n")
            Spider.num_errors += 1
            return set()

        Spider.num_media += finder.getImgCount()
        Spider.total_size += (finder.getImgSize()/1000)
        Spider.add_media(finder.getMedia())

        return finder.page_links()

    def add_media(links):
        for img in links:
            if img[1] in Spider.media:
                continue
            lst = list(img)
            lst[1] = quote(lst[1], safe="%/:=&?~+!$,;'@()*[]#")
            img = tuple(lst)
            Spider.media.add(img)


    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            t_queue = Spider.queue.copy()
            t_crawled = Spider.crawled.copy()
            if any(url[1] == item[1] for item in t_queue) or any(url[1] == item[1] for item in t_crawled):
                continue
            if not Spider.domain_name in get_domain_name(url[1]) and not url[1][0] == '/':
                continue
            lst = list(url)
            lst[1] = quote(lst[1], safe="%/:=&?~+!$,;'@()*[]#")
            if '%20' in lst[1][-3:]:
                lst[1] = lst[1][:-3]
            url = tuple(lst)
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        a = set()
        b = set()
        c = set()
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.media, Spider.media_file)
        size = Spider.total_size/1000
        update_summary(Spider.summary_file, Spider.project_name, Spider.base_url[1], str(Spider.num_pdf), str(Spider.num_html), str(Spider.num_media), str(Spider.num_other), str(Spider.num_errors), str(Spider.pages), str.format("{:.3f}", size), str(len(Spider.queue)), str(len(Spider.crawled)))
