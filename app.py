import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Real Estate AI Pro", layout="wide")

# ====== Dark Theme ======
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1C1F26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 نظام إدارة العقارات الاحترافي")

# ====== Data ======
if "properties" not in st.session_state:
    st.session_state.properties = pd.DataFrame(columns=[
        "اسم العقار",
        "عدد الوحدات",
        "الوحدات المؤجرة",
        "الإيجار الشهري"
    ])

menu = st.sidebar.radio("القائمة الرئيسية", [
    "لوحة التحكم",
    "إدارة العقارات"
])

# ====== Dashboard ======
if menu == "لوحة التحكم":

    df = st.session_state.properties

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
        st.session_state.properties = pd.concat([st.session_state.properties, new_row], ignore_index=True)
        st.success("تمت إضافة العقار بنجاح")

    st.divider()
    st.subheader("قائمة العقارات")
    st.dataframe(st.session_state.properties, use_container_width=True)
