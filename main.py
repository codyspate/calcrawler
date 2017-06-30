
import threading
from queue import Queue
from spider import Spider
import tkinter
from tkinter import ttk
from domain import *
from general import *


class Crawler(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        self.queue_count = tkinter.IntVar()
        self.crawled_count = tkinter.IntVar()
        self.pdf_count = tkinter.IntVar()
        self.webpage_count = tkinter.IntVar()
        self.media_count = tkinter.IntVar()
        self.error_count = tkinter.IntVar()


        self.init_gui()


    def init_gui(self):
        self.root.title("Crawler")
        self.grid(column=0, row=0, sticky='nsew')

        self.url = ttk.Entry(self, width=30)
        self.url.grid(column=1, row=1)

        self.num_crawlers = ttk.Entry(self, width=5)
        self.num_crawlers.insert(0, "16")
        self.num_crawlers.grid(column=1, row=2)

        ttk.Label(self, text='Crawler').grid(column=0, row=0,
            columnspan=4)
        ttk.Label(self, text='Base URL').grid(column=0, row=1)
        ttk.Label(self, text='Number of crawlers (default 16)').grid(column=0, row=2)
        self.start_button = ttk.Button(self, text='Start Crawl', command=self.start)
        self.start_button.grid(column=0, row=3, columnspan=4)

        ttk.Separator(self, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew')

        ttk.Label(self, text='Queue').grid(column=0, row=5)
        ttk.Label(self, textvariable=self.queue_count).grid(column=1, row=5)

        ttk.Label(self, text='Crawled').grid(column=0, row=6)
        ttk.Label(self, textvariable=self.crawled_count).grid(column=1, row=6)

        ttk.Label(self, text='PDF').grid(column=0, row=7)
        ttk.Label(self, textvariable=self.pdf_count).grid(column=1, row=7)

        ttk.Label(self, text='Webpages').grid(column=0, row=8)
        ttk.Label(self, textvariable=self.webpage_count).grid(column=1, row=8)

        ttk.Label(self, text='Media').grid(column=0, row=9)
        ttk.Label(self, textvariable=self.media_count).grid(column=1, row=9)

        ttk.Label(self, text='Errors (see log)').grid(column=0, row=10)
        ttk.Label(self, textvariable=self.error_count).grid(column=1, row=10)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def start(self):
        self.HOMEPAGE = self.url.get()
        if not '://' in self.HOMEPAGE:
            self.HOMEPAGE = "http://" + self.HOMEPAGE + '/'
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)
        self.PROJECT_NAME = self.DOMAIN_NAME[:self.DOMAIN_NAME.index('.')]
        self.QUEUE_FILE = 'projects/' + self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = 'projects/' + self.PROJECT_NAME + '/crawled.txt'
        self.SUMMARY_FILE = 'projects/' + self.PROJECT_NAME + '/summary.txt'
        self.NUMBER_OF_THREADS = int(self.num_crawlers.get())
        self.queue = Queue()
        self.spider = Spider(self.PROJECT_NAME, self.HOMEPAGE, self.DOMAIN_NAME)
        self.create_workers()
        self.crawl()


    # Create worker threads (will die when main exits)
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()


    # Do the next job in the queue
    def work(self):
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    def update_nums(self):
        data = self.spider.data()
        self.queue_count.set(data['queue'])
        self.crawled_count.set(data['crawled'])
        self.pdf_count.set(data['pdf'])
        self.webpage_count.set(data['webpage'])
        self.media_count.set(data['media'])
        self.error_count.set(data['error'])
        self.update()


    def crawl(self):
        queued_links = file_to_set(self.QUEUE_FILE)        
        while len(queued_links) > 0:
            self.update_nums()
            queued_links = file_to_set(self.QUEUE_FILE)
            for link in queued_links:
                self.queue.put(link)
                print(link)
            self.queue.join()
            print(str(len(queued_links)) + ' links in the queue')


if __name__ == '__main__':
    root = tkinter.Tk()
    Crawler(root)
    root.mainloop()


# #PROJECT_NAME = input("Project Name: ")
# HOMEPAGE = input('URL: ')
# if not '://' in HOMEPAGE:
#     HOMEPAGE = "http://" + HOMEPAGE + '/'
# DOMAIN_NAME = get_domain_name(HOMEPAGE)
# PROJECT_NAME = DOMAIN_NAME[:DOMAIN_NAME.index('.')]
# QUEUE_FILE = 'projects/' + PROJECT_NAME + '/queue.txt'
# CRAWLED_FILE = 'projects/' + PROJECT_NAME + '/crawled.txt'
# SUMMARY_FILE = 'projects/' + PROJECT_NAME + '/summary.txt'
# NUMBER_OF_THREADS = int(input("Number of threads: ") or 16)
# queue = Queue()
# Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
# def create_workers():
#
#     for _ in range(NUMBER_OF_THREADS):
#         t = threading.Thread(target=work)
#         t.daemon = True
#         t.start()
#
#
# # Do the next job in the queue
# def work():
#     while True:
#         url = queue.get()
#         Spider.crawl_page(threading.current_thread().name, url)
#         queue.task_done()
#
#
# # Each queued link is a new job
# # def create_jobs():
# #     for link in file_to_set(QUEUE_FILE):
# #         queue.put(link)
# #     queue.join()
# #     crawl()
#
#
# # Check if there are items in the queue, if so crawl them
# # def crawl():
# #     queued_links = file_to_set(QUEUE_FILE)
# #     if len(queued_links) > 0:
# #         print(str(len(queued_links)) + ' links in the queue')
# #         create_jobs()
#
# def crawl():
#     queued_links = file_to_set(QUEUE_FILE)
#     while len(queued_links) > 0:
#         queued_links = file_to_set(QUEUE_FILE)
#         for link in queued_links:
#             queue.put(link)
#             print(link)
#         queue.join()
#         print(str(len(queued_links)) + ' links in the queue')
#
#
#
# create_workers()
# crawl()
