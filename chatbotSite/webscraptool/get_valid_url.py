import requests
import time
# this progrom will automatically detect if the given location exists on the target website
# the url will detect through a given dictionary
# complement of scrapy url crawler(as it some times scrapy miss pages)
def run(domain, page_dictionary):
    domain_url = 'https://' + domain +'/'
    urls_exist = []

    def check_url_validity(url):
        # return true if url exists(code:200)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        try:
            r = requests.head(url,headers=headers)
            r.close()
        except Exception as e:
            print('error:' + str(e))
            return False
        print(r.status_code)
        return r.status_code == 200 or r.status_code == 301

    for page in page_dictionary:
        time.sleep(1)
        if check_url_validity(domain_url + page):
            urls_exist.append({'url':domain_url + page})
    
    return urls_exist
