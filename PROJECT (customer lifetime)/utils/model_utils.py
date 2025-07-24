import joblib
from sklearn.linear_model import LinearRegression

def train_and_save_clv_model(rfm, model_path='models/clv_model.pkl'):
    X = rfm[['Recency', 'Frequency', 'Monetary']]
    y = rfm['Monetary'] * 3  # Dummy assumption
    model = LinearRegression().fit(X, y)
    joblib.dump(model, model_path)

def load_clv_model(model_path='models/clv_model.pkl'):
    return joblib.load(model_path)