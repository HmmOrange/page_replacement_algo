import streamlit as st
import pandas as pd
from algo import *
from table import *

st.set_page_config(
    page_title = "Page Replacement Algorithms",
    page_icon = "📄",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'Get help': 'https://github.com/HmmOrange/page-replacement-algo',
        'About': "# Made with 💖\nhttps://github.com/HmmOrange/page-replacement-algo",
    }
)


st.title("Thuật toán thay thế trang")

pages_input = st.sidebar.text_input("Chuỗi số hiệu", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1")
pages = pages_input.replace(",", " ").replace("  ", " ").split()

algo_options = [
    "FIFO - Vào trước ra trước", 
    "OPT - Tối ưu", 
    "LRU - Đã không sử dụng lâu nhất", 
    "MRU - Đã không sử dụng gần nhất", 
    "LFU - Tần suất sử dụng thấp nhất",
    "MFU - Tần suất sử dụng cao nhất",
    "Second chance - Cơ hội thứ hai"
]

checkbox_options = []
for option in algo_options:
    checkbox = st.sidebar.checkbox(option)
    if checkbox:
        checkbox_options.append(option)


frame_size = st.sidebar.slider("Số lượng frame", 1, 10, 3)

                        
if len(checkbox_options):
    for i in checkbox_options:
        if i == algo_options[0]:
            page_faults, history = fifo(pages, frame_size)
        elif i == algo_options[1]:
            page_faults, history = opt(pages, frame_size)
        elif i == algo_options[2]:
            page_faults, history = lru(pages, frame_size)
        elif i == algo_options[3]:
            page_faults, history = mru(pages, frame_size)
        elif i == algo_options[4]:
            page_faults, history = lfu(pages, frame_size)
        elif i == algo_options[5]:
            page_faults, history = mfu(pages, frame_size)
        else:
            page_faults, history = second_chance(pages, frame_size)

        st.subheader(i, divider = "blue")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"Total Pages: {len(pages)}")
            st.write(f"Total Page Faults: {page_faults}")
            st.write(f"Hit Rate: {round((len(pages) - page_faults) / len(pages) * 100, 2)}%")

        # Creating table
        vertical_history = []
        vertical_history.append(pages)
        for i in range(frame_size):
            vertical_history.append([])
            for j in range(len(history)):
                if i < len(history[j]):
                    vertical_history[i + 1].append(history[j][i] if history[j][i] != None else "\u200b")

        # df = pd.DataFrame(vertical_history, columns = (i for i in range(len(pages))))
        # # df = df.set_index(df.columns[0])
            
        # st.table(df.style.hide(axis = "index"))
        
        # # st.markdown(df.style.hide(axis = "index").hide.to_html(), unsafe_allow_html = True)

        html_table = render_html_table(vertical_history, get_highlighted_cells(history))
        with col2:
            st.markdown(html_table, unsafe_allow_html = True)
        


