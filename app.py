import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Personal AI Photo Sorter", page_icon="📁", layout="centered")

st.title("📁 Personal AI Photo Sorter")
st.markdown("Upload your photos below and let AI sort them into your exact categories!")

# Automatically load API key from Streamlit Secrets if available, otherwise show input box
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Enter your Gemini API key:", type="password")

if not api_key:
    st.warning("Please enter your Gemini API key above to unlock the app.")
    st.stop()

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Multi-image uploader
uploaded_files = st.file_uploader("Choose images from your device...", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"Successfully loaded {len(uploaded_files)} image(s).")
    
    if st.button("🚀 Sort and Classify Photos"):
        st.markdown("---")
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(image, caption=uploaded_file.name, width=150)
                
            with col2:
                with st.spinner(f"Analyzing {uploaded_file.name} ..."):
                    try:
                        prompt = """
                        Analyze this image carefully. You are an expert classifier for a personal gallery.
                        Classify this image into EXACTLY ONE of these primary categories:
                        1. Vehicles (Sedans, SUVs, Sports Cars, Bikes, etc.)
                        2. Firearms (Assault Rifles, SMGs, Pistols, Revolvers, Shotguns, etc.)
                        3. Tactical & Outdoor Gear (Body armor, plate carriers, camping tents, backpacks, survival gear, etc.)
                        4. Food & Meals (Home-cooked dishes, snacks, restaurant items, etc.)
                        5. Clothing & Apparel (Shirts, jackets, trousers, activewear, etc.)
                        6. Accessories (Watches, sunglasses, belts, hats, shoes, wallets, etc.)
                        7. General / Other (Screenshots, random notes, scenery, or anything else)

                        Provide your response in this strict layout:
                        * **Category:** [Choose one from the list above]
                        * **Specific Details:** [Name the exact vehicle model, firearm type, armor piece, dish, or item seen]
                        * **Reason:** [1 brief sentence]
                        """
                        
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=[image, prompt],
                        )
                        
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error processing image: {e}")
            st.markdown("---")
            
