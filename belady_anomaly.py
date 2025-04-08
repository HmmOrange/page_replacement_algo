import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from algo import *
from table import *

st.set_page_config(
    page_title = "Page Replacement Algorithms",
    page_icon = "📄",
    initial_sidebar_state = "expanded",
    menu_items = {
        'Get help': 'https://github.com/HmmOrange/page-replacement-algo',
        'About': "# Made with 💖\nhttps://github.com/HmmOrange/page-replacement-algo",
    }
)

st.title("Hiện tượng bất thường Bélády")

pages_input = st.sidebar.text_input("Chuỗi số hiệu", "3, 2, 1, 0, 3, 2, 4, 3, 2, 1, 0, 4")
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

if len(checkbox_options):
    frame_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in checkbox_options:
        page_fault_count = []
        for frame_size in range(1, 11):
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

            page_fault_count.append(page_faults)

        st.subheader(i)

        fig, ax = plt.subplots()
        ax.plot(frame_sizes, page_fault_count, marker = 'o', color = 'deepskyblue', linewidth = 2)

        # Highlight anomaly if you want
        for i in range(len(page_fault_count) - 1):
            if page_fault_count[i] < page_fault_count[i + 1]:
                ax.plot([i + 1, i + 2], [page_fault_count[i], page_fault_count[i + 1]], marker = 'o', color= '#FF8080', linewidth = 2)

        ax.set_xlabel("Number of Frames")
        ax.set_ylabel("Number of Page Faults")
        ax.grid(True)
        ax.set_xticks(frame_sizes)
        ax.set_yticks(range(min(page_fault_count), max(page_fault_count) + 1, 1))

        # Show in Streamlit
        st.pyplot(fig)
        
