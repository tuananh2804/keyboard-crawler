import pandas as pd

# Đọc các tệp CSV vào các DataFrame
df1 = pd.read_csv('clean_data.csv')
df2 = pd.read_csv('clean_data_anphat.csv')

# Ghép các DataFrame lại với nhau
merged_df = pd.concat([df1, df2])
print(merged_df)
# Lưu DataFrame ghép lại thành tệp CSV

merged_df.to_csv('Data_Clean.csv', index=False, encoding='utf-8-sig')
print("Kiểm tra và cập nhật dữ liệu thành công. Kết quả đã được lưu vào file '.csv'")
