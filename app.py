import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Sales Dashboard", layout="wide")

st.title("📊 Smart Dynamic Sales Dashboard")
st.write("Adaptive dashboard based on uploaded data ✅")

# -------------------------------
# Helper: Find matching column
# -------------------------------
def find_column(df, possible_names):
    for col in df.columns:
        for name in possible_names:
            if name.lower() in col.lower():
                return col
    return None

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx'])

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("File uploaded successfully ✅")

    st.write("### 🔍 Detected Columns:")
    st.write(df.columns.tolist())

    # -------------------------------
    # Detect columns dynamically
    # -------------------------------
    date_col = find_column(df, ['date'])
    product_col = find_column(df, ['product', 'item'])
    customer_col = find_column(df, ['customer', 'party', 'company'])
    qty_col = find_column(df, ['qty', 'quantity'])
    value_col = find_column(df, ['amount', 'value', 'sales'])

    # Convert safely
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['Month'] = df[date_col].dt.strftime('%Y-%m')

    if qty_col:
        df[qty_col] = pd.to_numeric(df[qty_col], errors='coerce')

    if value_col:
        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')

    # -------------------------------
    # KPIs
    # -------------------------------
    st.markdown("## 📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    if value_col:
        col1.metric("Total Sales", f"₹{df[value_col].sum():,.0f}")
    if qty_col:
        col2.metric("Total Quantity", f"{df[qty_col].sum():,.0f}")
    if customer_col:
        col3.metric("Customers", df[customer_col].nunique())

    st.markdown("---")

    # -------------------------------
    # Dynamic Charts
    # -------------------------------

    # Top Products
    if product_col and value_col:
        st.subheader("📦 Top Products")
        top_products = df.groupby(product_col)[value_col].sum().sort_values(ascending=False).head(10)

        fig = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            title="Top Products"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top Customers
    if customer_col and value_col:
        st.subheader("👥 Top Customers")
        top_customers = df.groupby(customer_col)[value_col].sum().sort_values(ascending=False).head(10)

        fig2 = px.bar(
            x=top_customers.values,
            y=top_customers.index,
            orientation='h',
            title="Top Customers"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly Trend
    if date_col and value_col:
        st.subheader("📈 Monthly Trend")
        monthly = df.groupby('Month')[value_col].sum().reset_index()

        fig3 = px.line(monthly, x='Month', y=value_col, markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------
    # Download Section
    # -------------------------------
    st.markdown("---")
    st.subheader("⬇️ Download Data")

    st.download_button(
        "Download Full Data (CSV)",
        df.to_csv(index=False),
        file_name="full_data.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download Summary (CSV)",
        df.describe().to_csv(),
        file_name="summary.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a file to generate dashboard")