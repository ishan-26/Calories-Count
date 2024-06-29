from distutils.command import upload
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


load_dotenv()  ## load all the environment variables


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    # ... (your existing code)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([input_prompt, image[0]])

    text = response.text
    return text

def input_image_setup(uploaded_file):
    # check if file uploaded or not
    if uploaded_file is not None:
        # read the bytes of file
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts

    else:
        print("No file uploaded")

# initialize streamlit app

st.set_page_config(page_title="Calories Advisor")
st.header("Calories Count")

uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    #instructs Streamlit to use the image's natural width, but not exceeding the column width.
    st.image(image,use_column_width=True)

submit = st.button("Tell me about the total calories of the dish")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items present in the imagewith calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
Finally you can also mention whether the food is healthy or not. Additionally, you strictly need to furnish a breakdown
of each food item along with its respective content in points:

    Food Item
    Serving Size
    Total Cal.
    Protein (g)
    Fat (g)
    Carbs (g)
    Fiber (g)
    Vit B-12 (mcg)
    Vit B-6 (mg)
    Iron (mg)
    Zinc (mg)
    Manganese (mg).

Also if the total calories of the dish is less than the required then suggest some more Indian dishes vegeterian and non-vegetarian
to include in the dish for different course seperately in the form of list. Do not include the dishes that are already present in the image and not exceeding the total calories required for the day.

Only respond if the image pertains to the food items else respond with not appropriate image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)

    st.subheader("Your dish summary:")
    st.write(response)
