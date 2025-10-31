import streamlit as st
import pandas as pd
from modules.data_access import load_sales_history_combined, load_product_prices, load_current_inventory
from modules.mix_model import compute_channel_item_mix
from modules.plan_engine import revenue_to_required_qty, summarize_shortage

st.set_page_config(page_title="매출 기반 재고 계획", page_icon="📊", layout="wide")
st.title("📦 예상 매출 → 필요 재고량 → 부족량 계산")

with st.spinner("DB에서 판매데이터 불러오는 중..."):
    sales = load_sales_history_combined()
    prices = load_product_prices()
    stock = load_current_inventory()

channels = sorted(sales["channel"].dropna().unique())
st.write(f"📈 {len(channels)}개 채널 데이터 로드 완료")

st.subheader("① 예상 매출 입력")
input_df = pd.DataFrame({"channel": channels, "expected_revenue": [0]*len(channels)})
expected = st.data_editor(input_df, num_rows="dynamic", use_container_width=True)

if st.button("필요 재고량 계산"):
    mix = compute_channel_item_mix(sales, expected["channel"].tolist())
    req = revenue_to_required_qty(expected, mix, prices)
    shortage = summarize_shortage(req, stock)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 품목별 부족량")
        st.dataframe(shortage, use_container_width=True)
        st.download_button("📥 부족량 다운로드", shortage.to_csv(index=False).encode("utf-8-sig"), "shortage.csv")

    with col2:
        st.markdown("### 🔍 채널별 필요 수량")
        st.dataframe(req, use_container_width=True)
        st.download_button("📥 필요수량 다운로드", req.to_csv(index=False).encode("utf-8-sig"), "required_qty.csv")
else:
    st.info("예상 매출액 입력 후 [필요 재고량 계산] 버튼을 눌러주세요.")
