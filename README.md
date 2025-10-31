# EqqualBerry Demand Dashboard (DB-first, Rebuilt)

This is a rebuilt, DB-first version intended for Streamlit Cloud.

## Structure
```
app/
  main_app.py
  modules/
    db_connector.py
    data_manager.py
    future_forecast.py
    kpi_analysis.py
    trend_analysis.py
    utils.py
  requirements.txt
```

## Secrets
Create `.streamlit/secrets.toml` with:
```
db_user="YOUR_USER"
db_password="YOUR_PASSWORD"
db_host="YOUR_HOST"
db_port="3306"
db_name="boosters"
```

## Run
```
streamlit run main_app.py
```
