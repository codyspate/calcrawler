from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    summary_file = ''
    num_pdf = 0
    num_html = 0
    num_media = 0
    num_other = 0
    num_errors = 0
    total_size = 0
    pages = 0
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = 'projects/' + Spider.project_name + '/queue.txt'
        Spider.crawled_file = 'projects/' + Spider.project_name + '/crawled.txt'
        Spider.summary_file = 'projects/' + Spider.project_name + '/summary.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir("projects/" + Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            links = Spider.gather_links(page_url)
            Spider.add_links_to_queue(links)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        Spider.pages += 1
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                Spider.total_size += (len(html_bytes)/1000)
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            if ".pdf" in page_url.lower():
                Spider.num_pdf += 1
            media_types = ['.mp3', '.jpg', '.png', '.mpeg', '.ico', '.wmv', '.avi', '.mov', '.mng', '.gif', '.bmp', '.jpeg']
            for t in media_types:
                if t in page_url.lower():
                    Spider.num_media += 1
                    break
            html_types = ['.html', '.htm', '.xhtml', '.asp', '.aspx', '.php', '.mhtml']
            for t in html_types:
                if t in page_url.lower() or (not page_url[-4] == '.' and not page_url[-5] == '.'):
                    Spider.num_html += 1
                    break

        except Exception as e:
            print(str(e))
            Spider.num_errors += 1
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if not Spider.domain_name in get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        size = Spider.total_size/1000
        update_summary(Spider.summary_file, Spider.project_name, Spider.base_url, str(Spider.num_pdf), str(Spider.num_html), str(Spider.num_media), str(Spider.num_other), str(Spider.num_errors), str(Spider.pages), str.format("{:.3f}", size), str(len(Spider.queue)), str(len(Spider.crawled)))
