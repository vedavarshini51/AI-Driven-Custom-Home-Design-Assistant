import streamlit as st
import google.generativeai as genai
import requests

# Configure Gemini API Key
api_key = "AIzaSyD0_7wmxlhPnw9IUAjtPmhWXRTmTY7ArnY"
genai.configure(api_key=api_key)

# Define model parameters
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Function to generate home design ideas
def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config)
    
    context = f"""
    Generate a custom home design plan based on these inputs:
    - Style: {style}
    - Size: {size}
    - Number of rooms: {rooms}

    Include:
    - Layout suggestions
    - Color schemes
    - Furniture recommendations
    - Preferred materials
    """
    
    response = model.generate_content(context)
    
    return response.text if isinstance(response.text, str) else response.text[0]

# Function to fetch an image from Lexica.art
def fetch_image_from_lexica(style):
    lexica_url = f"https://lexica.art/api/v1/search?q={style} home design"
    response = requests.get(lexica_url)

    if response.status_code == 200:
        data = response.json()
        st.write("Lexica API Response:", data)  # Debugging output in Streamlit
        if data.get('images') and len(data['images']) > 0:
            return data['images'][0]['src']
    return None

# Streamlit UI
st.title("🏡 AI-Driven Custom Home Design Assistant")

style = st.text_input("Enter the home design style (e.g., Modern, Rustic)")
size = st.text_input("Enter the size of the home (e.g., 2000 sq ft)")
rooms = st.text_input("Enter the number of rooms")

if st.button("Generate Design"):
    if style and size and rooms:
        design_idea = generate_design_idea(style, size, rooms)
        image_url = fetch_image_from_lexica(style)
        
        st.markdown("### 🏠 Custom Home Design Idea")
        st.markdown(design_idea)

        if image_url:
            st.image(image_url, caption="Design inspiration from lexica.art")
        else:
            st.warning("⚠ No relevant images found on Lexica.art. Showing a default image.")
            st.image("https://via.placeholder.com/500", caption="Default Image")
    else:
        st.warning("⚠ Please fill in all the fields.")
