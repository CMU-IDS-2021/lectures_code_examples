import streamlit as st
import pandas as pd
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser

__authors__ = "Hendrik Strobelt"

st.set_page_config(layout="wide")


@st.cache
def open_index():
    storage = FileStorage("index")
    return storage.open_index()


index = open_index()

q_string = st.text_input("Query","vis")

with index.searcher() as s:
    q = QueryParser("abstract", index.schema).parse(q_string)
    st.write(q)
    results = s.search(q)
    for r in results:
        st.markdown(f"<div style='background-color:lightgray; padding:3pt;margin:1pt;border-radius:5px;'><span style='font-size:16pt'>{r['title']}</span> "
                    f"<span style='font-size:9pt'>({round(r.score,3)})</span><br>"
                    f"{r.highlights('abstract')}</div>", unsafe_allow_html=True)
        # st.markdown(r.highlights('abstract'), unsafe_allow_html=True)
