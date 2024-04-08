
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import csv
import re
import urllib
import locale


def keyboard_crawler(max_pages):

    # define the global variables which are called in get_item
    global csv_writer

    # create and opens a .csv file in write mode and loads in the appropriate headlings
    csv_file = open('keyboard_data.csv', 'w',newline='',encoding='UTF-16')
    csv_writer = csv.writer(csv_file,delimiter='\t')
    csv_writer.writerow(['Tên SP','Nhà sản xuất','Model','Kết nối','Kích thước','Loại switch','Giá(đ)'])


 

    # define the start page
    page = 1
    count = 1

    # loop through each item of each page to scrape data until until max page
    while page <= max_pages:

        #load starting url with header to bypass security
        url = 'https://hacom.vn/ban-phim-may-tinh/'+str(page)+'/'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", 
                    "Upgrade-Insecure-Requests": "1"
                   }

        # request the url text and create BeautifulSoup object to parse html
        req = requests.Session()
        source_code = req.get(url,headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
       # print(soup.prettify())
        # parses through each keyboard on the page to scrape the data
        for link in tqdm(soup.findAll('div', {'class': 'p-img'})):

            # pulls the keyboard url
            keyboard = link.a
            print(keyboard.get('href'))
            href = 'https://hacom.vn/' + keyboard.get('href')

            # calls get_item to perform the actual data scraping 
            get_item(href, count)
            count += 1

        print('{}/{} page(s) have been crawled!'.format(page, max_pages))

        page += 1

    #close the .csv file once all keyboard have been scraped
    csv_file.close()
    print('All {} page(s) have been scraped!'.format(max_pages))

def get_item(item_url, count):

    #same procedure as before, request keyboard url and create a BeuatifulSoup object
    headers = {"User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "UTF-8,gzip, deflate", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    source_code = requests.get(item_url, headers=headers)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    #print(soup.prettify())


    try:
        name = soup.find('div', {'class': 'product_detail-header'}).h1.text.strip()
        #print(name)
    except:
        name = None
    try:
        price_tag = soup.find('strong', class_='giakm')
        price = int(price_tag['data-price'])

        # Format the price with commas
        formatted_price = '{:,.0f}'.format(float(price))
        
    except:
        formatted_price = None

   # csv_writer.writerow([name])

    rows = soup.find('div',{'class': 'bang-tskt'}).find_all('tr')

    # Khởi tạo danh sách để chứa thông tin từng dòng
    info_list = []
    brand= model =connectType = size= switch= ''

    # Lặp qua từng dòng và lưu vào danh sách
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            if 'sản xuất' in key or 'Thương hiệu' in key:
                brand = cells[1].text.strip()
            elif 'Model' in key or 'Mã sản phảm' in key:
                model= cells[1].text.strip()
            elif 'Kết nối' in key:
                connectType = cells[1].text.strip()
            elif 'Kích thước' in key or 'Kích cỡ' in key:
                size = cells[1].text.strip()
            elif 'Switch' in key or 'Loại switch' in key:
                switch = cells[1].text.strip()
  
    csv_writer.writerow([name,brand,model,connectType,size,switch,price])

def main():
    max_pages = 23 # Số trang tối đa cần crawl
    keyboard_crawler(max_pages)

if __name__ == "__main__":
    main()

   