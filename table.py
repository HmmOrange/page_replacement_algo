import streamlit as st

def render_html_table(data, red_cells):
    if red_cells is None:
        red_cells = set()

    html = """
    <style>
        table {
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }
        thead tr {
            background-color: deepskyblue;
            font-weight: bold;
            border-bottom: 3px solid black;
        }
        .red-cell {
            background-color: #FF8080;
        }
    </style>
    <table>
        <thead>
            <tr>
    """

    # First row as headers
    for cell in data[0]:
        html += f"<th>{cell}</th>"
    html += "</tr></thead><tbody>"

    # Data rows
    for row_idx, row in enumerate(data[1:], start=1):
        html += "<tr>"
        for col_idx, cell in enumerate(row):
            # Check if this cell is in the red_cells set (by position)
            cell_style = ' class="red-cell"' if (row_idx, col_idx) in red_cells else ''
            html += f"<td{cell_style}>{cell}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html

def get_highlighted_cells(history):
    print(history)
    prev_col = [None] * (len(history) - 1)
    red_cells = []
    for i in range(len(history)):
        for j in range(len(history[i])):
            if history[i][j] != prev_col[j]:
                red_cells.append((j + 1, i))
                break
        prev_col = history[i]
    return red_cells
                
