import os
import pickle
import streamlit as st
import pandas as pd
from google.auth import exceptions
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from sklearn.preprocessing import LabelEncoder

# Google Drive API için gerekli ayarlar
SERVICE_ACCOUNT_FILE = r'C:\Users\CEMİL EMİN GÜNGÖR\Desktop\composite-bruin-448609-g1-fe0f5d8afb6c.json'
# Servis hesabı JSON dosyasının yolu (yeni dosya adıyla)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Servis hesabını yükleme
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive API servisini başlatma
service = build('drive', 'v3', credentials=credentials)

# Dosya ID'si ve indirme işlemi
file_id = '1GP_yrRY4uKQLfVbAs8t0uvQiFpf8S6rr'  # Google Drive dosyasının ID'si
request = service.files().get_media(fileId=file_id)

# İndirilecek dosyanın yolu
file_name = 'Linear_model.pkl'
with open(file_name, 'wb') as file:
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"İndirilme durumu: {int(status.progress() * 100)}%")

print(f"{file_name} başarıyla indirildi.")

# Modeli yükle
with open(file_name, 'rb') as file:
    model = pickle.load(file)

# Başlık
st.title("Tarım Yapılacak Alan Bilgileri")

# Kullanıcıdan verileri al
region = st.selectbox(
    "Tarım Yapılacak Bölgeyi Seçiniz",
    ["Bölge 1", "Bölge 2", "Bölge 3"]
)

soil_type = st.selectbox(
    "Tarım Yapacağınız Toprak Türünü Seçiniz",
    ["Toprak Türü 1", "Toprak Türü 2", "Toprak Türü 3"]
)

crop = st.selectbox(
    "Tarım Yapacağınız Ürünü Seçiniz",
    ["Ürün 1", "Ürün 2", "Ürün 3"]
)

rainfall_mm = st.number_input("Ortalama Yağış Miktarı (mm):", min_value=0.0)
temperature_celsius = st.number_input("Ortalama Sıcaklık (Celsius):", min_value=-50.0, max_value=50.0)
fertilizer_used = st.selectbox("Gübre Kullanılacak mı:", [False, True])
irrigation_used = st.selectbox("Sulama Kullanılacak mı:", [False, True])

weather_condition = st.selectbox(
    "Tarım Yapılacak Mevsim",
    ["Mevsim 1", "Mevsim 2", "Mevsim 3"]
)

days_to_harvest = st.number_input("Hasat Edilecek Gün:", min_value=0)

if st.button("Tahmin Et"):
    # Kategorik verileri dönüştürme
    label_encoder_region = LabelEncoder()
    label_encoder_soil_type = LabelEncoder()
    label_encoder_crop = LabelEncoder()
    label_encoder_weather_condition = LabelEncoder()

    input_data = pd.DataFrame({
        'Rainfall_mm': [rainfall_mm],
        'Temperature_Celsius': [temperature_celsius],
        'Fertilizer_Used': [int(fertilizer_used)],
        'Irrigation_Used': [int(irrigation_used)],
        'Days_to_Harvest': [days_to_harvest],
        'Region': [region],
        'Soil_Type': [soil_type],
        'Crop': [crop],
        'Weather_Condition': [weather_condition]
    })

    # Kategorik verileri dönüştürme
    input_data['Region'] = label_encoder_region.fit_transform(input_data['Region'])
    input_data['Soil_Type'] = label_encoder_soil_type.fit_transform(input_data['Soil_Type'])
    input_data['Crop'] = label_encoder_crop.fit_transform(input_data['Crop'])
    input_data['Weather_Condition'] = label_encoder_weather_condition.fit_transform(input_data['Weather_Condition'])

    # Modelin sütun sırasını ayarlama
    model_columns = ['Rainfall_mm', 'Temperature_Celsius', 'Fertilizer_Used', 'Irrigation_Used', 
                     'Days_to_Harvest', 'Region', 'Soil_Type', 'Crop', 'Weather_Condition']

    for col in model_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[model_columns]

    # Tahmin yap
    prediction = model.predict(input_data)

    # Tahmini göster
    st.write("### Tahmin Sonucu")
    st.write(f"Tahmini Verim: {prediction[0]:.2f} ton/hektar")
