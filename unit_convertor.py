import streamlit as st  
import pyperclip
import requests

# Theme Toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

# Set colors based on theme
if dark_mode:
    bg_color = "#121212"
    text_color = "white"
    card_bg = "rgba(255, 255, 255, 0.1)"
    btn_bg = "linear-gradient(135deg, #00c8ff, #005f73)"
    btn_hover = "linear-gradient(135deg, #00a2ff, #004a5e)"
else:
    bg_color = "#f5f5f5"
    text_color = "black"
    card_bg = "white"
    btn_bg = "linear-gradient(135deg, #007bff, #0056b3)"
    btn_hover = "linear-gradient(135deg, #0056b3, #003f7f)"

# Styling
st.markdown(f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Arial', sans-serif;
    }}
    .stApp {{
        background: {bg_color};
        padding: 30px;
        border-radius: 15px;
    }}
    h1 {{
        text-align: center; 
        font-size: 40px;
        color: {text_color};
        font-weight: bold;
    }}
    .stButton>button {{
        background: {btn_bg};
        color: white;
        border: none;
        padding: 12px 25px;
        transition: all 0.3s ease;
        font-size: 18px;
        border-radius: 8px;
    }}
    .stButton>button:hover {{
        background: {btn_hover};
        transform: scale(1.05);
        color: black;
    }}
    .result-box {{
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        background-color: {card_bg};
        padding: 20px;
        margin-top: 20px;
        border-radius: 10px;
        box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.3);
    }}
    .footer {{
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: {text_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# Title & Description
st.markdown(f"""
    <h1>🌍 Smart Unit Converter</h1>
    <p style="text-align: center; font-size: 18px; color: {text_color};">
    Easily convert Length, Weight, Temperature, and Currency with precision! ⚡
    </p>
""", unsafe_allow_html=True)

# Sidebar menu
conversion_type = st.sidebar.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature", "Currency"])
value = st.number_input("Enter Value", min_value=0.0, step=0.1)

col1, col2 = st.columns(2)

if conversion_type == "Length":
    with col1:
        from_unit = st.selectbox("From", ["centimeters", "meters", "kilometers", "miles", "feet", "yards", "inches"])
    with col2:
        to_unit = st.selectbox("To", ["centimeters", "meters", "kilometers", "miles", "feet", "yards", "inches"])

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From", ["grams", "kilograms", "pounds", "ounces", "milligrams"])
    with col2:
        to_unit = st.selectbox("To", ["grams", "kilograms", "pounds", "ounces", "milligrams"])

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])

elif conversion_type == "Currency":
    with col1:
        from_unit = st.text_input("From (Currency Code)", "USD")
    with col2:
        to_unit = st.text_input("To (Currency Code)", "PKR")


# Conversion Functions
def length_converter(value, from_unit, to_unit):
    length_units = {
        "centimeters": 0.01, "meters": 1, "kilometers": 1000,
        "miles": 1609.34, "feet": 0.3048, "yards": 0.9144, "inches": 0.0254
    }
    return value * (length_units[to_unit] / length_units[from_unit])

def weight_converter(value, from_unit, to_unit):
    weight_units = {
        "grams": 1, "kilograms": 1000, "pounds": 453.592,
        "ounces": 28.3495, "milligrams": 0.001
    }
    return value * (weight_units[to_unit] / weight_units[from_unit])

def temperature_converter(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        return value * 9/5 + 32 if to_unit == "Fahrenheit" else value + 273.15
    if from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15
    if from_unit == "Kelvin":
        return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32

def currency_converter(value, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url).json()
    if to_currency in response["rates"]:
        return value * response["rates"][to_currency]
    return None

# Convert Button
if st.button("Convert 🚀"):
    result = None
    if conversion_type == "Length":
        result = length_converter(value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = weight_converter(value, from_unit, to_unit)
    elif conversion_type == "Temperature":
        result = temperature_converter(value, from_unit, to_unit)
    elif conversion_type == "Currency":
        result = currency_converter(value, from_unit, to_unit)

    if result is not None:
        st.markdown(f'<div class="result-box">🔹 Result: {result:.2f} {to_unit}</div>', unsafe_allow_html=True)
        if st.button("📋 Copy Result"):
            pyperclip.copy(f"{result:.2f} {to_unit}")
            st.success("Copied to clipboard!")
    else:
        st.error("Conversion Error! Please check inputs.")

st.markdown(f"<p class='footer'>Made with ❤️ by Vandana Chohan</p>", unsafe_allow_html=True)
