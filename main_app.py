import streamlit as st
import pandas as pd
from modules.data_access import load_sales_history_combined

st.set_page_config(page_title="Sales History Combined", layout="wide")
st.title("📦 판매이력 통합 조회")

with st.spinner("DB에서 판매 데이터 로드 중..."):
    df_sales = load_sales_history_combined()

st.success(f"총 {len(df_sales):,}건의 데이터 로드 완료")

st.dataframe(df_sales, use_container_width=True)
