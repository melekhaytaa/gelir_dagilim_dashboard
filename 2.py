import streamlit as st
import pandas as pd
import plotly.express as px

# Veriyi yükle
df = pd.read_excel('/Users/melekhayta/Desktop/potansiyel_musteri_hesaplama/data/verilerim.xlsx')

# Başlık
st.title('Gelir Dashboard\'u')

# Başlık altı açıklama
st.markdown("""
    **Bu dashboard**, gelir analizlerini ve kategorilere göre gelir dağılımını görselleştiren, 
    aynı zamanda zaman içindeki değişimi gözler önüne seren interaktif bir platformdur.
""")

# Kolonları kullanarak sayfada düzenleme
col1, col2 = st.columns(2)  # 2 kolon oluşturuyoruz

# 1. Kolon: Gelir Kategorileri Grafiği
with col1:
    # Gelir Kategorilere Göre Dağılım
    gelir_by_kategori = df.groupby('Description')['UnitPrice'].sum()
    fig_gelir_kategori = px.bar(gelir_by_kategori,
                                 x=gelir_by_kategori.index,
                                 y=gelir_by_kategori.values,
                                 labels={'x': 'Description', 'y': 'UnitPrice'},
                                 title='Gelir Kategorilere Göre',
                                 color=gelir_by_kategori.index)
    fig_gelir_kategori.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14, color="black"),
        title_font=dict(size=16, family="Arial, sans-serif"),
        showlegend=False
    )
    st.plotly_chart(fig_gelir_kategori, use_container_width=True)

# 2. Kolon: Zaman Serisi Gelir Değişimi
with col2:
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    gelir_by_tarih = df.groupby(df['InvoiceDate'].dt.to_period('M'))['UnitPrice'].sum()
    fig_zaman_serisi = px.line(gelir_by_tarih,
                               x=gelir_by_tarih.index.astype(str),
                               y=gelir_by_tarih.values,
                               labels={'x': 'InvoiceDate', 'y': 'UnitPrice'},
                               title='Zamanla Gelir Değişimi',
                               color_discrete_sequence=["#ff6347"])
    fig_zaman_serisi.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14, color="black"),
        title_font=dict(size=16, family="Arial, sans-serif")
    )
    st.plotly_chart(fig_zaman_serisi, use_container_width=True)

# Widgetlar
st.write("### Gelir Kategorisi Seçimi")
kategori_sec = st.selectbox(
    'Bir kategori seçin:',
    df['Description'].unique()
)

# Seçilen Kategori için Gelir Grafik
st.write(f"Seçilen Kategori: {kategori_sec}")
kategori_data = df[df['Description'] == kategori_sec]
kategori_gelir = kategori_data.groupby('InvoiceDate')['UnitPrice'].sum()
fig_kategori_gelir = px.line(kategori_gelir,
                             x=kategori_gelir.index.astype(str),
                             y=kategori_gelir.values,
                             title=f"{kategori_sec} Kategorisi için Gelir Değişimi")
fig_kategori_gelir.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14, color="black"),
    title_font=dict(size=16, family="Arial, sans-serif")
)
st.plotly_chart(fig_kategori_gelir, use_container_width=True)

# Slider ile Gelir Değeri
st.write("### Gelir Değeri Seçimi")
gelir_slider = st.slider(
    'Gelir Değer Aralığını Seçin:',
    min_value=int(df['UnitPrice'].min()),
    max_value=int(df['UnitPrice'].max()),
    value=(int(df['UnitPrice'].min()), int(df['UnitPrice'].max()))
)

# Slider ile belirlenen aralıkta veriyi filtreleyip gösterme
filtered_data = df[(df['UnitPrice'] >= gelir_slider[0]) & (df['UnitPrice'] <= gelir_slider[1])]
st.write(f"Seçilen Gelir Aralığı: {gelir_slider[0]} - {gelir_slider[1]}")

# Kategorilere Göre Gelir
st.write("### Kategorilere Göre Gelir Dağılımı (Seçilen Aralıkta)")
gelir_by_kategori_filtered = filtered_data.groupby('Description')['UnitPrice'].sum()
fig_gelir_kategori_filtered = px.bar(gelir_by_kategori_filtered,
                                     x=gelir_by_kategori_filtered.index,
                                     y=gelir_by_kategori_filtered.values,
                                     labels={'x': 'Description', 'y': 'UnitPrice'},
                                     title="Seçilen Gelir Aralığına Göre Kategoriler")
fig_gelir_kategori_filtered.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14, color="black"),
    title_font=dict(size=16, family="Arial, sans-serif")
)
st.plotly_chart(fig_gelir_kategori_filtered, use_container_width=True)

# Sayfanın sonunda açıklamalar
st.markdown("""
    #### Dashboard Özeti:
    - **Gelir Kategorilere Göre**: Bu grafik, her bir kategori için toplam geliri gösteriyor.
    - **Zamanla Gelir Değişimi**: Zaman içindeki gelir değişimini incelemek için kullanabilirsiniz.
    - **Kategori Seçimi**: Belirli bir kategoriyi seçerek o kategoriye ait gelir trendlerini görselleştirebilirsiniz.
    - **Gelir Aralığı Seçimi**: Slider ile belirlediğiniz gelir aralığındaki verileri filtreleyebilir ve bu aralıkta yer alan gelirleri gösterebilirsiniz.
""")

# Estetik Stil
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f4f9;
            color: #333;
        }
        .css-1v3fvcr {
            padding: 20px;
            margin: 10px;
            font-size: 18px;
        }
        .stSelectbox, .stSlider {
            font-size: 16px;
            background-color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

