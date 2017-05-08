# -*- coding: utf-8 -*-
import pandas as ps
from bs4 import BeautifulSoup

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

if __name__ == '__main__':
    data = scraping()
    embed()
