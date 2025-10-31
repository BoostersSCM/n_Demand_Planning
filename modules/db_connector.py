import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

@st.cache_resource(show_spinner=False)
def init_connection(db_type="erp"):
    """
    ERP(DB: boosters) 또는 SCM(DB: scm)에 연결하는 SQLAlchemy 엔진 생성
    db_type: "erp" (기본) | "scm"
    """
    if db_type == "erp":
        user = st.secrets["db_user_erp"]
        pwd  = st.secrets["db_password_erp"]
        host = st.secrets["db_server_erp"]
        port = st.secrets["db_port_erp"]
        name = st.secrets["db_name_erp"]
    else:
        user = st.secrets["db_user_scm"]
        pwd  = st.secrets["db_password_scm"]
        host = st.secrets["db_server_scm"]
        port = st.secrets["db_port_scm"]
        name = st.secrets["db_name_scm"]

    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)

def read_sql_df(sql: str, db_type="erp") -> pd.DataFrame:
    """지정된 DB에서 SQL 실행 후 DataFrame 반환"""
    engine = init_connection(db_type)
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)
