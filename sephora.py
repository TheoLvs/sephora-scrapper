#! /usr/bin/python
# -*- coding:utf-8 -*-

import bs4 as bs
import requests
import time
import datetime



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


SEPHORA_PROMO_MAPPING = {
    "FR":{
        "brand":"marque_promo_ss_menu",
        "description":"desc_promo_ss_menu",
        "price":"prix",
    }
}





#=============================================================================================================================
# CLASS WRAPPER
#=============================================================================================================================



class SephoraScrapper(object):
    def __init__(self,country):
        self.country = country.upper()
        self.website = SEPHORA_WEBSITES[self.country]
        self.page = scrapping(self.website)


    def get_promo_blocks(self,googlesheet = None):
        blocks = self.page.find_all(class_ = "btn_menu")
        data = []
        for block in blocks:
            category = block.find("a").text
            if category == "":
                continue
            promo = block.find(class_ = "bloc_promo_ss_menu")
            if promo is not None:
                promo = self.parse_promo_block(promo)
                promo["category"] = category
                data.append(promo)

        if googlesheet is not None:
            for row in data:
                row = [
                    str(datetime.datetime.now().date()),
                    row.get("category"),
                    row.get("brand"),
                    row.get("description"),
                    row.get("price"),
                    row.get("img"),
                    row.get("other"),
                ]

                googlesheet.append_row(row)

            print(f"... {len(data)} added to google sheet {googlesheet.title}")

        return data


    def parse_promo_block(self,block):


        data = {}
        mapping = SEPHORA_PROMO_MAPPING.get(self.country,"FR")

        for attr in ["brand","price","img","description","other"]:

            if attr == "img":
                try:
                    img = self.website + block.find("img").attrs["src"]
                except:
                    img = ""

                data["img"] = img

            else:
                try:
                    data_attr = block.find(class_= mapping.get(attr))
                    a = data_attr.find("a")
                    if a is None:
                        data_attr = data_attr.text
                    else:
                        data_attr = a.text
                except:
                    data_attr = ""

                data[attr] = data_attr.strip()

        return data
