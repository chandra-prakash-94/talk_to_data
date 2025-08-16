import streamlit as st
import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
import tempfile
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")

# Configure your LLM
llm = LiteLLM(model="gemini/gemini-2.5-pro", api_key= api_key)

# Set PandasAI config
pai.config.set({"llm": llm, "save_charts": False, "verbose": False})
st.set_page_config(page_title="Talk to Your Data", layout="wide")
st.title("📊 Talk to Your Data")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    if uploaded_file.name.endswith(".csv"):
        df = pai.read_csv(tmp_path)
    else:
        df = pai.read_excel(tmp_path)
    st.success(f"✅ File `{uploaded_file.name}` uploaded successfully!")

    with st.expander("Preview Data"):
        st.dataframe(df)

    query = st.text_input("Ask a question about your data:")
    if query:
        result = df.chat(query)
        # If a chart is generated
        if plt.get_fignums():
            fig = plt.gcf()
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.write(result)

    os.remove(tmp_path)
