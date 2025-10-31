import streamlit as st
import pandas as pd
from .db_connector import read_sql_df, init_connection
from .sqls import SQL_SALES_HISTORY_BOOSTERS, SQL_SALES_HISTORY_SCM

@st.cache_data(show_spinner=False)
def load_sales_history_combined() -> pd.DataFrame:
    """boosters + scm 판매이력 병합"""
    engine_boosters = init_connection()  # ERP
    df_boosters = read_sql_df(SQL_SALES_HISTORY_BOOSTERS)

    # SCM DB 연결
    user = st.secrets["db_user_scm"]
    pwd  = st.secrets["db_password_scm"]
    host = st.secrets["db_server_scm"]
    port = st.secrets["db_port_scm"]
    name = st.secrets["db_name_scm"]
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset=utf8mb4"
    scm_engine = create_engine(url, pool_pre_ping=True)
    df_scm = pd.read_sql(SQL_SALES_HISTORY_SCM, scm_engine)

    # 형식 동일 → 병합
    df = pd.concat([df_boosters, df_scm], ignore_index=True)
    df = df.dropna(subset=["ym", "product_code"]).copy()
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)
    return df
