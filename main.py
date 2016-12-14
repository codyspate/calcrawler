import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

#PROJECT_NAME = input("Project Name: ")
HOMEPAGE = input('URL: ')
if not '://' in HOMEPAGE:
    HOMEPAGE = "http://" + HOMEPAGE + '/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
PROJECT_NAME = DOMAIN_NAME[:DOMAIN_NAME.index('.')]
QUEUE_FILE = 'projects/' + PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = 'projects/' + PROJECT_NAME + '/crawled.txt'
SUMMARY_FILE = 'projects/' + PROJECT_NAME + '/summary.txt'
NUMBER_OF_THREADS = int(input("Number of threads: ") or 16)
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():

    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
