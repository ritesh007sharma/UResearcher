#!/usr/bin/env python3
import requests
import json
import os
import yaml


## Global variables
ELS_API_KEY = ""

with open("elsevierBot_config.yaml", 'r') as config:
    try:
        yaml_config = yaml.safe_load(config)
        ELS_API_KEY = yaml_config["ELS_API_KEY"]
    except yaml.YAMLError as exc:
        print(exc)


# content color functions
def cRed(c): return "\033[91m{}\033[00m".format(c)
def cGreen(c): return "\033[92m{}\033[00m".format(c)
def cYellow(c): return "\033[93m{}\033[00m".format(c)
def cCyan(c): return "\033[96m{}\033[00m".format(c) 

# check connection status
def checkConnectionStatus(response):
    if response.status_code == 200:
        print(cGreen("[+]") + "Success")
        return True
    elif response.status_code == 404:
        print(cRed("[-]") + "404 Not Found")
        return False
    else: 
        print(cRed("[-]") + "Error")
        return False

def checkConnectionStatus(response, info):
    if response.status_code == 200:
        print(cGreen("[+]") + info + " Success")
        return True
    elif response.status_code == 404:
        print(cRed("[-]") + info + " 404 Not Found")
        return False
    else: 
        print(cRed("[-]") + info + " Error")
        return False

## Query details
query = input("Search: ") # search keywords
count = input("Number: ") # search numbers
database = {"affiliation":"affiliation", "author":"author", "sciencedirect":"sciencedirect", "scopus":"scopus"}
url = "https://api.elsevier.com/content/search/" + database["scopus"] + "?query=" + query + "&apiKey=" + ELS_API_KEY + "&count=" + str(count)
header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

## GET
response = requests.get(url, headers = header)
checkConnectionStatus(response, "Database Query")


## Article Info
class ArticleInfo:
  def __init__(self, title, creator, doi, eid):
    self.title = title
    self.creator = creator
    self.doi = doi
    self.eid = eid

## Check valid content
rContent = response.content
rJson = json.loads(rContent)
articleInfoList = []
index = 0
for item in rJson["search-results"]["entry"]:
    print(cCyan("[*]") + "Try: result[" + str(index) + "]")
    index += 1
    hasId = 0
    if "prism:doi" in item:
        hasId = 1
        doi = item["prism:doi"]
    if "eid" in item:
        hasId = 1
        eid = item["eid"]
    if not hasId:
        print(cRed("[-]") + "Error")
        continue
    if "dc:title" in item: 
        title = item["dc:title"]
    if "dc:creator" in item: 
        creator = item["dc:creator"]
    print(" Title: " + title)
    print(" Creator: " + creator)
    print(" doi: " + doi)
    print(" eid: " + eid)
    articleInfoList.append(ArticleInfo(title, creator, doi, eid))
    print(cGreen("[+]") + "Complete")

## GET article
def get_article_retrieval_doi_url(doi): return "https://api.elsevier.com/content/article/doi/" + doi + "?APIKey=" + ELS_API_KEY
def get_article_retrieval_eid_url(eid): return "https://api.elsevier.com/content/article/eid/" + eid + "?APIKey=" + ELS_API_KEY

folderName = "result"
if not os.path.exists(folderName):
    os.mkdir(folderName)
def get_file_path(fileName): return os.path.join("./" + folderName + "/" + fileName + ".txt")
article_retrieval_header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

success_article_num = 0

for item in articleInfoList:
    if item.doi is not None: 
        doi_url = get_article_retrieval_doi_url(item.doi)
        response_article_doi = requests.get(doi_url, headers = article_retrieval_header)
        if checkConnectionStatus(response_article_doi, "Article Retrieval"):
            with open(get_file_path(item.title[:10]), "w+") as file:
                file.write(str(response_article_doi.content))
            success_article_num += 1
            print(cGreen("[+]") + "Complete")
    elif item.eid is not None: 
        eid_url = get_article_retrieval_doi_url(item.doi)
        response_article_doi = requests.get(eid_url, headers = article_retrieval_header)
        if checkConnectionStatus(response_article_eid, "Article Retrieval"):
            with open(get_file_path(item.title[:10]), "w+") as file:
                file.write(str(response_article_edi.content))
            success_article_num += 1
            print(cGreen("[+]") + "Complete")
    else: 
        print(cRed("[-]") + info + " Error")

print("")

# Summary
print(cGreen("[*]") + "Summary")
# Total Query Number
print(cYellow("[*]") + "Total Query Number is: \t" + str(count))
# Total Crawled Number 
print(cYellow("[*]") + "Total Crawled Number is: \t" + str(success_article_num))
# Success Rate
successRate = success_article_num / int(count)
print(cYellow("[*]") + "Success Rate is: \t" + str(successRate))
