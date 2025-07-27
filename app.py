from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)

with open('artifacts/titanic_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        Pclass = int(request.form['Pclass'])
        Sex = 1 if request.form['Sex'] == 'male' else 0
        Age = float(request.form['Age'])
        SibSp = int(request.form['SibSp'])
        Parch = int(request.form['Parch'])
        Fare = float(request.form['Fare'])
        Embarked = request.form['Embarked']

        embarked_map = {'C': 0, 'Q': 1, 'S': 2}
        Embarked_val = embarked_map.get(Embarked, 2)

        input_data = [[Pclass, Sex, Age, SibSp, Parch, Fare, Embarked_val]]

        prediction = model.predict(input_data)
        survived = int(prediction[0])

        return render_template('result.html', prediction=survived)

    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
