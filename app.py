import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

st.set_page_config(page_title="Real Estate AI Pro", layout="wide")

st.title("🏢 نظام إدارة العقارات الاحترافي")

# ====== Google Sheets Connection ======
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key("18c7cdOIjNcFkv2f8wUyV-V_K-AoKsbZbaRkVDlRQMuI").sheet1

# ====== Load Data ======
@st.cache_data(ttl=60)
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_data(df):
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

df = load_data()

menu = st.sidebar.radio("القائمة الرئيسية", [
    "لوحة التحكم",
    "إدارة العقارات"
])

# ====== Dashboard ======
if menu == "لوحة التحكم":

    total_properties = len(df)
    total_units = df["عدد الوحدات"].sum() if not df.empty else 0
    rented_units = df["الوحدات المؤجرة"].sum() if not df.empty else 0
    occupancy = (rented_units / total_units * 100) if total_units > 0 else 0
    revenue = (df["الوحدات المؤجرة"] * df["الإيجار الشهري"]).sum() if not df.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("إجمالي العقارات", total_properties)
    col2.metric("إجمالي الوحدات", total_units)
    col3.metric("نسبة الإشغال", f"{occupancy:.1f}%")
    col4.metric("الإيراد الشهري", f"{revenue:,.0f}")

    st.divider()

    if not df.empty:
        st.bar_chart(df.set_index("اسم العقار")["الإيجار الشهري"])

# ====== Property Management ======
if menu == "إدارة العقارات":

    st.subheader("إضافة عقار جديد")

    name = st.text_input("اسم العقار")
    units = st.number_input("عدد الوحدات", min_value=1, step=1)
    rented = st.number_input("الوحدات المؤجرة", min_value=0, step=1)
    rent = st.number_input("الإيجار الشهري للوحدة", min_value=0, step=100)

    if st.button("إضافة"):
        new_row = pd.DataFrame([{
            "اسم العقار": name,
            "عدد الوحدات": units,
            "الوحدات المؤجرة": rented,
            "الإيجار الشهري": rent
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("تمت إضافة العقار بنجاح")
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.subheader("قائمة العقارات")
    st.dataframe(df, use_container_width=True)
