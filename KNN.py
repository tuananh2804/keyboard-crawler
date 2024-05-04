import numpy as np
from sklearn.impute import KNNImputer

# Tạo một tập dữ liệu minh họa với dữ liệu thiếu
X = np.array([[1, 2, np.nan],
              [3, np.nan, 4],
              [np.nan, 5, 6]])

# Khởi tạo và huấn luyện mô hình KNN
imputer = KNNImputer(n_neighbors=2)
X_imputed = imputer.fit_transform(X)

print("Dữ liệu ban đầu:")
print(X)
print("\nDữ liệu sau khi xử lý dữ liệu thiếu bằng KNN:")
print(X_imputed)
