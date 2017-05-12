# -*- coding: utf-8 -*-
import pandas as ps
from bs4 import BeautifulSoup
import MeCab
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# intractive shell
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

def scraping():
    soup = BeautifulSoup(open("./SFC-SFS.html"),"html.parser");
    htmls = soup.find_all("table")
    ans_html_list = htmls[2].find_all("tr")
    del ans_html_list[0:3]
    datas = []
    header = ["stdno","affili","cns","title","ans"]
    for i in range(0,len(ans_html_list),2):
        metadatas = ans_html_list[i].find_all("td")
        ansdata = ans_html_list[i+1].find_all("td")
        datas.append([metadatas[1].string,metadatas[2].string,metadatas[4].string,metadatas[5].string,ansdata[0].find("pre").text])
    dataflame = ps.DataFrame(datas,columns=header)
    return dataflame

def parse(unicode_string):
    tagger = MeCab.Tagger("-Ochasen")
    text = unicode_string.encode("utf-8")
    node = tagger.parseToNode(text)

    words = []
    nouns = []
    verbs = []
    adjs = []
    while node:
        pos = node.feature.split(",")[0]
        # unicode 型に戻す
        word = node.surface.decode("utf-8")
        if pos == "名詞":
            nouns.append(word)
        elif pos == "動詞":
            verbs.append(word)
        elif pos == "形容詞":
            adjs.append(word)
        words.append(word)
        node = node.next
    parsed_words_dict = {
        "all": words[1:-1],
        "nouns": nouns,
        "verbs": verbs,
        "adjs": adjs
        }
    return parsed_words_dict


def remove_duplicates(x):
    y=[]
    for i in x:
        if i not in y:
            y.append(i)
    return y



if __name__ == '__main__':
    data = scraping()
    print("done scraping")
    stdwordlists = []
    allwordlist = []
    for a in range(0,len(data)):
        words = parse(data.ans[a])
        stdwordlists.append(words["nouns"])
        allwordlist.extend(words["nouns"])
    allwordlist = remove_duplicates(allwordlist)
    stdstatuses = []
    for a in range(0,len(stdwordlists)):
        stdstatus = [0] * len(allwordlist)
        for word in stdwordlists[a]:
            i = allwordlist.index(word)
            stdstatus[i] += 1
        stdstatuses.append(stdstatus)
    status = list(stdstatuses)
    print("k-means clustering")
    pred = KMeans(n_clusters=15).fit_predict(status)

    data["cluster"] = pred
    data.to_csv("./datawithcluster.csv")
