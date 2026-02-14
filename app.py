import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Executive Dashboard")

# ==========================
# روابط CSV
# ==========================
properties_url = "https://docs.google.com/spreadsheets/d/118TQGBJDgeoPQpDJAPEbl9HkmfandXFu/export?format=csv&gid=1036124252"
units_url = "https://docs.google.com/spreadsheets/d/118TQGBJDgeoPQpDJAPEbl9HkmfandXFu/export?format=csv&gid=1895018394"
payments_url = "https://docs.google.com/spreadsheets/d/118TQGBJDgeoPQpDJAPEbl9HkmfandXFu/export?format=csv&gid=1506718084"
maintenance_url = "https://docs.google.com/spreadsheets/d/118TQGBJDgeoPQpDJAPEbl9HkmfandXFu/export?format=csv&gid=2041686772"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

properties = load_data(properties_url)
units = load_data(units_url)
payments = load_data(payments_url)
maintenance = load_data(maintenance_url)

st.title("🏢 Executive Real Estate Dashboard")

# ==========================
# فلتر الشهر
# ==========================
selected_month = st.selectbox("اختر الشهر", payments["الشهر"].unique())

payments_filtered = payments[payments["الشهر"] == selected_month]
maintenance_filtered = maintenance[maintenance["الشهر"] == selected_month]

# ==========================
# KPIs
# ==========================
total_income = payments_filtered["الدخل"].sum()
total_maintenance = maintenance_filtered["التكلفة"].sum()
net_profit = total_income - total_maintenance
occupied_units = len(units[units["الحالة"] == "مؤجرة"])
total_units = len(units)
occupancy_rate = (occupied_units / total_units) * 100 if total_units > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("إجمالي الدخل", f"{total_income:,.0f}")
col2.metric("إجمالي الصيانة", f"{total_maintenance:,.0f}")
col3.metric("صافي الربح", f"{net_profit:,.0f}")
col4.metric("نسبة الإشغال", f"{occupancy_rate:.1f}%")

st.divider()

# ==========================
# الرسوم البيانية
# ==========================

# 1 خطي للدخل
fig1 = px.line(payments, x="الشهر", y="الدخل", title="اتجاه الدخل")
st.plotly_chart(fig1, use_container_width=True)

# 2 مقارنة دخل وصيانة
merged_income = payments.groupby("الشهر")["الدخل"].sum().reset_index()
merged_maint = maintenance.groupby("الشهر")["التكلفة"].sum().reset_index()

compare = pd.merge(merged_income, merged_maint, on="الشهر")

fig2 = px.bar(compare, x="الشهر", y=["الدخل", "التكلفة"],
              barmode="group",
              title="دخل مقابل صيانة")

st.plotly_chart(fig2, use_container_width=True)

# 3 Pie توزيع الوحدات
fig3 = px.pie(units, names="الحالة", title="توزيع الوحدات")
st.plotly_chart(fig3, use_container_width=True)

# 4 أداء العقارات
property_income = payments.groupby("رقم_العقار")["الدخل"].sum().reset_index()

fig4 = px.bar(property_income,
              x="رقم_العقار",
              y="الدخل",
              title="أداء كل عقار")

st.plotly_chart(fig4, use_container_width=True)
