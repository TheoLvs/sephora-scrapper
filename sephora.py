#! /usr/bin/python
# -*- coding:utf-8 -*-

import bs4 as bs
import requests
import time



#=============================================================================================================================
# SCRAPPING BASE FUNCTION
#=============================================================================================================================



def scrapping(url,timeout = 15,session = None):
    """
    Scrapping function that takes an URL to get a beautiful soup object of the source code of the URL
    A timeout is set by default at 15 seconds

    Returns : a beautiful soup object
    """
    if session is not None:
        html = session.get(url,timeout = timeout).content
    else:     
        html = requests.get(url,timeout = timeout).content
    return parsing(html)


def parsing(html):
    return bs.BeautifulSoup(html,'lxml')





#=============================================================================================================================
# MAPPING WEBSITE
#=============================================================================================================================



SEPHORA_WEBSITES = {
    "FR":"http://www.sephora.fr/",
    "ES":"http://www.sephora.es/",
    "PL":"http://www.sephora.pl/",
    "IT":"http://www.sephora.it/",
    "CZ":"http://www.sephora.cz/",
    "PT":"http://www.sephora.pt/",
    "RO":"http://www.sephora.ro/",
    "GR":"https://www.sephora.gr/el/",
}





#=============================================================================================================================
# CLASS WRAPPER
#=============================================================================================================================



class SephoraScrapper(object):
    def __init__(self,country):
        self.country = country
        self.website = SEPHORA_WEBSITES[self.country.upper()]
        self.page = scrapping(self.website)


    def get_promo_blocks(self):
        blocks = self.page.find_all(class_ = "bloc_promo_ss_menu")
        blocks = [self.parse_promo_block(block) for block in blocks]
        return blocks


    def parse_promo_block(self,block):
        # Image
        try:
            img = self.website + block.find("img").attrs["src"]
        except:
            img = ""

        # Text
        try:
            text = block.text.replace("\t","").replace("\n\n\n","\n").replace("\n\n","\n").replace("\t","").replace("\n\r\n","\n").strip().split("\n")
        except:
            text = block.text

        return {"img":img,"text":text}


