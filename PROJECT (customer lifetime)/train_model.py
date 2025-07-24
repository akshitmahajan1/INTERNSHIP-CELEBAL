import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load data
df = pd.read_excel("data/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df.dropna(subset=["Customer ID"], inplace=True)
df = df[df["Quantity"] > 0]
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Create RFM
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "Invoice": "nunique",
    "TotalPrice": "sum"
})
rfm.columns = ["Recency", "Frequency", "Monetary"]

# Train a simple CLV model (just use Monetary * 3 as target for now)
X = rfm[["Recency", "Frequency", "Monetary"]]
y = rfm["Monetary"] * 3

model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "models/clv_model.pkl")
print("✅ Model trained and saved successfully.")