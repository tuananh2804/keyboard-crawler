import pandas as pd
import numpy as np
import re

def read_data_from_csv(filename):
    df = pd.read_csv(filename, sep='\t',encoding='UTF-16')
    return df 

def replace_missing_manufacturer(df):
    # Thay đổi giá trị 'Đang cập nhật' thành khoảng trắng
    df['Nhà sản xuất'] = df['Nhà sản xuất'].replace('Đang cập nhật', '')

    # Tạo một danh sách chứa tất cả các nhà sản xuất đã xuất hiện trong cột "Nhà sản xuất"
    manufacturers = df['Nhà sản xuất'].unique().tolist()
    
    # Duyệt qua từng dòng trong dataframe
    for index, row in df.iterrows():
        product_name = row['Tên SP']
        if isinstance(product_name, str):  # Kiểm tra xem giá trị của product_name có phải là chuỗi không
            # Duyệt qua từng nhà sản xuất đã từng xuất hiện
            for manufacturer in manufacturers:
                if isinstance(manufacturer, str):  # Kiểm tra xem giá trị của manufacturer có phải là chuỗi không
                    # Nếu tên nhà sản xuất có trong tên sản phẩm thì thay thế dữ liệu trống trong cột "Nhà sản xuất"
                    if manufacturer.lower() in product_name.lower():
                        df.at[index, 'Nhà sản xuất'] = manufacturer
                        break  # Sau khi thay thế xong, thoát khỏi vòng lặp
    
    return df

def replace_missing_model(df):
    # Thay đổi giá trị 'Đang cập nhật' thành khoảng trắng
    df['Model'] = df['Model'].replace('Đang cập nhật', '')

    # Tạo một danh sách chứa tất cả các model đã xuất hiện trong cột "Model"
    models = df['Model'].unique().tolist()
    
    # Duyệt qua từng dòng trong dataframe
    for index, row in df.iterrows():
        product_name = row['Tên SP']
        if isinstance(product_name, str):  # Kiểm tra xem giá trị của product_name có phải là chuỗi không
            # Duyệt qua từng model đã từng xuất hiện
            for model in models:
                if isinstance(model, str):  # Kiểm tra xem giá trị của model có phải là chuỗi không
                    # Nếu tên model có trong tên sản phẩm thì thay thế dữ liệu trống trong cột "Model"
                    if model.lower() in product_name.lower():
                        df.at[index, 'Model'] = model
                        break  # Sau khi thay thế xong, thoát khỏi vòng lặp
    
    return df

def replace_missing_value(df):
    # Thay đổi giá trị NaN thành 0 trong tất cả các cột
    df.fillna(0, inplace=True)
    
    # Thay đổi giá trị rỗng thành 0 trong tất cả các cột (nếu có)
    df.replace('', 0, inplace=True)
    
    return df

def check_missing_data(df):
    # Thống kê lại dữ liệu trống sau khi thực hiện thay thế
    missing_data = df.isnull().sum()
    print(missing_data)

def check_and_remove_empty_rows(df):
    # Kiểm tra nếu cột 'Nhà sản xuất' trống hoặc 3 trong 6 cột còn lại bị trống hoặc NaN, thì xóa hàng đó
    df['empty_count'] = df.isnull().sum(axis=1)
    df = df[df['empty_count'] < 3]
    df = df.drop(columns=['empty_count'])
    return df

def remove_special_characters(text):
    # Kiểm tra nếu text không phải là chuỗi thì trả về text nguyên thể
    if isinstance(text, str):
        # Xóa các kí tự như "/", "(", "_" và toàn bộ kí tự phía sau
        text = re.sub(r'[/(_\n].*', '', text)
    return text
# bỏ chữ mm và các kí tự dư khác
def remove_special_charactersKichThuoc(text):
    # Kiểm tra nếu text không phải là chuỗi thì trả về text nguyên thể
    if isinstance(text, str):
        # Xóa các kí tự như "/", "(", "mm" và toàn bộ kí tự phía sau
        text = re.sub(r'[/(mm*xX×.].*', '', text)
    return text

def simplify_decimal_to_integer(text):
    # Kiểm tra nếu text không phải là chuỗi thì trả về text nguyên thể
    if isinstance(text, str):
        # Tìm kiếm số thập phân trong chuỗi và chuyển về số tự nhiên
        match = re.search(r'\d+\.\d+', text)
        if match:
            decimal_number = float(match.group())
            integer_number = int(decimal_number)
            text = re.sub(r'\d+\.\d+', str(integer_number), text)
    return text
def change_connection_values(df):
    df['Kết nối'] = df['Kết nối'].replace(['Dây', 'Có dây ', 'Có dây'], 'Có dây')
    return df
def update_connection_type(df):
    for index, row in df.iterrows():
        connection_type = row['Kết nối']
        if isinstance(connection_type, str):
            if 'Type C' in connection_type:
                df.at[index, 'Kết nối'] = 'vừa có dây vừa không dây'
            elif 'USB 2.0' in connection_type or connection_type == 'có dây' or connection_type == 'Có dây'or 'cáp liền' in connection_type:
                df.at[index, 'Kết nối'] = 'có dây'
            elif connection_type == '0':
                pass
            else:
                df.at[index, 'Kết nối'] = 'không dây'
    return df
def update_size_column(df):
    for index, row in df.iterrows():
        connection_type = row['Kích thước']
        if isinstance(connection_type, str):
            if 'Fullsize' in connection_type or 'fullsize' in connection_type or 'Full size' in connection_type or 'Full Size' in connection_type:
                df.at[index, 'Kích thước'] = '430'
    return df

# Đọc dữ liệu từ file CSV
df = read_data_from_csv('raw_data.csv')

print("Thông kê dữ liệu trống trước khi thay thế:")
check_missing_data(df)

# Thực hiện thay thế dữ liệu trống trong cột "Nhà sản xuất"
df = replace_missing_manufacturer(df)
df = replace_missing_model(df)
# Kiểm tra lại dữ liệu trống sau khi thực hiện thay thế
print("Thông kê dữ liệu trống sau khi thay thế:")
check_missing_data(df)

# Kiểm tra và xóa các hàng bị trống nhiều thỏa mãn điều kiện
df = check_and_remove_empty_rows(df)


# Áp dụng hàm remove_special_characters cho cột 'Tên SP' 'Model' 'Kết nối' 'Loại switch'
df['Tên SP'] = df['Tên SP'].apply(remove_special_characters)
df['Model'] = df['Model'].apply(remove_special_characters)
df['Kết nối'] = df['Kết nối'].apply(remove_special_characters)
df['Loại switch'] = df['Loại switch'].apply(remove_special_characters)

df['Kích thước'] = df['Kích thước'].apply(remove_special_charactersKichThuoc)

df = replace_missing_value(df)
df = change_connection_values(df)
df = update_connection_type(df)
df['Kích thước'] = df['Kích thước'].apply(simplify_decimal_to_integer)
df = update_size_column(df)

# Lưu dữ liệu đã được cập nhật vào file CSV
df.to_csv('clean_data.csv', index=False,encoding='utf-8-sig')

print("Kiểm tra và cập nhật dữ liệu thành công. Kết quả đã được lưu vào file 'clean_data.csv'")