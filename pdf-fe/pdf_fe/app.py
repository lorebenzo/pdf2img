import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

# backend API URL
API_URL = os.environ["API_URL"]

st.set_page_config(
    page_title="PDF to PNG Converter",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# bad hack to add custom CSS
st.markdown(
    """
    <style>
        .main {
            background-color: #F5F5F5;
        }
        h1 {
            color: #2F4F4F;
            text-align: center;
        }
        .stFileUploader {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        [data-testid="stBaseButton-secondary"] { 
            background-color: #2F4F4F !important; 
            color: white !important; 
            border-radius: 5px; 
            padding: 10px 24px;
            border: none;
        }   
        
        .success-msg {
            background-color: #E8F5E9; 
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0; 
        }

        .download-button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px 24px;
        }
        .sidebar .sidebar-content {
            background-color: #2F4F4F;
            color: white;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📄 PDF to PNG Converter ✨")

# sidebar section
with st.sidebar:
    st.header("About")
    st.write(
        """
    **PDF to PNG Converter** is a simple web application that allows you to convert PDF files to images.
    """
    )
    st.markdown("---")

# upload section
with st.container():
    st.subheader("📤 Upload Your PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        # type=["pdf"], # Commented out to allow all file types, to retrieve errors from the BE
        label_visibility="collapsed",
    )

if uploaded_file is not None:
    st.markdown(
        f"""
        <div class="success-msg">
            📑 File uploaded: <strong>{uploaded_file.name}</strong><br>
            📏 Size: {(uploaded_file.size / (1024 ** 2)):.2f} MB
        </div>
    """,
        unsafe_allow_html=True,
    )

    # spinner for conversion
    with st.spinner("✨ Converting PDF to image...", show_time=True):
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }
            response = requests.post(API_URL, files=files, verify=False)

            if response.status_code == 200:
                st.markdown(
                    '<p class="success-msg">✅ Conversion Successful!</p>',
                    unsafe_allow_html=True,
                )

                image = Image.open(BytesIO(response.content))
                with st.container():
                    st.image(
                        image,
                        caption="Converted Image Preview",
                        use_container_width=True,
                        output_format="PNG",
                    )

                st.download_button(
                    label="⬇️ Download Image",
                    data=response.content,
                    file_name="converted_image.png",
                    mime="image/png",
                    key="download-btn",
                    help="Click here to download the converted image",
                )

            else:
                st.error(
                    f"🚨 Conversion Error: {response.json().get('detail', 'Unknown error')}"
                )

        except Exception as e:
            st.error(f"🚨 Unexpected Error: {str(e)}")
