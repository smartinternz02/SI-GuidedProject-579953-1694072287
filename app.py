from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

# Save the model

model = pickle.load(open('F:/project_new/model.pkl', 'rb'))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")
def index():
    return render_template("predict.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    pt = "Error"
    
    if request.method == 'POST':
        SIZE = float(request.form['SIZE'])
        FUEL = request.form['FUEL']  # No need to convert to float
        DISTANCE = float(request.form['DISTANCE'])
        DESIBEL = float(request.form['DESIBEL'])
        AIRFLOW = float(request.form['AIRFLOW'])
        FREQUENCY = float(request.form['FREQUENCY'])

        # Map the FUEL value to a numerical value
        if FUEL == 'Gasoline':
            FUEL = 1.0  # Replace with the actual numerical value
        elif FUEL == 'OtherFuelType':
            FUEL = 2.0  # Replace with the actual numerical value
        # Add more mappings as needed

        data = [[SIZE, FUEL, DISTANCE, DESIBEL, AIRFLOW, FREQUENCY]]
        df = pd.DataFrame(data, columns=['SIZE', 'FUEL', 'DISTANCE', 'DESIBEL', 'AIRFLOW', 'FREQUENCY'])

        prediction = model.predict(df)
        prediction = prediction[0]

        if prediction == 0:
            pt = "The fire is in a non-extinction state"
            
        else:
            pt = "The fire is in an extinction state"

    return render_template('results.html', prediction_text=pt)

#     # return render_template('predict.html')  # Return to the input form if it's a GET request or no POST data

if __name__ == '__main__':
    app.run(debug=True)
