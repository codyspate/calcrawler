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
    delete_file_contents(queue)
    delete_file_contents(crawled)
    delete_file_contents(summary)
    delete_file_contents(errors)
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(summary):
        t = "PDF count:     \nHTML/HTM count:     \nMedia files:     \nOther:     \nErrors:     \n\nTotal size:     "
        write_file(summary, t)
    if not os.path.isfile(errors):
        write_file(errors, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


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
        f.write('Queue: ' + queue + '\nCrawled:  ' + crawled)
# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")
