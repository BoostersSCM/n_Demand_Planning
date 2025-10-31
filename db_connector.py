import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

@st.cache_resource(show_spinner=False)
def init_connection():
    """Create a SQLAlchemy engine using Streamlit secrets."""
    user = st.secrets['db_user']
    pwd = st.secrets['db_password']
    host = st.secrets['db_host']
    port = st.secrets.get('db_port', '3306')
    name = st.secrets['db_name']
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)

def run_query(sql: str, params=None) -> pd.DataFrame:
    engine = init_connection()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})
