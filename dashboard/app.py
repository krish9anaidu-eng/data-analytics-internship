
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Spend Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    path = (
        Path(__file__).resolve().parents[1]
        / "data/cleaned/cleaned_spend.csv"
    )

    df = pd.read_csv(path)
    df["action_date"] = pd.to_datetime(df["action_date"])

    df["recipient_name"] = (
        df["recipient_name"].fillna("Unknown")
    )

    df["product_or_service_code"] = (
        df["product_or_service_code"]
        .fillna("Unknown").astype(str)
    )

    df["month"] = df["action_date"].dt.strftime("%Y-%m")

    return df

df = load_data()

amount = "federal_action_obligation"

# Dashboard title
st.title("📊 Procurement Spend Analytics Dashboard")

st.caption("Data Analytics Internship | Project 1")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

dates = st.sidebar.date_input(
    "Date Range",
    value=(
        df["action_date"].min().date(),
        df["action_date"].max().date()
    )
)

suppliers = st.sidebar.multiselect(
    "Select Suppliers",
    sorted(df["recipient_name"].unique())
)

categories = st.sidebar.multiselect(
    "Select Categories",
    sorted(df["product_or_service_code"].unique())
)

# Apply filters
filtered = df.copy()

if len(dates) == 2:
    filtered = filtered[
        (filtered["action_date"].dt.date >= dates[0]) &
        (filtered["action_date"].dt.date <= dates[1])
    ]

if suppliers:
    filtered = filtered[
        filtered["recipient_name"].isin(suppliers)
    ]

if categories:
    filtered = filtered[
        filtered["product_or_service_code"].isin(categories)
    ]

if filtered.empty:
    st.warning("No records match your filters.")
    st.stop()

# Calculate KPIs
total_spend = filtered[amount].sum()

total_suppliers = filtered.loc[
    filtered["recipient_name"] != "Unknown",
    "recipient_name"
].nunique()

total_transactions = len(filtered)

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Net Obligations", f"${total_spend:,.2f}")
col2.metric("Total Suppliers", f"{total_suppliers:,}")
col3.metric("Total Transactions", f"{total_transactions:,}")

st.divider()

# Monthly spending
monthly = filtered.groupby(
    "month", as_index=False
)[amount].sum()

fig1 = px.line(
    monthly,
    x="month",
    y=amount,
    markers=True,
    title="Monthly Spending Trend",
    labels={amount: "Amount ($)", "month": "Month"}
)

st.plotly_chart(fig1, use_container_width=True)

# Top 10 suppliers
top_suppliers = filtered[
    filtered["recipient_name"] != "Unknown"
].groupby(
    "recipient_name", as_index=False
)[amount].sum().nlargest(10, amount)

fig2 = px.bar(
    top_suppliers,
    x=amount,
    y="recipient_name",
    orientation="h",
    title="Top 10 Suppliers",
    labels={amount: "Amount ($)", "recipient_name": "Supplier"}
)

fig2.update_yaxes(categoryorder="total ascending")

# Category spending
category_spend = filtered.groupby(
    "product_or_service_code",
    as_index=False
)[amount].sum().nlargest(10, amount)

fig3 = px.bar(
    category_spend,
    x="product_or_service_code",
    y=amount,
    title="Top 10 Spending Categories",
    labels={
        amount: "Amount ($)",
        "product_or_service_code": "Category"
    }
)

left, right = st.columns(2)

left.plotly_chart(fig2, use_container_width=True)
right.plotly_chart(fig3, use_container_width=True)

# Pareto analysis
st.subheader("Supplier Concentration")

if total_spend > 0:
    pareto = top_suppliers[amount].sum() / total_spend * 100

    st.metric(
        "Top 10 Suppliers Share",
        f"{pareto:.2f}%"
    )
else:
    st.info("Share unavailable for non-positive net spend.")

# Business insights
st.subheader("Key Business Insights")

highest_month = monthly.loc[monthly[amount].idxmax()]

st.write(
    f"Highest spending month: {highest_month['month']}"
)

if not top_suppliers.empty:
    st.write(
        f"Top supplier: {top_suppliers.iloc[0]['recipient_name']}"
    )

# Transaction table
st.subheader("Transaction Details")

st.dataframe(filtered.head(1000))

# Download data
st.download_button(
    label="Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name="filtered_spend.csv",
    mime="text/csv"
)

st.divider()
st.caption("Project 1 | Data Analytics Internship")
