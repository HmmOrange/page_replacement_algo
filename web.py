import streamlit as st
pages = {
    "Bộ nhớ ảo": [
        st.Page("page_replacement.py", title="Thuật toán thay thế trang"),
        st.Page("belady_anomaly.py", title="Hiện tượng bất thường Bélády")
    ],
}

pg = st.navigation(pages)
pg.run()