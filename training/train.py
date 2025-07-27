from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import pickle
import os

def load_titanic_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    data = pd.read_csv(url)
    return data

data = load_titanic_data()

data = data.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])

data['Age'].fillna(data['Age'].mean(), inplace=True)
data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
data['Embarked'] = data['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

data = data.dropna()

X_train, X_test, y_train, y_test = train_test_split(
    data.drop(columns=['Survived']),
    data['Survived'],
    test_size=0.2,
    random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

os.makedirs('artifacts/', exist_ok=True)

with open('artifacts/titanic_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)