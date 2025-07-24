# 📁 streamlit_app.py (Polished Version)

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils.model_utils import load_clv_model

# ===========================
# 🎨 CSS Styling
# ===========================

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# ===========================
# 📦 Load Clean Data & Model
# ===========================

@st.cache_data

def load_data():
    df = pd.read_excel('data/online_retail_II.xlsx', sheet_name='Year 2010-2011')
    df.rename(columns={
        'Invoice': 'InvoiceNo',
        'CustomerID': 'Customer ID',
        'UnitPrice': 'Price'
    }, inplace=True)
    df.dropna(subset=['Customer ID'], inplace=True)
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]
    df['Customer ID'] = df['Customer ID'].astype(int)
    df['TotalPrice'] = df['Quantity'] * df['Price']
    return df

def get_features(df):
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    clv_data = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum',
        'Country': 'first'
    }).reset_index()
    clv_data.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary', 'Country']
    clv_data['Segment'] = pd.qcut(clv_data['Monetary'], q=4, labels=["Low", "Mid", "High", "Very High"])
    return clv_data

# ✅ Load assets
df = load_data()
features = get_features(df)
model = load_clv_model('models/clv_model.pkl')

# ===========================
# 🧠 Homepage & Introduction
# ===========================

st.title("🧠 Customer Lifetime Value Intelligence")
st.markdown("""
Welcome to the CLV Intelligence Dashboard.
Here, you can:
- 🔍 Predict a customer's lifetime value
- 📈 Simulate business revenue from loyalty efforts
- 🎯 Recommend products based on behavior
- 🌍 Explore geographic churn risks
""")

# ===========================
# 1️⃣ Predict CLV for a Customer
# ===========================

st.header("🔍 Predict CLV for a Customer")
customer_id = st.selectbox("Choose a Customer ID", features['Customer ID'].unique())

if customer_id:
    customer_row = features[features['Customer ID'] == customer_id]
    input_features = customer_row[['Recency', 'Frequency', 'Monetary']]
    clv_prediction = model.predict(input_features)[0]
    st.metric(label=f"💰 Predicted CLV for Customer {customer_id}", value=f"₹{clv_prediction:,.2f}")

# ===========================
# 2️⃣ Revenue Simulator by Segment
# ===========================

st.header("📈 Revenue Simulator by Segment")
segment = st.selectbox("Select Segment", features['Segment'].unique())
retention_uplift = st.slider("Retention Increase (%)", 0, 100, 10)
order_uplift = st.slider("Avg Order Value Increase (%)", 0, 100, 5)

if st.button("Simulate Revenue Uplift"):
    seg_df = features[features['Segment'] == segment]
    base = model.predict(seg_df[['Recency', 'Frequency', 'Monetary']])
    new_clv = base * (1 + retention_uplift / 100) * (1 + order_uplift / 100)
    uplift = new_clv.sum() - base.sum()
    st.success(f"📊 Estimated Revenue Gain: ₹{uplift:,.2f} for segment '{segment}'")

# ===========================
# 3️⃣ Product Recommender
# ===========================

st.header("🎯 Personalized Product Recommender")
if customer_id:
    cust_purchases = df[df['Customer ID'] == customer_id]['Description'].value_counts().head(3).index.tolist()
    st.markdown("**Most Frequently Purchased Products:**")
    for item in cust_purchases:
        st.markdown(f"- {item}")

    similar_customers = df[df['Description'].isin(cust_purchases)]['Customer ID'].unique().tolist()
    reco_items = df[df['Customer ID'].isin(similar_customers)]['Description'].value_counts().head(5)
    st.markdown("**Similar Users Also Bought:**")
    for item in reco_items.index:
        st.markdown(f"- {item}")

# ===========================
# 4️⃣ Churn Risk Map
# ===========================

st.header("🌍 Geographic Churn Risk Map")
geo_df = features.groupby('Country').agg({'Monetary': 'mean', 'Frequency': 'mean'}).reset_index()
geo_df['Churn Risk'] = geo_df['Monetary'] / geo_df['Frequency']

fig = px.choropleth(geo_df, locations='Country', locationmode='country names',
                    color='Churn Risk', hover_name='Country',
                    color_continuous_scale='Reds', title="Churn Risk by Country")

st.plotly_chart(fig, use_container_width=True)

# ===========================
# ✅ Footer
# ===========================

st.markdown("""
---
👨‍💼 Built for smart customer retention strategies | Developed with ❤️ using Streamlit
""")