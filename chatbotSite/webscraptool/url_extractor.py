import json
import re
import subprocess
from os.path import exists
import os


def crawl(url):
    # delete previous output json file
    output_dir = './url_crawler/outputfile.json' 
    file_exists = exists(output_dir)

    if file_exists: os.remove(output_dir)
    cmdline = f'cd url_crawler && scrapy crawl crawl_url -a url={url} -t json -o outputfile.json'

    # use subprocess because os will always jump to next step without finishing the cmd command
    p = subprocess.Popen(cmdline, shell=True) 
    return_code = p.wait()

def get_text(url):
    cmdline = f'cd get_text && scrapy crawl get_text -a url={url}'
    p = subprocess.Popen(cmdline, shell=True)
    return_code = p.wait()

def extract_url(json_dir):
    # extract every important url from website
    url_text = ""
    json_file = open(json_dir)
    dict = json.load(json_file)

    for d in dict:
        temp_url = str(d['url'])
        url_text = url_text + temp_url + '\n'

    json_file.close()

    with open("url_list.txt", "w") as f:
        f.write(url_text)

def filter_url(json_dir, keywords):
    # filter from extracted url by keyword 
    # if no url remains after filteration return false
    url_filtered = ""
    json_file = open(json_dir)
    dict = json.load(json_file)
    titles = []

    for d in dict:
        temp_title = str(d['title'])
        temp_url = str(d['url'])

        for keyword in keywords:
            # filter out same page
            if keyword in temp_title and temp_title not in titles:
                titles.append(temp_title)
                url_filtered = url_filtered + 'title:' + temp_title + 'url:' + temp_url + '\n'

    json_file.close()
    if url_filtered!='':
        with open("url_filtered_list.txt", "w") as f:
            f.write(url_filtered)  
        return True  
    else:
        return False

def get_text_from_filtered_url(file_dir, output_file_dir):
    f = open(file_dir)

    # delete previous output txt file if exists
    output_dir = output_file_dir
    file_exists = exists(output_dir)

    if file_exists: 
        os.remove(output_dir)

    while(True):
        url = ''
        str1 = f.readline()

        if not str1: break

        if 'url' in str1:
            url = str1.split('url:')[1]
            
        get_text(url)
        