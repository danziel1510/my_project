import json
import os
import datetime
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


class AttendanceStorage:
    def __init__(self):
        self.use_sheets = self._has_sheet_config()
        self.sheet = None
        self.local_filename = f"data {datetime.datetime.now().strftime('%Y-%m-%d')}.json"
        if self.use_sheets:
            self._init_google_sheet()

    def _has_sheet_config(self):
        return "gcp_service_account" in st.secrets and "spreadsheet_id" in st.secrets

    def _init_google_sheet(self):
        if gspread is None or Credentials is None:
            st.error("Google Sheets storage requires `gspread` and `google-auth`. Update requirements.txt and redeploy.")
            self.use_sheets = False
            return

        service_account_info = st.secrets["gcp_service_account"]
        if isinstance(service_account_info, str):
            service_account_info = json.loads(service_account_info)

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_key(st.secrets["spreadsheet_id"]).sheet1
        self._ensure_header()

    def _ensure_header(self):
        if not self.sheet:
            return
        header = self.sheet.row_values(1)
        if header != ["first_name", "last_name", "matric_number", "timestamp"]:
            try:
                self.sheet.insert_row(["first_name", "last_name", "matric_number", "timestamp"], index=1)
            except Exception:
                pass

    def load_attendance(self):
        if self.use_sheets and self.sheet:
            return self.sheet.get_all_records()

        if os.path.exists(self.local_filename) and os.path.getsize(self.local_filename) > 0:
            with open(self.local_filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_attendance(self, record):
        record["timestamp"] = datetime.datetime.utcnow().isoformat()
        if self.use_sheets and self.sheet:
            self.sheet.append_row(
                [record["first_name"], record["last_name"], record["matric_number"], record["timestamp"]],
                value_input_option="RAW",
            )
            return

        data = self.load_attendance()
        data.append(record)
        with open(self.local_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def has_duplicate(self, record):
        attendance = self.load_attendance()
        return any(
            item.get("first_name") == record["first_name"]
            and item.get("last_name") == record["last_name"]
            and item.get("matric_number") == record["matric_number"]
            for item in attendance
        )
