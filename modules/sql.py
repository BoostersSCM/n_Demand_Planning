# ERP (boosters DB) 판매이력 쿼리
SQL_SALES_HISTORY_BOOSTERS = """
SELECT 
    DATE_FORMAT(f1.date, '%Y-%m') AS ym,
    f1.resource_code AS product_code,
    f1.resource_name AS product_name,
    CASE 
        WHEN f1.order_gubun LIKE '%amazon%' THEN 'AMZ'
        ELSE 'ETC'
    END AS channel,
    SUM(f1.quantity) AS qty
FROM (
    SELECT 
        DATE(DATE_FORMAT(asroi.kor_purchase_date, '%Y-%m-%d')) AS `date`,
        bi.resource_code,
        REPLACE(REPLACE(REPLACE(bi.resource_name, '(AMZ)', ''), '(AMJP)', ''), '(OY)', '') AS resource_name,
        bi.brand_name,
        CASE 
            WHEN asroi.seller_order_id LIKE '5%' THEN 'tiktok'
            WHEN asroi.seller_order_id LIKE '%shopify%' THEN 'shopify'
            WHEN asroi.seller_order_id LIKE '70%' AND asroi.sales_channel = 'amazon.ca' THEN 'canada_amazon'
            WHEN asroi.seller_order_id LIKE '70%' AND asroi.sales_channel = 'amazon.com.mx' THEN 'mexico_amazon'
            WHEN asroi.sales_channel = 'amazon.co.jp' THEN 'japan_amazon'
            WHEN asroi.sales_channel = 'amazon.com.br' THEN 'brazil_amazon'
            WHEN asroi.sales_channel = 'amazon.com.au' THEN 'australia_amazon'
            WHEN asroi.sales_channel = 'amazon.co.uk' THEN 'uk_amazon'
            WHEN asroi.sales_channel = 'amazon.de' THEN 'germany_amazon'
            WHEN asroi.sales_channel = 'amazon.fr' THEN 'france_amazon'
            WHEN asroi.sales_channel = 'amazon.it' THEN 'italy_amazon'
            WHEN asroi.sales_channel = 'amazon.es' THEN 'spain_amazon'
            WHEN asroi.sales_channel = 'amazon.nl' THEN 'netherlands_amazon'
            WHEN asroi.sales_channel = 'amazon.se' THEN 'sweden_amazon'
            WHEN asroi.sales_channel = 'amazon.pl' THEN 'poland_amazon'
            WHEN asroi.sales_channel = 'amazon.com.be' THEN 'belgium_amazon'
            WHEN asroi.sales_channel = 'amazon.in' THEN 'india_amazon'
            WHEN asroi.sales_channel = 'amazon.sg' THEN 'singapore_amazon'
            WHEN asroi.sales_channel = 'amazon.com.tr' THEN 'turkey_amazon'
            WHEN asroi.sales_channel = 'amazon.ae' THEN 'uae_amazon'
            WHEN asroi.sales_channel = 'amazon.sa' THEN 'saudi_amazon'
            WHEN asroi.sales_channel = 'amazon.eg' THEN 'egypt_amazon'
            WHEN asroi.seller_order_id LIKE '%seeding%' THEN 'seeding'
            WHEN asroi.sales_channel = 'non-amazon' THEN 'non_amazon'
            ELSE 'amazon' 
        END AS order_gubun,
        asrodi.quantity
    FROM amazon_seller_report_order_infos AS asroi
    LEFT JOIN amazon_seller_report_order_detail_infos AS asrodi 
        ON asrodi.amazon_seller_report_order_info_id = asroi.id
    LEFT JOIN boosters_items AS bi 
        ON bi.amazon_seller_asin = asrodi.asin
) AS f1
WHERE 
    f1.date >= '2025-01-01'
    AND f1.brand_name = '이퀄베리'
    AND f1.resource_code NOT LIKE 'BA1%%'
    AND f1.order_gubun <> 'non_amazon'
GROUP BY 
    DATE_FORMAT(f1.date, '%Y-%m'),
    f1.resource_code,
    f1.resource_name,
    channel;
"""

# SCM DB 판매이력 쿼리
SQL_SALES_HISTORY_SCM = """
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS ym,
    resource_code AS product_code,
    resource_name AS product_name,
    CASE
        WHEN channel_name LIKE '%쇼피%' THEN '쇼피'
        WHEN channel_name LIKE '%cafe24%' THEN NULL
        ELSE 'B2B'
    END AS channel,
    SUM(output) AS qty
FROM scm.SCM2_channel_output
WHERE 
    brand_name = '이퀄베리'
    AND resource_code NOT LIKE '%-%'
    AND resource_code NOT LIKE '%\\_%' ESCAPE '\\'
    AND channel_type NOT LIKE 'sample'
    AND channel_type NOT LIKE '%이동출고%'
    AND channel_name NOT LIKE '%cafe24%'
GROUP BY ym, product_code, product_name, channel;
"""
