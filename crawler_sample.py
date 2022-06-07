import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')


class GoogleCrawler():
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    
    #  URL 萃取 From Google Search上 , using 第三方套件
    #  https://python-googlesearch.readthedocs.io/en/latest/
    def google_url_search_byOpenSource(query,tbs='qdr:m',num=10):
        array_url = [url for url in search('tsmc', tbs='qdr:m' , num=10)]
        return array_url
    # 網路擷取器
    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
    # URL 萃取 From Google Search上
    def scrape_google(self,query):
        response = self.get_source(self.url + query)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
# URL萃取器，有link之外，也有標題
#     qdr:h (past hour)
#     qdr:d (past day)
#     qdr:w (past week)
#     qdr:m (past month)
#     qdr:y (past year)
    def google_search(self,query,timeline='',page='0'):
        url = self.url + query + '&tbs={timeline}&start={page}'.format(timeline=timeline,page=page)
        print('[Check][URL] URL : {url}'.format(url=url))
        response = self.get_source(url)
        return self.parse_googleResults(response)
    # Google Search Result Parsing
    def parse_googleResults(self,response):
        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            item = {
                'title': result.find(css_identifier_title).get_text(),
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                'text': result.find("div", {"class": css_identifier_text}).get_text()
            }
            output.append(item)
        return output
    
    # 網頁解析器
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup
    # 解析後，取<p>文字
    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    def get_link_json(self, query, all_link, time):
        data_array = []
        json_data = {
            'Date' : time,
            'Query' : query , 
            'Link' : all_link
        }
        data_array.append(json_data)
        return data_array
    def jsonarray_toexcel(self,data_array,path):
        df = pd.DataFrame(data=data_array)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        filename = path + current_time + ".xlsx"
        print("save result as "+filename)
        try:
            print("Save to pvc")
            df.to_excel(filename , index=False)
        except:
            print("Save Error, Change")
            print("Save to Root")
            df.to_excel('result.xlsx' , index=False)
        return
    def jsonarray_toexcel_local(self,data_array):
        df = pd.DataFrame(data=data_array)
        df.to_excel('result.xlsx' , index=False)
        return
    def str_contain_chinese(self,txt):
        for ch in txt:
            if u'\u4e00'<=ch<=u'\u9fa5':
                return True
        return False


if __name__ == "__main__":
    path = '/var/log/history/' 
    querys = ["台積電 ASML", "台積電 Applied Materials", "台積電 SUMCO"]
    year = [5,4,3,2,1,12,11,10,9,8,7,6]
    
    big_month = [1,3,5,7,8,10,12]
    time_line = []
    for month in year:
        if month in big_month:
            if month<6:
                time_line.append('cdr%3A1%2Ccd_min%3A{start_month}%2F{start_day}%2F{start_year}%2Ccd_max%3A{end_month}%2F{end_day}%2F{end_year}'.format(start_month=month, start_day=1, start_year=2022, end_month=month, end_day=31, end_year=2022))
            else:
                time_line.append('cdr%3A1%2Ccd_min%3A{start_month}%2F{start_day}%2F{start_year}%2Ccd_max%3A{end_month}%2F{end_day}%2F{end_year}'.format(start_month=month, start_day=1, start_year=2021, end_month=month, end_day=31, end_year=2021))
        elif month==2:
            time_line.append('cdr%3A1%2Ccd_min%3A{start_month}%2F{start_day}%2F{start_year}%2Ccd_max%3A{end_month}%2F{end_day}%2F{end_year}'.format(start_month=month, start_day=1, start_year=2022, end_month=month, end_day=28, end_year=2022))
        else:
            if month<6:
                time_line.append('cdr%3A1%2Ccd_min%3A{start_month}%2F{start_day}%2F{start_year}%2Ccd_max%3A{end_month}%2F{end_day}%2F{end_year}'.format(start_month=month, start_day=1, start_year=2022, end_month=month, end_day=30, end_year=2022))
            else:
                time_line.append('cdr%3A1%2Ccd_min%3A{start_month}%2F{start_day}%2F{start_year}%2Ccd_max%3A{end_month}%2F{end_day}%2F{end_year}'.format(start_month=month, start_day=1, start_year=2021, end_month=month, end_day=30, end_year=2021))

    year_result = []
    for month,time in enumerate(time_line):
        print("Now time:",time)
        for index,query in enumerate(querys):
            crawler = GoogleCrawler()
            results = crawler.google_search(query , time , '0')
            all_link = []
            for result in results:
                Target_URL = result["link"]
                response = crawler.get_source(Target_URL)
                if response!=None:
                    soup = crawler.html_parser(response.text)
                    orignal_text = crawler.html_getText(soup)
                    if(crawler.str_contain_chinese(orignal_text)):
                        all_link.append(result["link"]) #只儲存中文資料
            month_result = crawler.get_link_json(query, all_link, year[month])
            year_result.append(month_result[0])
    

    crawler.jsonarray_toexcel(year_result,path )
    #crawler.jsonarray_toexcel_local(year_result)
    print('Excel is OK')
