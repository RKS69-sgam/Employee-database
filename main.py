import streamlit as st
import gspread
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# === Google Sheets Credentials from Secrets (encoded JSON)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# base64 में credentials.json को Streamlit secrets में रखें
encoded = st.secrets["google_service"]["base64_credentials"]
decoded = base64.b64decode(encoded)
credentials_dict = json.loads(decoded)

# Authorize gspread
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

# === Google Sheet Open
sheet_id = "YOUR_SHEET_ID_HERE"  # Google Sheet ka ID
sheet = client.open_by_key(sheet_id)
worksheet = sheet.sheet1  # या specific worksheet नाम: sheet.worksheet("Sheet1")

# === Data पढ़ें और दिखाएँ
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)
