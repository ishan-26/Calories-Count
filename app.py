from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


load_dotenv()  ## load all the environment variables


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

def get_gemini_response(input_prompt, image):
    # ... (your existing code)
 model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config,)
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
You are an expert nutritionist. Your task is to analyze an image of food items and calculate the total calories present in the image. You should provide details of each food item with calorie intake in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

Additionally, provide a detailed nutritional breakdown for each food item with the following content in points:

    Food Item
    Serving Size
    Total Calories
    Protein (g)
    Fat (g)
    Carbs (g)
    Fiber (g)
    Vitamin B-12 (mcg)
    Vitamin B-6 (mg)
    Iron (mg)
    Zinc (mg)
    Manganese (mg)

Finally, assess whether the food is healthy or not. If the total calories of the dish are less than the required daily intake, suggest some additional Indian dishes (both vegetarian and non-vegetarian) to include in different courses, ensuring the total daily calorie requirement is met. Do not include dishes already present in the image.

Only respond if the image pertains to food items, else respond with "Not an appropriate image."
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)

    st.subheader("Your dish summary:")
    st.write(response)
