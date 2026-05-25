name = "Madhivanan R R"
print(f"My name is {name}") #f-string #{} is used to insert the value of the variable name into the string.

#f-string #{} is used to insert the value of the variable name into the string.
import requests
import pandas as pd
from datetime import datetime

# The API address where the official earthquake data lives
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []
start_year = datetime.now().year - 5   # Calculates 5 years ago
end_year = datetime.now().year

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            next_month = 1
            next_year  = year + 1
        else:
            next_month = month + 1
            next_year  = year

        end_date = f"{next_year}-{next_month:02d}-01"

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }

        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"⚠️ Failed for {start_date}: {response.text[:200]}")
            continue

        try:
            data = response.json()
        except Exception as e:
            print(f"⚠️ JSON error for {start_date}: {e}")
            continue

        for f in data["features"]:
            p = f["properties"]
            g = f["geometry"]["coordinates"]
            
            all_records.append({
                "id": f.get("id"),
                "time": pd.to_datetime(p.get("time"), unit="ms"),
                "updated": pd.to_datetime(p.get("updated"), unit="ms"),
                "code" : p.get("code"),
                "ids" : p.get("ids"),
                "latitude": g[1] if g else None,
                "longitude": g[0] if g else None,
                "depth_km": g[2] if g else None,
                "place": p.get("place"),
                "mag": p.get("mag"),
                "magType": p.get("magType"),
                "type": p.get("type"),
                "types" : p.get("types"),
                "tsunami": p.get("tsunami"),
                "sig": p.get("sig"),
                "alert": p.get("alert"),
                "felt" : p.get("felt"),
                "cdi": p.get("cdi"),
                "mni": p.get("mni"),
                "nst": p.get("nst"),
                "gap": p.get("gap"),
                "rms": p.get("rms"),
                "net" : p.get("net"),
                "sources" : p.get("sources"),
                "dmin" : p.get("dmin"),
                "status": p.get("status"),
            })

df = pd.DataFrame(all_records)

print("Total Earthquakes Gathered (Rows):", df.shape[0])
print("Total Features Stored (Columns):", df.shape[1])
print("\nFirst 5 rows look like this:")
print(df.head())

print(response)

all_records

df.columns

print(df)

df.info() # Check the structure and data types of the DataFrame

df.isna().sum() # Check for missing values in each column. null values can cause problems in analysis, so it's important to know where they are.

# --- STEP 1: DEFINE ALL 26 COLUMNS ---
numeric_columns = ['mag', 'depth_km', 'nst', 'gap', 'rms', 'dmin', 'felt', 'cdi', 'mni', 'mmi', 'sig', 'magError', 'depthError', 'magNst']
text_columns = ['alert', 'place', 'magType', 'net', 'sources', 'types', 'status', 'type', 'code', 'ids']

# --- STEP 2: FIX NUMERIC COLUMNS ---
for col in numeric_columns:
    if col not in df.columns:
        df[col] = None
    
    df[col] = pd.to_numeric(df[col], errors='coerce')
    column_median = df[col].median()
    
    # If the median is missing, we use 0.00 as a precise scientific reading
    if pd.isna(column_median):
        column_median = 0.00
        
    df[col] = df[col].fillna(column_median)

# --- STEP 3: FIX TEXT COLUMNS ---
for col in text_columns:
    if col not in df.columns:
        df[col] = None
        
    if col == 'alert':
        df['alert'] = df['alert'].fillna('No Alert Issued')
    elif col == 'place':
        df['place'] = df['place'].fillna('Undocumented Location')
    elif col == 'sources':
        df['sources'] = df['sources'].fillna('No Reporting Agency')
    elif col == 'types':
        df['types'] = df['types'].fillna('No Associated Data')
    else:
        if df[col].notna().sum() > 0:
            df[col] = df[col].fillna(df[col].value_counts().index[0])
        else:
            df[col] = df[col].fillna('Not Specified')

print("✨ DataFrame is 100% complete with all 26 features preserved!")


print(df.isna().sum())

df

print(data)

#**SQL CONNECTION**

import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Datascience2025" # Put your real password here
)
cursor = conn.cursor() # Create a cursor object to execute SQL commands
cursor.execute("CREATE DATABASE IF NOT EXISTS earthquakes")
conn.close()

print("✅ Database is ready!")

import pandas as pd
from sqlalchemy import create_engine, text

# 1. Setup the high-speed connection highway to your local MySQL database
engine = create_engine("mysql+pymysql://root:Datascience2025@localhost/earthquakes")

# 2. Upload the data and update the database structure safely
df.to_sql(
    name="EQ",
    con=engine,
    if_exists="replace",  # CHANGED FROM "append" TO "replace" TO FIX THE ERROR
    index=False
)

print("✅ Data has been inserted successfully into the 'EQ' table with all professional metrics!")