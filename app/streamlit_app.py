import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="House Price Demo", page_icon="🏠")
st.title("🏠 House Price Prediction")
st.caption("Enter property details to get an estimated price")

with st.form("form"):
    col1, col2 = st.columns(2)

    with col1:
        area             = st.number_input("Area (sq ft)",    min_value=100,  max_value=20000, value=5000)
        bedrooms         = st.number_input("Bedrooms",         min_value=1,    max_value=10,    value=3)
        bathrooms        = st.number_input("Bathrooms",        min_value=1,    max_value=10,    value=2)
        stories          = st.number_input("Stories",          min_value=1,    max_value=5,     value=2)
        parking          = st.number_input("Parking spots",    min_value=0,    max_value=5,     value=1)
        furnishingstatus = st.selectbox("Furnishing", ["furnished", "semi-furnished", "unfurnished"])

    with col2:
        mainroad        = st.selectbox("Main road",          ["yes", "no"])
        guestroom       = st.selectbox("Guest room",         ["yes", "no"])
        basement        = st.selectbox("Basement",           ["yes", "no"])
        hotwaterheating = st.selectbox("Hot water heating",  ["yes", "no"])
        airconditioning = st.selectbox("Air conditioning",   ["yes", "no"])
        prefarea        = st.selectbox("Preferred area",     ["yes", "no"])

    submitted=st.form_submit_button("Predict Price", use_container_width=True)

if submitted:
    payload = {
        "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
        "stories": stories, "parking": parking, "furnishingstatus": furnishingstatus,
        "mainroad": mainroad, "guestroom": guestroom, "basement": basement,
        "hotwaterheating": hotwaterheating, "airconditioning": airconditioning,
        "prefarea": prefarea
    }

    try:
        res=requests.post(API_URL,json=payload,timeout=5)
        if res.status_code==200:
            r=res.json()
            st.divider()
            st.success(f"Estimated Price: ₹{r['predicted_price']:,.0f}")
            c1, c2 = st.columns(2)
            c1.metric("Low estimate",  f"₹{r['price_range_low']:,.0f}")
            c2.metric("High estimate", f"₹{r['price_range_high']:,.0f}")
        else:
            try:
                error_msg = res.json().get("detail", "Unknown error")
            except Exception:
                error_msg = res.text  # fallback when response is not JSON

            st.error(f"Error {res.status_code}: {error_msg}")
    except requests.exceptions.ConnectionError:
        st.error("cant connect to api . make sure fastapi is running")
