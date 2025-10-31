import streamlit as st
import pandas as pd
from .db_connector import read_sql_df
from .sqls import SQL_SALES_HISTORY_BOOSTERS, SQL_SALES_HISTORY_SCM

@st.cache_data(show_spinner=False)
def load_sales_history_combined() -> pd.DataFrame:
    """
    boosters(ERP) + scm(SCM) DB의 판매이력 데이터를 가져와 병합
    """
    # boosters DB
    df_boosters = read_sql_df(SQL_SALES_HISTORY_BOOSTERS, db_type="erp")

    # scm DB
    df_scm = read_sql_df(SQL_SALES_HISTORY_SCM, db_type="scm")

    # 병합 후 클린업
    df = pd.concat([df_boosters, df_scm], ignore_index=True)
    df = df.dropna(subset=["ym", "product_code"]).copy()
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)

    return df
