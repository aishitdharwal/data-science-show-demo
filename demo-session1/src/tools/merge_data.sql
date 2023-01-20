SELECT
   sa.timestamp, sa.product_id, sa.quantity, te.temperature
FROM
   cleaned_groceries.stock_agg st 
LEFT JOIN
   cleaned_groceries.sales_agg sa 
   ON st.timestamp = sa.timestamp 
   AND st.product_id = sa.product_id 
LEFT JOIN
   cleaned_groceries.temp_agg te 
   ON st.timestamp = te.timestamp