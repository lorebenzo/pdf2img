import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
import PyPDF2
from concurrent.futures import ThreadPoolExecutor

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
        
        .page-header {
            color: #2F4F4F;
            margin-bottom: 1rem;
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
        # type=["pdf"], # commented out to allow all file types, to retrieve errors from the BE
        label_visibility="collapsed",
    )

def split_pdf_into_pages(pdf_bytes) -> list[tuple[int, bytes]]:
    """Split PDF into individual pages"""
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    pages = []
    
    # foreach page take the bytes and store it in a list (page_num, page_bytes)
    for i, page in enumerate(pdf_reader.pages):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(page)
        page_bytes = BytesIO()
        pdf_writer.write(page_bytes)
        page_bytes.seek(0)
        pages.append((i + 1, page_bytes.getvalue()))
    return pages

# convert single page
def convert_page(page_data) -> tuple[int, bytes, str]:
    page_num, page_bytes = page_data
    try:
        files = {
            "file": (
                f"page_{page_num}.pdf",
                page_bytes,
                "application/pdf",
            )
        }
        response = requests.post(API_URL, files=files, verify=False)
        if response.status_code == 200:
            return (page_num, response.content, None)
        return (page_num, None, response.json().get('detail', 'Unknown error'))
    except Exception as e:
        return (page_num, None, str(e))

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

    try:
        # split pdf into individual pages
        with st.spinner("🔨 Splitting PDF into individual pages..."):
            pdf_bytes = uploaded_file.getvalue()
            pages = split_pdf_into_pages(pdf_bytes)
            num_pages = len(pages)
            st.markdown(f"**📄 Number of pages detected:** {num_pages}")

        # convert pages to PNG
        with st.spinner(f"✨ Converting {num_pages} pages in parallel..."):
            with ThreadPoolExecutor() as executor:
                results = executor.map(convert_page, pages)

            # Process results
            success_pages = []
            errors = []
            for page_num, img_data, error in results:
                if error:
                    errors.append((page_num, error))
                else:
                    success_pages.append((page_num, img_data))

            # disaply errors
            if errors:
                st.error(f"Failed to convert {len(errors)} pages:")
                for page_num, error in errors:
                    st.error(f"Page {page_num}: {error}")

            if success_pages:
                st.success(f"✅ Successfully converted {len(success_pages)} pages!")
                
                for page_num, img_data in success_pages:
                    with st.container():
                        # download button on the right side
                        col1, col2 = st.columns([0.8, 0.2])
                        with col1:
                            st.markdown(f"<h4 class='page-header'>📄 Page {page_num}</h4>", unsafe_allow_html=True)
                            img = Image.open(BytesIO(img_data))
                            st.image(img, use_container_width=True)
                        
                        with col2:
                            st.download_button(
                                label=f"⬇️ Page {page_num}",
                                data=img_data,
                                file_name=f"page_{page_num}.png",
                                mime="image/png",
                                key=f"download-{page_num}",
                            )

    except PyPDF2.errors.PdfReadError:
        st.error("Invalid PDF file. Please upload a valid PDF document.")
    except Exception as e:
        st.error(f"🚨 Unexpected Error: {str(e)}")