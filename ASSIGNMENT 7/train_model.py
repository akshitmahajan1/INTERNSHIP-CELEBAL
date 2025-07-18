import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
df = pd.read_csv('data/Titanic-Dataset.csv')

# Preprocess
df = df[['Survived', 'Pclass', 'Sex', 'Age', 'Fare', 'Embarked']].dropna()
le_sex = LabelEncoder()
le_embarked = LabelEncoder()

df['Sex'] = le_sex.fit_transform(df['Sex'])
df['Embarked'] = le_embarked.fit_transform(df['Embarked'])

X = df.drop('Survived', axis=1)
y = df['Survived']

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/titanic_model.pkl")
joblib.dump(le_sex, "model/label_encoder_sex.pkl")
joblib.dump(le_embarked, "model/label_encoder_embarked.pkl")