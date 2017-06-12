import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.middle = tk.Frame(self)
        self.bottom = tk.Frame(self)
        self.stats = tk.Frame(self)
        self.stats.pack( side = 'bottom' )
        self.bottom.pack( side = 'bottom' )
        self.middle.pack( side = 'bottom' )
        self.ready = False
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.url_label = tk.Label(self, text="Base URL")
        self.url_label.pack( side = 'left' )
        self.url_field = tk.Entry(self)
        self.url_field.pack( side = 'right' )
        self.threads_label = tk.Label(self.middle, text="Number of Threads")
        self.threads_label.pack( side = 'left' )
        t = tk.StringVar(self)
        t.set('16')
        self.threads_field = tk.Spinbox(self.middle, from_=1, to=100, textvariable=t)
        self.threads_field.pack( side = 'right' )
        self.submit = tk.Button(self.bottom, text="Start", command=lambda : self.start())
        self.submit.pack()

    def start(self):
        self.create_stats_box()
        self.ready = True

    def create_stats_box(self):
        self.stats_box = tk.Listbox(self.stats)
        self.stats_box.insert(1, "Crawling: " + self.url_field.get())
        self.stats_box.pack()

    def get_url(self):
        return self.url_field.get()

    def get_threads(self):
        return self.threads_field.get()

    def show(self, pdf, html, media, other, errors, pages, size, queue, crawled):
        self.stats_box.insert(2, "PDF: " + pdf)
        self.stats_box.insert(3, "HTML: " + html)
        self.stats_box.insert(4, "Media: " + media)
        self.stats_box.insert(5, "Other: " + other)
        self.stats_box.insert(6, "Errors: " + errors)
        self.stats_box.insert(7, "Pages: " + pages)
        self.stats_box.insert(8, "Size: " + size + " MB")
        self.stats_box.insert(9, "Queue: " + queue)
        self.stats_box.insert(10, "Crawled: " + crawled)
