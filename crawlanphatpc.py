import requests
from bs4 import BeautifulSoup
import csv
from tqdm.auto import tqdm

def keyboard_crawler(max_pages):
    global csv_writer

    csv_file = open('raw_data_anphatpc.csv', 'w', newline='', encoding='UTF-16')
    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['Tên SP', 'Nhà sản xuất', 'Model', 'Kết nối', 'Kích thước', 'Loại switch','Cân nặng', 'Giá(đ)'])
    page = 1
    count = 1
    for page in range(1, max_pages + 1):
        url = f'https://www.anphatpc.com.vn/ban-phim-co-choi-game.html?page={page}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1"
        }

        req = requests.Session()
        source_code = req.get(url, headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")

        for link in tqdm(soup.find_all('div', class_='p-item js-p-item')):
            keyboard = link.a
            print(keyboard.get('href'))
            href = 'https://www.anphatpc.com.vn/' + keyboard.get('href')

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
    # print(soup.prettify())


    
   
    try:
        # Tìm thẻ div với class 'pro-info-center'
        pro_info_center = soup.find('div', {'class': 'pro-info-center'})

         # Tìm thẻ h1 bên trong thẻ div đó và lấy nội dung văn bản
        name = pro_info_center.find('h1', {'class': 'pro-name js-product-name'}).text.strip()
    except:
        name = None
    try:
        promo_price_tag = soup.find('b', class_='text-18 js-pro-total-price')
        promo_price = promo_price_tag.get_text(strip=True)
        price = promo_price.replace('đ', '').replace('.', '')

    except:
        price = None

# Lấy tất cả các thẻ span bên trong div đó
    pro_info_summary = soup.find('div', {'class': 'pro-info-summary'})
    brand= model =connectType = size= switch=weight= ''
    brand_model_set = False
    try:
        items = pro_info_summary.find_all('span', {'class': 'item'})
    except:
        items = None
    # Lấy nội dung văn bản của từng thẻ span và lưu vào danh sách
    if items:
        data = [item.get_text(strip=True) for item in items]
        
        # Kiểm tra số lượng phần tử trong danh sách
        if len(data) < 5:
            print("Not enough data to fill all columns.")
        else:
            for item in data:
                if ('Bàn phím cơ' in item or 'Bàn phím' in item) and not brand_model_set:
                    brand_model = item.replace('Bàn phím cơ', '').replace('Bàn phím', '').strip()
                    brand = brand_model.split()[0]  # Assuming the first word is the brand
                    model = brand_model.split()[1] if len(brand_model.split()) > 1 else ''  # The word after the brand
                    if 'switch' in brand_model:              
                        switch_index = brand_model.split().index('switch')                    
                        if switch_index > 0:
                           
                            switch = brand_model.split()[switch_index - 1]
                    brand_model_set = True  # Set flag to True after assigning values
                    
                elif 'kết nối' in item or 'Kết nối' in item:
                    try:
                        connectType = item.split(':')[1].strip()
                    except:
                        connectType = ''
                elif 'Kích thước' in item:
                    if('Nặng' in item or 'Trọng lượng' in item):
                        try:
                            parts = item.split('|')
                            size = parts[0].split(':')[1].strip()
                            weight = parts[1].strip()
                        except IndexError:
                            size = ''
                            weight = ''
                    else:
                        try:
                            size = item.split(':')[1].strip()
                        except:
                            size = ''
                elif 'Cân nặng' in item or 'Trọng lượng' in item:
                    try:
                         weight = item.split(':')[1].strip()
                    except:
                        weight = ''
   # csv_writer.writerow([name])

    # rows = soup.find('div',{'class': 'bang-tskt'}).find_all('tr')

    # Khởi tạo danh sách để chứa thông tin từng dòng
    # info_list = []


    # # Lặp qua từng dòng và lưu vào danh sách
    # for row in rows:
    #     cells = row.find_all('td')
    #     if len(cells) == 2:
    #         key = cells[0].text.strip()
    #         if 'sản xuất' in key or 'Thương hiệu' in key:
    #             brand = cells[1].text.strip()
    #         elif 'Model' in key or 'Mã sản phảm' in key:
    #             model= cells[1].text.strip()
    #         elif 'Kết nối' in key:
    #             connectType = cells[1].text.strip()
    #         elif 'Kích thước' in key or 'Kích cỡ' in key:
    #             size = cells[1].text.strip()
    #         elif 'Switch' in key or 'Loại switch' in key:
    #             switch = cells[1].text.strip()
  
    csv_writer.writerow([name,brand,model,connectType,size,switch,weight,price])

def main():
    max_pages = 15
    keyboard_crawler(max_pages)

if __name__ == "__main__":
    main()
