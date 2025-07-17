import streamlit as st
import pandas as pd
import gspread
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials

# === Google Auth ===
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
encoded = st.secrets["google_service"]["base64_credentials"]
decoded = base64.b64decode(encoded)
credentials_dict = json.loads(decoded)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

# === Google Sheet Setup ===
sheet_id = "1UUoTgK7HUGzPwoUZ8ex8hhmmbVD_mNPtpsfiyXgmOsA"
sheet = client.open_by_key(sheet_id)
worksheet = sheet.sheet1

# === Load Data ===
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("Employee Master Database")

menu = st.sidebar.radio("Select Action", ["Search", "Add New", "Edit/Update"])

# === SEARCH ===
if menu == "Search":
    search_name = st.text_input("Enter employee name or PF No. to search")
    if search_name:
        result = df[df.apply(lambda row: search_name.lower() in str(row).lower(), axis=1)]
        if not result.empty:
            st.success("Match Found:")
            st.dataframe(result)
        else:
            st.warning("No match found.")

# === ADD NEW ===
elif menu == "Add New":
    st.subheader("Add New Employee")

    new_data = {}
    columns = df.columns.tolist()
    for col in columns:
        new_data[col] = st.text_input(f"{col}")

    if st.button("Add Employee"):
        # Convert to row format
        new_row = [new_data[col] for col in columns]
        worksheet.append_row(new_row)
        st.success("Employee added successfully!")

# === EDIT / UPDATE ===
elif menu == "Edit/Update":
    st.subheader("Edit Existing Employee")

    pf_no = st.text_input("Enter PF No. of employee to edit:")
    if pf_no:
        match = df[df['PF No.'] == pf_no]
        if not match.empty:
            index = match.index[0]
            updated_data = {}
            for col in df.columns:
                updated_data[col] = st.text_input(f"{col}", value=str(df.at[index, col]))

            if st.button("Update Record"):
                for i, col in enumerate(df.columns):
                    worksheet.update_cell(index + 2, i + 1, updated_data[col])  # +2 because 1 for header, 1 for 0-index
                st.success("Record updated successfully!")
        else:
            st.error("PF No. not found in records.")