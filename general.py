import os, shutil


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join('projects', os.path.join(project_name , 'queue.txt'))
    crawled = os.path.join('projects', os.path.join(project_name,"crawled.txt"))
    summary = os.path.join('projects', os.path.join(project_name, "summary.txt"))
    errors = os.path.join('projects', os.path.join(project_name, "errors.txt"))
    media = os.path.join('projects', os.path.join(project_name, "media.txt"))
    #ext_link_errors = os.path.join('projects', os.path.join(project_name, "ext_link_errors.txt"))
    delete_file_contents(queue)
    delete_file_contents(crawled)
    delete_file_contents(summary)
    delete_file_contents(errors)
    delete_file_contents(media)
    #delete_file_contents(ext_link_errors)
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(summary):
        t = "PDF count:     \nHTML/HTM count:     \nMedia files:     \nOther:     \nErrors:     \n\nTotal size:     "
        write_file(summary, t)
    if not os.path.isfile(errors):
        write_file(errors, '')
    if not os.path.isfile(media):
        write_file(media, '')
    # if not os.path.isfile(ext_link_errors):
    #     write_file(ext_link_errors, '')


# Create a new file
def write_file(path, data):
    try:
        with open(path, 'w') as f:
            f.write(data)
    except Exception as e:
        print(str(e))


# Add data onto an existing file
def append_to_file(path, data):
    try:
        with open(path, 'a') as file:
            file.write(data + '\n')
    except Exception as e:
        print(str(e))


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()

def update_summary(path, pname, url, pdf, html, media, other, errors, pages, size, queue, crawled):
    delete_file_contents(path)
    with open(path, 'a') as f:
        f.write("Cal Crawler v1.0\n\n")
        f.write("Website: " + pname + '\n')
        f.write("URL: "+ url + '\n\n')
        f.write("PDF count: " + pdf + "\nHTML/HTM count: " + html + "\nMedia files: " + media + "\nOther: " + other + "\nErrors: " + errors + "\n\nTotal Number of Pages: " + pages + "\nTotal size: " + size  + " MB\n\n")
        f.write('Queue: ' + queue + '\nCrawled:  ' + crawled + "\n\n")
# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            fields = line.split("|")
            fields[1] = fields[1].replace('\n', '')
            results.add((fields[0], fields[1]))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name, mode="w"):
    try:
        with open(file_name,mode) as f:
            for l in sorted(links, key=lambda k: k[0]):
                f.write(l[0] + "|" + l[1] + "\n") #pip delimit source and link

    except Exception as e:
        print(str(e))

def media_to_file(links, file_name, mode="r+"):
    try:
        with open(file_name,mode) as f:
            for item in sorted(med, key=lambda k: k['link']):
                f.write('On Page: ' +  item[0]+ "   ----------->   Item: " + item[1])
    except Exception as e:
        print(str(e))

def make_file_readable(file_name):
    results = set()
    try:
        with open(file_name, "r") as f:
            for line in f:
                fields = line.split("|")
                fields[1] = fields[1].replace('\n', '')
                results.add((fields[0], fields[1]))
    except Exception as e:
        print(str(e))
    delete_file_contents(file_name)
    with open(file_name, "a") as f:
        for l in sorted(results, key=lambda k: k[0]):
            f.write("Source: " + l[0] + "\n")
            f.write("Data: " + l[1] + "\n\n")
