import streamlit as st
import pandas as pd
from .db_connector import run_query

@st.cache_data(show_spinner=False)
def load_products() -> pd.DataFrame:
    """Load active products from boosters_items. Column aliases are standardized."""
    sql = '''
    SELECT
        itemno            AS 제품코드,
        itemname          AS 제품명,
        COALESCE(barcode, '') AS 바코드,
        COALESCE(price, 0)    AS 판매가,
        COALESCE(route, '')   AS 경로 -- optional; if absent, leave ''
    FROM boosters_items
    WHERE COALESCE(is_active, 1) = 1
    '''
    df = run_query(sql)
    # Ensure numeric price
    df['판매가'] = pd.to_numeric(df['판매가'], errors='coerce').fillna(0.0)
    return df

@st.cache_data(show_spinner=False)
def load_kpi() -> pd.DataFrame:
    """Load KPI targets from monthly_kpi. Expecting YYYY-MM in 'month'."""
    sql = '''
    SELECT
        DATE_FORMAT(month, '%Y-%m') AS 월,
        route                        AS 경로,
        kpi_sales                    AS KPI매출
    FROM monthly_kpi
    '''
    df = run_query(sql)
    df['KPI매출'] = pd.to_numeric(df['KPI매출'], errors='coerce').fillna(0.0)
    return df

@st.cache_data(show_spinner=False)
def load_sales_history(months_back: int = 6) -> pd.DataFrame:
    """
    Load sales history.

    Preferred: a materialized view named `sales_history` with columns:
      month(YYYY-MM), route, product_code, product_name, quantity

    Fallback: attempt to derive from global_b2b_invoices + _details if available.
    If details table is not present, returns empty DF (the prediction will fall back to equal ratios).
    """
    # 1) Try unified sales_history view first
    sql_view = '''
    SELECT
        DATE_FORMAT(month, '%Y-%m') AS 월,
        route                       AS 경로,
        product_code                AS 제품코드,
        product_name                AS 제품명,
        quantity                    AS 판매수량
    FROM sales_history
    WHERE month >= DATE_SUB(CURDATE(), INTERVAL %(months_back)s MONTH)
    '''
    try:
        df = run_query(sql_view, params={'months_back': months_back})
        if len(df) > 0:
            return df
    except Exception:
        pass

    # 2) Try to build from global_b2b_invoices + global_b2b_invoice_details
    #    Note: if details table doesn't exist, this block may fail.
    sql_fallback = '''
    SELECT
        DATE_FORMAT(a.order_date, '%Y-%m')                   AS 월,
        a.shop_name                                          AS 경로,
        b.resource_code                                      AS 제품코드,
        b.resource_name                                      AS 제품명,
        CAST(b.quantity AS SIGNED)                           AS 판매수량
    FROM global_b2b_invoices a
    INNER JOIN global_b2b_invoice_details b
        ON a.id = b.global_b2b_invoice_id
    WHERE a.is_delete = 0
      AND b.is_delete = 0
      AND a.order_date >= DATE_SUB(CURDATE(), INTERVAL %(months_back)s MONTH)
    '''
    try:
        df = run_query(sql_fallback, params={'months_back': months_back})
        return df
    except Exception:
        # Return empty; downstream will handle graceful fallbacks
        return pd.DataFrame(columns=['월','경로','제품코드','제품명','판매수량'])
