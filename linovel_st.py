from typing import List
import streamlit as st
from epub import Epub
from novel_oldlinovel import OldLinovel
from novel_360dxs import Dxs
from novel_wenku8 import Wenku
from novel import AbstractNovel

st.set_page_config(page_title="Novel Downloader", page_icon=":book:")
st.title("📗Novel Downloader")

url = st.text_input("Novel URL")
start_download = st.button("Download")

@st.cache_data(ttl="1d")
def download_book(url: str) -> List[str]:
    r = []
    for cls in [OldLinovel, Dxs, Wenku]:
        if cls.check_url(url):
            novel:AbstractNovel = cls(url, False)
            novel.extract_novel_information()
            books = novel.get_novel_information()
            for book in books:
                epub = Epub(single_thread=False, **book)
                file_name = epub.generate_file()
                st.info(f"Downloaded {file_name}")
                r.append(file_name)
            break
    return r

if start_download:
    file_names = []
    with st.spinner("Downloading..."):
        file_names = download_book(url)
    for file_name in file_names:
        with open(file_name, "rb") as f:
            file = f.read()
            st.download_button(label=file_name, data=file, file_name=file_name)
