from image_scraper import search_and_download
import os


if __name__ =="__main__":
    query_list = ["Takina Inoue"]
    
    for q in query_list:
        search_and_download(q,"/usr/bin/chromedriver")
