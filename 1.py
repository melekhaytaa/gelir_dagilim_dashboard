
import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
from matplotlib.lines import lineStyles
from sympy.printing.pretty.pretty_symbology import line_width

# Veriyi içe aktarma
data = pd.read_excel('data/verilerim.xlsx')
print(data.head())
print(data.info())

#eksik verileri temizleme

missing_data = data.isnull().sum()
print("Eksik Veri Sayısı:")
print(missing_data)

cleaned_data = data.dropna()

cleaned_missing_data = cleaned_data.isnull().sum()
print("\nTemizlendikten Sonra Eksik Veri Sayısı:")
print(cleaned_missing_data)

print("\nTemizlenmiş Veri Seti:")
print(cleaned_data.head())

data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
plt.figure(figsize=(10,6))
plt.plot(data["InvoiceDate"],data["UnitPrice"], marker="o", color="r")

plt.title('Toplam Gelir Zaman Serisi')
plt.xlabel('Tarih')
plt.xlabel('Gelir')

plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()