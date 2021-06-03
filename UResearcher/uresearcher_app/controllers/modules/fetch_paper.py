# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:18:23 2021

@author: benny
"""
from rake_nltk import Rake
import re, os, fitz, math, random,time,json,requests, threading

delaytime_coefficient = 10

class collect_citedby_year_thread(threading.Thread):
    def __init__(self, year, title, id_, thread_counter, container, threadlocker):
        threading.Thread.__init__(self)
        self.year = year
        self.title = title
        self.id_ = id_
        self.thread_counter = thread_counter
        self.container = container
        self.threadlocker = threadlocker
        self.url = "https://academic.microsoft.com/api/search"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", }

    def run(self):
        skip = 0
        thread_list = []
        data = citedby_dataForm_year(self.title, self.id_, self.year, skip)
        proxy = getRandomPrxoy()
        r = send_request(data, proxy, 0)
        if r == "":
            return
        try:
            page_dic = json.loads(r.text)
        except:
            print(str(self.year) + " cannot parse")
        paper_numbers = page_dic["t"]
        # creats thread to collect each page
        for i in range(50):
            if skip >= paper_numbers:
                break
            else:
                data = citedby_dataForm_year(self.title, self.id_, self.year, skip)
                self.threadlocker.acquire()
                j = self.thread_counter[0]
                self.thread_counter[0] += 1
                self.threadlocker.release()
                global proxy_list
                delaytime = get_delaytime(j)
                thread_list.append((Search_thread(i, data, delaytime, self.container, self.threadlocker)))
                skip = skip + 10
        # run all thread
        for t in thread_list:
            t.start()
        # wait for everythread
        for t in thread_list:
            t.join()
        print("collected papers of " + str(self.year))


class collect_query_year_thread(threading.Thread):
    def __init__(self, year, keyword, thread_list, container, threadlocker):
        threading.Thread.__init__(self)
        self.year = year
        self.keyword = keyword
        self.thread_list = thread_list
        self.container = container
        self.threadlocker = threadlocker
        self.url = "https://academic.microsoft.com/api/search"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", }

    def run(self):
        skip = 0
        data = query_dataForm_year(self.keyword, self.year, skip)
        proxy = getRandomPrxoy()
        r = send_request(data, proxy, 0)
        if r == "":
            return
        try:
            page_dic = json.loads(r.text)
        except:
            print(str(self.year) + " cannot parse")
        paper_numbers = page_dic["t"]
        print(str(self.year)+ " has " + str(paper_numbers) + " papers")
        # creats thread to collect each page
        for i in range(50):
            if skip >= paper_numbers:
                break
            else:
                data = query_dataForm_year(self.keyword, self.year, skip)


                j = len(self.thread_list)
                global proxy_list
                delaytime = get_delaytime(j)
                self.thread_list.append((Search_thread(j, data, delaytime, self.container, self.threadlocker)))
                skip = skip + 10



class Search_thread(threading.Thread):
    def __init__(self, threadID, data, delaytime, container, threadlocker,proxy="",re_tey=0):
        threading.Thread.__init__(self)
        self.re_try=re_tey
        self.threadID = threadID
        self.data = data
        self.delaytime = delaytime
        self.url = "https://academic.microsoft.com/api/search"
        self.container = container
        self.threadLock = threadlocker
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", }
        self.proxy=proxy
        if self.proxy =="":
            self.proxy=getRandomPrxoy()



    def run(self):
        if(self.re_try > 2):
            print("re-try 3times, stop ")
            return


        url = self.url
        try:
            # delay request
            time.sleep(self.delaytime)

            r = requests.post(url, headers=self.headers, json=self.data,
                              proxies={"http": self.proxy, "https": self.proxy})
            page_dic = json.loads(r.text)
            l = collect_single_page(page_dic)
            print("Thread-" + str(self.threadID) + " is done, it has waited for " + str(self.delaytime) + " seconds")
            self.threadLock.acquire()
            self.container.extend(l)
            self.threadLock.release()
        except:
            print("Thread-" + str(self.proxy) + " is failed to extract data ")
            print(self.data)
            s = Search_thread(self.threadID,self.data,5,self.container,self.threadLock,proxy="",re_tey=self.re_try+1)
            s.start()
            s.join()

class Research_paper:
    def __init__(self, title, abstract, id_, year, source, authors, label, keywords):
        self.title = title
        self.abstract = abstract
        self.id_ = id_
        self.year = year
        self.source = source
        self.authors = authors
        self.label = label
        self.keywords = keywords

    def __eq__(self, other):
        return self.title == other.title and self.abstract == other.abstract

    def __hash__(self):
        return hash(self.title)






def read_from_file():

    dir_path = os.getcwd()
    print(dir_path)
    article_list=[]
    path =r"uresearcher_app\static\other\Articles"
    file_list = []
    for file in os.listdir(path):
        f = os.path.join(path, file)
        file_list.append(f)
    ########
    i=0
    for p in file_list:
        with fitz.open(p) as doc:
            text = ""
            for page in doc:
                text += page.getText()
        article_list.append(Research_paper(p, text, i, 1111, "source", "authors", "label", "keywords"))
        i+=1
    return article_list



def get_delaytime(thread_counter):

    delaytime = math.floor(delaytime_coefficient * (thread_counter / 5) * 10 / len(proxy_list))
    return delaytime


def remove_duplicate(l):
    s = set()

    for i in l:
        s.add(i)

    return list(s)


def remove_htmlelement(text):
    return re.sub('<\/?em>', "", text)


def getkeywords(text):
    # if abstract is empty, should skip it
    keys = ""
    if text != "":
        separator = ","
        # keys = separator.join(generate_grant_keywords(text))
        r = Rake()
        r.extract_keywords_from_text(text)
        keys = separator.join(r.get_ranked_phrases())

    #    else:
    #        print("empty abstract")

    return keys


def collect_single_paper(current_paper):
    abstract = current_paper["d"]  # abstract
    title = remove_htmlelement(current_paper["dn"])  # title
    id_ = current_paper["id"]  # id

    source = ""
    if (len(current_paper["s"]) != 0):
        source = str(current_paper["s"][0]["link"])
    year = current_paper["v"]["publishedDate"]  # publish year

    label = current_paper["v"]["displayName"]

    authors = ""
    # get authors
    for dictionary in current_paper["a"]:
        if (authors != ""):
            authors = authors + ", "

        authors = authors + dictionary["dn"]
    keys = getkeywords(abstract)
    p = Research_paper(title, abstract, id_, year, source, authors, label, keys)
    return p


def collect_single_page(page_dic):
    t = len(page_dic["pr"])
    l = []
    for i in range(t):
        try:
            p = collect_single_paper(page_dic["pr"][i]["paper"])
            l.append(p)
        except:
            global s_c
            s_c = s_c + 1
            continue
    return l


def query_dataForm_year(keyword, year, skip):
    data = {
        "query": keyword,
        "queryExpression": "",
        "filters": ["Y>=" + str(year), "Y<=" + str(year)],
        "orderBy": 0,
        "skip": skip,
        "sortAscending": True,
        "take": 10,
        "includeCitationContexts": True,
        "profileId": ""
    }
    return data


def citedby_dataForm_year(title, id_, year, skip):
    data = {
        "query": title,
        "queryExpression": "RId=" + str(id_),
        "filters": ["Y>=" + str(year), "Y<=" + str(year)],
        "orderBy": 0,
        "skip": skip,
        "sortAscending": True,
        "take": 10,
        "includeCitationContexts": True,
        "parentEntityId": id_,
        "profileId": ""
    }
    return data


def query_dataForm(keyword, skip=0):
    data = {
        "query": keyword,
        "queryExpression": "",
        "filters": [],
        "orderBy": 0,
        "skip": skip,
        "sortAscending": True,
        "take": 10,
        "includeCitationContexts": True,
        "profileId": ""
    }
    return data


def send_request(data, proxy, retry_counter):
    url = "https://academic.microsoft.com/api/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", }

    r = ""
    try:
        r = requests.post(url, headers=headers, json=data, proxies={"http": proxy, "https": proxy})
    except:
        print("\n Big Problem with " + proxy)
    return r


def getRandomPrxoy():
    random_index= random.randint(0, len(proxy_list) - 1)
    return proxy_list[random_index]

def getProxy_inorder(thread_counter):
    return proxy_list[ thread_counter % len(proxy_list)]


class Searcher():
    def __init__(self, proxies):
        self.article_list = []
        self.threadLock = threading.Lock()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", }
        self.url = "https://academic.microsoft.com/api/search"
        global proxy_list
        proxy_list = proxies
        print("intialize searcher")

    def querry_first_500(self, keyword):
        print("start query")
        skip = 0
        articles_list = []
        thread_list = []
        # know how many pages
        data = query_dataForm(keyword)
        proxy = getRandomPrxoy()
        try:
            r = requests.post(self.url, headers=self.headers, json=data, proxies={"http": proxy, "https": proxy})
            page_dic = json.loads(r.text)
        except:
            print("\n Big Problem with " + proxy)
            proxy = getRandomPrxoy()
            r = requests.post(self.url, headers=self.headers, json=data, proxies={"http": proxy, "https": proxy})
        paper_numbers = page_dic["t"]
        print("pages " + str(paper_numbers))
        # creats thread to collect each page
        for i in range(50):

            if (skip >= paper_numbers):
                break
            else:
                delaytime = get_delaytime(i)
                data = query_dataForm(keyword,skip)
                thread_list.append((Search_thread(i, data, delaytime, articles_list, self.threadLock)))
                skip = skip + 10
        # run all thread
        for t in thread_list:
            t.start()
        # wait for everythread
        for t in thread_list:
            t.join()
        l = remove_duplicate(articles_list)
        print("Done, collected " + str(len(l)) + " articles")
        return l

    def collect_all_citedby_articles(self, title, id_):
        l = []
        url = self.url
        data = {
            "query": title,
            "queryExpression": "RId=" + str(id_),
            "filters": [],
            "orderBy": 0,
            "skip": 0,
            "sortAscending": True,
            "take": 10,
            "includeCitationContexts": True,
            "parentEntityId": id_,
            "profileId": ""
        }
        # the first request just get the year list
        proxy = getRandomPrxoy()
        pre_r = requests.post(url, headers=self.headers, json=data, proxies={"http": proxy, "https": proxy})
        pre_dic = json.loads(pre_r.text)

        years = pre_dic["f"][5]["fi"]
        length_of_year = len(years)
        #
        articles_list = []
        thread_counter = [0]
        thread_list = []
        for i in range(length_of_year):
            year = years[i]["dn"]
            # collect all threads
            thread_list.append(
                (collect_citedby_year_thread(year, title, id_, thread_counter, articles_list, self.threadLock)))
        for t in thread_list:
            t.start()
            # wait for everythread
        for t in thread_list:
            t.join()

        articles_list = remove_duplicate(articles_list)
        print("Done, collected " + str(len(articles_list)) + " articles")

        return remove_duplicate(articles_list)

    def collect_all_query_articles(self, keyword):
        l = []
        url = self.url
        data = query_dataForm(keyword)
        # the first request just get the year list
        proxy = getRandomPrxoy()
        pre_r = requests.post(url, headers=self.headers, json=data, proxies={"http": proxy, "https": proxy})
        pre_dic = json.loads(pre_r.text)

        years = pre_dic["f"][5]["fi"]
        #length_of_year = len(years)
        #
        articles_list = []
        thread_list = []
        subthread_list=[]

        for t in years[-3:]:
            year = t["dn"]
            # collect all threads
            thread_list.append(
                (collect_query_year_thread(year, keyword, subthread_list, articles_list, self.threadLock)))

        #build all subthread
        for t in thread_list:
            t.start()
            # wait for everythread
        for t in thread_list:
            t.join()
        print("There are " + str(len(subthread_list)) + "threads in the list, and it takes "+ str(get_delaytime(len(subthread_list)))+ " seconds")
        #run all subthread
        for t in subthread_list:
            t.start()
            # wait for everythread
        for t in subthread_list:
            t.join()





        articles_list = remove_duplicate(articles_list)
        print("Done, collected " + str(len(articles_list)) + " articles")

        return remove_duplicate(articles_list)


if __name__ == '__main__':
    print("Start")
    proxies = []
    f = open("Webshare 100 proxies.txt", "r")

    for x in f:
        proxies.append(x.strip())

    searcher = Searcher(proxies)
    #l = searcher.collect_all_citedby_articles("title", 3037353812)
    #l = searcher.collect_all_query_articles("Latent knowledge")
    #l = searcher.querry_first_500("Cell")
    l = read_from_file()

    print(str(len(l)))
    f.close()