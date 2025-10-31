import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

@st.cache_resource(show_spinner=False)
def init_connection():
    """
    ✅ ERP DB(MySQL) 연결용
    Streamlit secrets.toml의 ERP 섹션 사용
    """
    user = st.secrets["db_user_erp"]
    pwd = st.secrets["db_password_erp"]
    host = st.secrets["db_server_erp"]
    port = st.secrets["db_port_erp"]
    name = st.secrets["db_name_erp"]

    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)

def run_query(sql: str, params=None) -> pd.DataFrame:
    """
    SELECT 쿼리 실행 전용 (ERP DB)
    """
    engine = init_connection()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})
