import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tally Sales Dashboard")
st.write("App started successfully ✅")

# Load data safely
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Required columns check
        required_cols = ['Date', 'Product Name', 'Company Name (Customer)', 'Quantity Sold', 'Sales Value']
        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            st.error(f"Missing columns: {missing}")
            st.stop()

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.strftime('%Y-%m')

        df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
        df['Sales Value'] = pd.to_numeric(df['Sales Value'], errors='coerce')

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

# Upload file
uploaded_file = st.file_uploader("Upload Excel/CSV", type=['xlsx', 'csv'])

if uploaded_file:
    df = load_data(uploaded_file)

    st.success("Data loaded successfully ✅")

    # KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{df['Sales Value'].sum():,.0f}")
    col2.metric("Total Quantity", f"{df['Quantity Sold'].sum():,.0f}")
    col3.metric("Customers", df['Company Name (Customer)'].nunique())

    st.markdown("---")

    # Top Products
    top_products = df.groupby('Product Name')['Sales Value'].sum().sort_values(ascending=False).head(10)

    fig = px.bar(
        x=top_products.values,
        y=top_products.index,
        orientation='h',
        title="Top Products"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Monthly Trend
    monthly = df.groupby('Month')['Sales Value'].sum().reset_index()

    fig2 = px.line(monthly, x='Month', y='Sales Value', markers=True)

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Please upload a file to start")