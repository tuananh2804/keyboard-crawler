import requests
from bs4 import BeautifulSoup
import csv
from tqdm.auto import tqdm

def keyboard_crawler(max_pages):
    global csv_writer

    csv_file = open('raw_data_anphatpc.csv', 'w', newline='', encoding='UTF-16')
    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['Tên SP', 'Nhà sản xuất', 'Model', 'Kết nối', 'Kích thước', 'Loại switch', 'Giá(đ)'])

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

        for item in tqdm(soup.find_all('div', class_='p-item js-p-item')):
            name = item.find('a', class_='p-name').h3.text.strip() if item.find('a', class_='p-name') else None
            price_with_currency = item.find('span', class_='p-price').text.strip() if item.find('span', class_='p-price') else None

            price = price_with_currency.replace('đ', '').replace('.', '')


            manufacturer = None
            model = None
            connection = None
            size = None
            switch_type = None

            # You can add more logic here to extract other attributes if needed

            csv_writer.writerow([name, manufacturer, model, connection, size, switch_type, price])

    csv_file.close()
    print('All {} page(s) have been scraped!'.format(max_pages))

def main():
    max_pages = 16
    keyboard_crawler(max_pages)

if __name__ == "__main__":
    main()
