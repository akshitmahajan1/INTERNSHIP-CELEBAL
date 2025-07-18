import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load model and encoders
model = joblib.load('model/titanic_model.pkl')
le_sex = joblib.load('model/label_encoder_sex.pkl')
le_embarked = joblib.load('model/label_encoder_embarked.pkl')

# Title
st.title("🚢 Titanic Survival Prediction App")
st.markdown("Enter passenger details to check survival prediction using a Random Forest model.")

# Input UI
pclass = st.selectbox("Passenger Class (Pclass)", [1, 2, 3])
sex = st.selectbox("Sex", ['male', 'female'])
age = st.slider("Age", 0, 80, 30)
fare = st.slider("Fare", 0.0, 500.0, 32.0)
embarked = st.selectbox("Port of Embarkation", ['S', 'C', 'Q'])

# Preprocessing input
sex_encoded = le_sex.transform([sex])[0]
embarked_encoded = le_embarked.transform([embarked])[0]
input_data = np.array([[pclass, sex_encoded, age, fare, embarked_encoded]])

# Prediction
prediction = model.predict(input_data)[0]
prediction_proba = model.predict_proba(input_data)[0]

st.subheader("Prediction Result")
if prediction == 1:
    st.success("🎉 The passenger **survived**.")
else:
    st.error("💀 The passenger **did not survive**.")

st.subheader("Prediction Probability")
st.write(f"Survival Probability: {prediction_proba[1]*100:.2f}%")
st.progress(int(prediction_proba[1]*100))

# Sample data overview and visual
st.subheader("Sample Dataset Overview")
df = pd.read_csv("data\Titanic-Dataset.csv")
df = df[['Survived', 'Pclass', 'Sex', 'Age', 'Fare', 'Embarked']].dropna()
st.dataframe(df.sample(5))

st.subheader("Survival Rate by Class and Sex")
fig, ax = plt.subplots()
sns.barplot(data=df, x='Pclass', y='Survived', hue='Sex', ax=ax)
st.pyplot(fig)
