#!/usr/bin/env python
import re, urllib2, operator

BASE_URL = "https://s3-us-west-2.amazonaws.com/simple-crawl-4rBsUnE1wl"

class Page():
    def __init__(self, url):
        self.url = url
        self.ctr = 1
        self.is_dead = False
        self.error_code = 0
        self.error_reason = ''

initial_page = Page(BASE_URL + '/' + 'page_0.html')
crawled_filenames = {} 
dead_filenames = {}
all_filenames = {}

def parse_url(myurl):
#    print "Processing: {}".format(myurl)
    if myurl in dead_filenames.keys(): 
        dead_filenames[myurl].ctr += 1
        return
    req = urllib2.Request(myurl)
    try: 
        data = urllib2.urlopen(req)
        for i in re.findall('''href=["'](.[^"']+)["']''', data.read(), re.I):
            i = re.sub(r"\?.+", "", i)
            i = BASE_URL + '/' + i
            if i in crawled_filenames.keys():
                crawled_filenames[i].ctr += 1
            else:
                crawled_filenames[i] = Page(i)
                parse_url(i)
    except urllib2.HTTPError as e:
        myurl = re.sub(r"\?.+", "", myurl)
        if myurl not in dead_filenames.keys():
            dead_filenames[myurl] = Page(myurl)
            dead_filenames[myurl].is_dead = True
            dead_filenames[myurl].code = e.code
            dead_filenames[myurl].reason = e.reason
        exit


def write_results(input_dict, filename):
    with open(filename, 'w') as f: 
        for value in input_dict.values():
            print "url: {}, ctr: {}".format(value.url, value.ctr)
            f.write(value.url + ':\t' + str(value.ctr) + '\n')

def prep_dict_for_sorting(dict_):
    for key in dict_.keys():
        all_filenames[key] = dict_[key].ctr


parse_url(BASE_URL + '/' + 'page_0.html')

# We need to include both good and dead pages when sorting  even though in this
# case a visual inspection reveals all the dead pages are referred to only once
prep_dict_for_sorting(crawled_filenames)
prep_dict_for_sorting(dead_filenames)
sorted_list = sorted(all_filenames.items(), key=operator.itemgetter(1))
sorted_list.reverse()


write_results(crawled_filenames, 'Task_1')
write_results(dead_filenames, 'Task_2')
with open('Task_3', 'w') as task3:
        for i in range(3):
            task3.write(sorted_list[i][0] + ':\t' + str(sorted_list[i][1]) + '\n')
