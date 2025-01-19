import streamlit as st
import pandas as pd
import pickle

# Model ve encoders yükle
with open('C:\\Users\\CEMİL EMİN GÜNGÖR\\Linear_model.pkl', 'rb') as file:
    model = pickle.load(file)
    
with open('C:\\Users\\CEMİL EMİN GÜNGÖR\\encoders.pkl', 'rb') as file:
    encoders = pickle.load(file)

with open('C:\\Users\\CEMİL EMİN GÜNGÖR\\model_columns.pkl', 'rb') as file:
    model_columns = pickle.load(file)

st.title("Tarım Yapılacak Alan Bilgileri")

# Kullanıcıdan verileri al
region = st.selectbox(
    "Tarım Yapılacak Bölgeyi Seçiniz",
    encoders['Region'].classes_
)
st.write("""
- **Region**: 
  - East: 0 
  - North: 1 
  - South: 2 
  - West: 3
""")

soil_type = st.selectbox(
    "Tarım Yapacağınız Toprak Türünü Seçiniz",
    encoders['Soil_Type'].classes_
)
st.write("""
- **Soil_Type**:
  - Clay: 0
  - Loam: 1
  - Marshy: 2
  - Sandy: 3
  - Silt: 4
  - Peaty: 5
""")

crop = st.selectbox(
    "Tarım Yapacağınız Ürünü Seçiniz",
    encoders['Crop'].classes_
)
st.write("""
- **Crop**:
  - Barley: 0
  - Cotton: 1
  - Maize: 2
  - Rice: 3
  - Soybean: 4
  - Wheat: 5
""")

rainfall_mm = st.number_input("Ortalama Yağış Miktarı (mm):", min_value=0.0)
temperature_celsius = st.number_input("Ortalama Sıcaklık (Celsius):", min_value=-50.0, max_value=50.0)
fertilizer_used = st.selectbox("Gübre Kullanılacak mı:", [False, True])
irrigation_used = st.selectbox("Sulama Kullanılacak mı:", [False, True])
weather_condition = st.selectbox(
    "Tarım Yapılacak Mevsim",
    encoders['Weather_Condition'].classes_
)
st.write("""
- **Weather_Condition**:
  - Cloudy: 0
  - Rainy: 1
  - Sunny: 2
""")

days_to_harvest = st.number_input("Hasat Edilecek Gün:", min_value=0)

if st.button("Tahmin Et"):
    # Girdi verilerinin dönüştürülmesi
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

    for kolon in ['Region', 'Soil_Type', 'Crop', 'Weather_Condition']:
        input_data[kolon] = encoders[kolon].transform(input_data[kolon])

    # Eksik sütunları doldur
    for col in model_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[model_columns]

    # Tahmin yap
    prediction = model.predict(input_data)

    # Tahmini göster
    st.write("### Tahmin Sonucu")
    st.write(f"Tahmini Verim: {prediction[0]} ton/hektar")
