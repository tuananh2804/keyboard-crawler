import pandas as pd
import numpy as np
import re
import random
from sklearn.impute import KNNImputer

# !!!!README!!!!!
# -Đã clean lại biến 'loại switch': chỉ giữ những dòng có ["blue", "cherry", "brown", "silver", "yellow", "pink", "green", "black", "white", "red"]
# các dòng khác lấy giá trị random từ các biến trên
# -Đã clean lại biến 'Model': chỉ lấy 32 model xuất hiện nhiều nhất, các dòng khác lấy giá trị random từ 32 giá trị đó
# DONE:
# -Thay thế hết các giá trị 0 ở các cột bằng giá trị random trong cột
# -Riếng biến 'Kích thước' là biến số thực thì sử dụng cách khác(có thể là dự báo KNN)
# -chuẩn hóa biến 'Kích thước' bằng min max scaler(đang nghiên cứu xem có cần thiết ko)


def read_data_from_csv(filename):
    df = pd.read_csv(filename, sep='\t',encoding='utf-16')
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
    df = df[df['empty_count'] <5]
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
        text = re.sub(r'[/(mm*xX×,.-].*', '', text)
    return text

def remove_commas(price):
    if isinstance(price, str):
        return price.replace(',', '')
    return price

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

def update_size_column(df):
    for index, row in df.iterrows():
        size_value = row['Kích thước']
        if isinstance(size_value, str):
            if 'Fullsize' in size_value or 'fullsize' in size_value:
                df.at[index, 'Kích thước'] = '430'
            elif 'Chiều cao' in size_value or 'Độ dài' in size_value or 'Đang cập nhật' in size_value:
                df.at[index, 'Kích thước'] = np.nan
            elif 'Độ dài: ' in size_value or 'Đang cập nhật' in size_value:
                df.at[index, 'Kích thước'] = np.nan
            elif '%' in size_value:
                df.at[index, 'Kích thước'] = np.nan
            else:
                # Kiểm tra nếu chuỗi chứa chữ cái
                if any(c.isalpha() for c in size_value):
                    df.at[index, 'Kích thước'] = np.nan
    return df


def simplify_decimal_to_integer(text):
    # Kiểm tra nếu text không phải là chuỗi thì dtrả về text nguyên thể
    if isinstance(text, str):
        # Tìm kiếm số thập phân trong chuỗi và chuyển về số tự nhiên
        match = re.search(r'\d+\.\d+', text)
        if match:
            decimal_number = float(match.group())
            integer_number = int(decimal_number)
            text = re.sub(r'\d+\,\d+', str(integer_number), text)
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

def convert_decimal_to_integer(value):
    if isinstance(value, str):
        # Tìm và chuyển đổi giá trị số thập phân thành số tự nhiên
        match = re.match(r'^(\d+),(\d+)$', value)
        if match:
            return int(match.group(1) + match.group(2))  # Kết hợp các nhóm số và chuyển đổi thành số tự nhiên
    return value

def remove_rows_with_size_info(df):
    # Chuyển đổi cột "Kích thước" thành chuỗi
    df['Kích thước'] = df['Kích thước'].astype(str)

    # Tạo một danh sách các chuỗi mô tả kích thước
    size_info_strings = ["Độ dài", "Chiều rộng", "Chiều cao"]

    # Tạo một mặt nạ (mask) để xác định các hàng cần xóa
    mask = df['Kích thước'].str.contains('|'.join(size_info_strings), case=False)

    # Xóa các hàng dữ liệu theo mặt nạ
    df = df[~mask]

    return df

def replace_nan_with_zero(df):
    # Thay thế giá trị NaN thành 0 trong toàn bộ DataFrame
    df.fillna(0, inplace=True)
    return df

def add_zero_to_two_digits(value):
    if isinstance(value, str) and len(value) == 2:
        return value + '0'
    return value


def replace_switch_type(switch):
    replacement_words = ["blue", "cherry", "brown", "silver", "yellow", "pink", "green", "black", "white", "red"]
    if isinstance(switch, str): 
        replaced = False
        for word in replacement_words:
            if word in switch.lower():
                replaced = True
                return word
        if not replaced:
            return random.choice(replacement_words)
    else:
        return random.choice(replacement_words)

def replace_model_with_top_32(df):
    # Đếm số lần xuất hiện của mỗi giá trị trong cột 'Model'
    model_counts = df['Model'].value_counts()

    # Chọn ra 32 giá trị xuất hiện nhiều nhất
    top_33_models = model_counts.head(33).index.tolist()
    
    # Loại trừ giá trị '0' khỏi top 32
    top_32_models = [model for model in top_33_models if model != 0][:32]
    
    # Thay thế các giá trị khác bằng giá trị ngẫu nhiên từ 32 giá trị đã chọn
    replacement_values = np.random.choice(top_32_models, size=len(df))
    df['Model'] = np.where(~df['Model'].isin(top_32_models), replacement_values, df['Model'])
    return df

def handle_missing_size_data_with_KNN(df):
    # Tạo một bản sao của DataFrame chỉ chứa cột cần xử lý
    df['Kích thước'] = pd.to_numeric(df['Kích thước'], errors='coerce')
    X = df[['Kích thước']].values
    # Khởi tạo và huấn luyện mô hình KNN
    imputer = KNNImputer(n_neighbors=15)
    X_imputed = imputer.fit_transform(X)
    # Thay thế cột cần xử lý trong DataFrame với dữ liệu đã được xử lý
    df['Kích thước'] = X_imputed
    return df
def fill_missing_values_random(df, column):
    # Lấy danh sách các giá trị không rỗng trong cột
    non_null_values = df[column].dropna().unique()
    
    # Lấy số lượng dữ liệu trống cần điền
    missing_count = df[column].isnull().sum()
    
    # Tạo một mảng chứa các giá trị ngẫu nhiên từ danh sách các giá trị không rỗng
    random_values = np.random.choice(non_null_values, missing_count)
    
    # Thay thế các dữ liệu trống bằng các giá trị ngẫu nhiên
    df.loc[df[column].isnull(), column] = random_values
    
    return df
def min_max_scaling_size(series):
    min_value = series.min()
    max_value = series.max()
    scaled_series = (series - min_value) / (max_value - min_value)
    return scaled_series
def to_numeric(series):
    return pd.to_numeric(series, errors='coerce')
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
#df = check_and_remove_empty_rows(df)

# Áp dụng hàm remove_special_characters cho cột 'Tên SP' 'Model' 'Kết nối' 'Loại switch'
df['Tên SP'] = df['Tên SP'].apply(remove_special_characters)
df['Model'] = df['Model'].apply(remove_special_characters)
df['Kết nối'] = df['Kết nối'].apply(remove_special_characters)
df['Loại switch'] = df['Loại switch'].apply(remove_special_characters)

df['Loại switch'] = df['Loại switch'].apply(replace_switch_type)

#df = remove_rows_with_size_info(df)

df['Kích thước'] = df['Kích thước'].apply(remove_special_charactersKichThuoc)

df['Kích thước'] = df['Kích thước'].apply(simplify_decimal_to_integer)
df['Kích thước'] = to_numeric(df['Kích thước'])
#df['Kích thước'] = min_max_scaling_size(df['Kích thước'])

df = update_size_column(df)
df['Giá(đ)'] = df['Giá(đ)'].apply(remove_commas)
df['Kích thước'] = df['Kích thước'].apply(simplify_decimal_to_integer)
df = change_connection_values(df)
# df = replace_missing_value(df)
df = update_connection_type(df)
df = replace_model_with_top_32(df)
df = handle_missing_size_data_with_KNN(df)
df = fill_missing_values_random(df,'Kết nối')
df = fill_missing_values_random(df,'Nhà sản xuất')

# df = replace_nan_with_zero(df)
df['Kích thước'] = df['Kích thước'].apply(add_zero_to_two_digits)
df = convert_decimal_to_integer(df)
# Lưu dữ liệu đã được cập nhật vào file CSV
df.to_csv('clean_data.csv', index=False,encoding='utf-8-sig')

print("Kiểm tra và cập nhật dữ liệu thành công. Kết quả đã được lưu vào file 'clean_data.csv'")
