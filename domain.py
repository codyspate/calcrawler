from urllib.parse import urlparse


def get_domain_name(url):
    try:

        results = get_sub_domain_name(url)
        dots = results.count('.')
        results = results.split('.')
        string = ''
        for i in range(dots+1):
            string += results[((dots-i)+1) *-1]
            if i < dots-1:
                string += '.'
        return string
        #return results[-3] + '.' + results[-2] + '.' + results[-1]
    except:
        return ''


def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
