import streamlit as st
from openai import OpenAI
import requests
import base64

# title and description.
st.title("Image Captioning Bot")
st.write(
    "Provide the bot with either an image URL or file upload and let it write your captions for you!"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# initialize session state
if "url_response" not in st.session_state:
    st.session_state.url_response = None

if "upload_response" not in st.session_state:
    st.session_state.upload_response = None

st.subheader("Image URL Input")
st.write("Input your image url here")
url = st.text_input("Image URL")
st.caption("Ensure link leads directly to the image and not a webpage with images on it.")

# button for api call
if st.button("Generate Caption for Inputted URL"):
    url_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": url, "detail": "auto"}},
                {"type": "text", "text": "Describe the image in at least 3 sentences. Write five different captions for this image."
                "Captions must vary in length, minimum one word but be no longer than 2 sentences."
                "Captions should vary in tone, such as, but not limited to funny, intellectual, and aesthetic."}
            ]
        }]
    )
    st.session_state.url_response = url_response.choices[0].message.content

# write response
if st.session_state.url_response:
    st.image(url, use_container_width=True)
    st.write(st.session_state.url_response)

st.subheader("Image Upload Input")
st.write("Upload your image here")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "gif"])

if st.button("Generate Caption for Uploaded Image") and uploaded:
    b64 = base64.b64encode(uploaded.read()).decode("utf-8")
    mime = uploaded.type  # e.g. "image/png"
    data_uri = f"data:{mime};base64,{b64}"

    upload_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": data_uri, "detail": "low"}},
                {"type": "text", "text": "Describe the image in at least 3 sentences. Write five different captions for this image."
                "Captions must vary in length, minimum one word but be no longer than 2 sentences."
                "Captions should vary in tone, such as, but not limited to funny, intellectual, and aesthetic."}
            ]
        }]
    )
    st.session_state.upload_response = upload_response.choices[0].message.content

# write response
if st.session_state.upload_response:
    st.image(uploaded, use_container_width=True)
    st.write(st.session_state.upload_response)
