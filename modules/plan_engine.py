import pandas as pd
import numpy as np

def revenue_to_required_qty(expected_df, mix_df, price_df):
    """예상 매출액 → 필요수량 계산"""
    df = mix_df.merge(price_df, on="product_code", how="left")
    df = df.merge(expected_df, on="channel", how="left")
    df["required_qty"] = np.where(
        df["unit_price"] > 0,
        (df["expected_revenue"] * df["mix_ratio"]) / df["unit_price"],
        0
    )
    df["required_qty"] = np.ceil(df["required_qty"]).astype(int)
    return df[["channel", "product_code", "required_qty"]]

def summarize_shortage(required_df, inventory_df):
    """필요수량 vs 현재고 비교 → 부족량"""
    result = required_df.groupby("product_code", as_index=False)["required_qty"].sum()
    result = result.merge(inventory_df, on="product_code", how="left").fillna(0)
    result["shortage"] = (result["required_qty"] - result["stock_qty"]).clip(lower=0)
    return result
