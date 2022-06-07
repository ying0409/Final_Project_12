import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import crawler_sample

def test_google_search():
    crawler = crawler_sample.GoogleCrawler()
    query = "TSMC Ingas"
    results = crawler.google_search(query)
    assert len(results) > 0

def test_get_source():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    assert response.status_code == 200

def test_html_parser():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    results = soup.findAll("div")
    assert len(results) > 0

def test_scrape_google():
    query = 'https://www.google.com/search?q='+"TSMC Ingas"
    crawler = crawler_sample.GoogleCrawler()
    results = crawler.scrape_google(query)
    assert len(results) > 0


def test_html_getText():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    assert len(orignal_text) > 0

def test_str_contain_chinese():
    crawler = crawler_sample.GoogleCrawler()
    test = '測試中文'
    contain_chinese = crawler.str_contain_chinese(test)
    assert contain_chinese==True
    test = 'test chinese'
    contain_chinese = crawler.str_contain_chinese(test)
    assert contain_chinese==False


