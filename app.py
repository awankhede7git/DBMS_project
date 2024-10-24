from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",   # Use your MySQL username
    password="AryaonSQL7#",  # Your MySQL password
    database="HospitalDB"
)
cursor = db.cursor()

@app.route('/')
def home():
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    return render_template('index.html', patients=patients)

# Route to handle adding a new patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        medical_history = request.form['medical_history']

        cursor.execute(
            "INSERT INTO Patient (Name, Age, Gender, Contact, MedicalHistory) VALUES (%s, %s, %s, %s, %s)",
            (name, age, gender, contact, medical_history)
        )
        db.commit()
        return redirect(url_for('home'))
    return render_template('add_patient.html')

# Route to handle updating a patient's details
@app.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
    patient = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        medical_history = request.form['medical_history']

        cursor.execute(
            "UPDATE Patient SET Name=%s, Age=%s, Gender=%s, Contact=%s, MedicalHistory=%s WHERE PatientID=%s",
            (name, age, gender, contact, medical_history, patient_id)
        )
        db.commit()
        return redirect(url_for('home'))

    return render_template('update_patient.html', patient=patient)

# Route to handle deleting a patient
@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    cursor.execute("DELETE FROM Patient WHERE PatientID = %s", (patient_id,))
    db.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)