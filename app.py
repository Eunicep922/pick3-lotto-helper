
import streamlit as st
import pandas as pd
from itertools import combinations
import numpy as np

# --- Helper Functions ---
def get_surrounding_values(i, j, df):
    rows, cols = df.shape
    surrounding = []
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j):
                surrounding.append(df.iloc[x, y])
    return surrounding

def get_pick3_combinations(df, key):
    positions = [(i, j) for i in range(df.shape[0]) for j in range(df.shape[1]) if df.iloc[i, j] == key]
    if not positions:
        return [], []

    i, j = positions[0]  # use first occurrence only
    surrounding_vals = get_surrounding_values(i, j, df)
    
    with_key = [(key,) + combo for combo in combinations(surrounding_vals, 2)]
    without_key = list(combinations(surrounding_vals, 3))
    
    return with_key, without_key

# --- Streamlit UI ---
st.set_page_config(page_title="Pick 3 Generator", layout="centered")
st.title("🔢 Pick 3 Combination Generator")

uploaded_file = st.file_uploader("Upload your number grid (Excel or CSV)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file, header=None)
    else:
        df = pd.read_excel(uploaded_file, header=None)

    st.write("### Grid Preview")
    st.dataframe(df)

    key_number = st.number_input("Enter a key number (e.g., 7, 2, 5, 0):", min_value=0, max_value=99, step=1)

    if st.button("Generate Pick 3 Combinations"):
        with_key, without_key = get_pick3_combinations(df, key_number)

        st.subheader(f"✅ Pick 3 combinations WITH key {key_number}:")
        st.write(pd.DataFrame(with_key, columns=["Val1", "Val2", "Val3"]))

        st.subheader(f"❌ Pick 3 combinations WITHOUT key {key_number}:")
        st.write(pd.DataFrame(without_key, columns=["Val1", "Val2", "Val3"]))

        with pd.ExcelWriter("pick3_results.xlsx") as writer:
            pd.DataFrame(with_key).to_excel(writer, sheet_name="With_Key", index=False)
            pd.DataFrame(without_key).to_excel(writer, sheet_name="Without_Key", index=False)

        with open("pick3_results.xlsx", "rb") as f:
            st.download_button("📥 Download Results as Excel", f, file_name="pick3_results.xlsx")
