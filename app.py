from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="AryaonSQL7#",  
    database="HospitalDB2"
)
cursor = db.cursor()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to view all patients
@app.route('/patients')
def view_patients():
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    return render_template('patients.html', patients=patients)

# Route to delete a patient by their ID
@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    cursor.execute("DELETE FROM Patient WHERE PatientID = %s", (patient_id,))
    db.commit()
    return redirect(url_for('view_patients'))

# Route to add a patient
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
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

# Route to update a patient
@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
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
        return redirect(url_for('view_patients'))

    cursor.execute("SELECT * FROM Patient WHERE PatientID=%s", (patient_id,))
    patient = cursor.fetchone()
    return render_template('edit_patient.html', patient=patient)

# Route to view list of doctors
@app.route('/doctors')
def view_doctors():
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()
    return render_template('doctors.html', doctors=doctors)

# Route to delete a doctor by their ID
@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    cursor.execute("DELETE FROM Doctor WHERE DoctorID = %s", (doctor_id,))
    db.commit()
    return redirect(url_for('view_doctors'))  # Redirect to the view doctors page

# Route to add a doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        cursor.execute(
            "INSERT INTO Doctor (Name, Specialization, Contact) VALUES (%s, %s, %s)",
            (name, specialization, contact)
        )
        db.commit()
        return redirect(url_for('view_doctors'))
    return render_template('add_doctor.html')

# Route to update a doctor
@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        cursor.execute(
            "UPDATE Doctor SET Name=%s, Specialization=%s, Contact=%s WHERE DoctorID=%s",
            (name, specialization, contact, doctor_id)
        )
        db.commit()
        return redirect(url_for('view_doctors'))

    cursor.execute("SELECT * FROM Doctor WHERE DoctorID=%s", (doctor_id,))
    doctor = cursor.fetchone()
    return render_template('edit_doctor.html', doctor=doctor)

# Route to view list of appointments
@app.route('/appointments')
def view_appointments():
    cursor.execute("""
        SELECT Appointment.AppointmentID, Patient.Name, Doctor.Name, Appointment.Date, Appointment.Time
        FROM Appointment
        JOIN Patient ON Appointment.PatientID = Patient.PatientID
        JOIN Doctor ON Appointment.DoctorID = Doctor.DoctorID
    """)
    appointments = cursor.fetchall()
    return render_template('appointments.html', appointments=appointments)

# Route to delete an appointment by its ID
@app.route('/delete_appointment/<int:appointment_id>')
def delete_appointment(appointment_id):
    cursor.execute("DELETE FROM Appointment WHERE AppointmentID = %s", (appointment_id,))
    db.commit()
    return redirect(url_for('view_appointments'))  # Redirect to the view appointments page

# Route to add an appointment
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']

        cursor.execute(
            "INSERT INTO Appointment (PatientID, DoctorID, Date, Time) VALUES (%s, %s, %s, %s)",
            (patient_id, doctor_id, date, time)
        )
        db.commit()
        return redirect(url_for('home'))

    # Fetch patient and doctor lists for the dropdown
    cursor.execute("SELECT PatientID, Name FROM Patient")
    patients = cursor.fetchall()

    cursor.execute("SELECT DoctorID, Name FROM Doctor")
    doctors = cursor.fetchall()

    return render_template('add_appointment.html', patients=patients, doctors=doctors)
 

# Route to update an appointment
@app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']

        cursor.execute(
            "UPDATE Appointment SET PatientID=%s, DoctorID=%s, Date=%s, Time=%s WHERE AppointmentID=%s",
            (patient_id, doctor_id, date, time, appointment_id)
        )
        db.commit()
        return redirect(url_for('view_appointments'))

    cursor.execute("SELECT * FROM Appointment WHERE AppointmentID=%s", (appointment_id,))
    appointment = cursor.fetchone()
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()

    return render_template('edit_appointment.html', appointment=appointment, patients=patients, doctors=doctors)

# Route to view list of bills
@app.route('/bills')
def view_bills():
    cursor.execute("""
        SELECT BillID, Patient.Name, TotalAmount, Date
        FROM Billing
        JOIN Patient ON Billing.PatientID = Patient.PatientID
    """)
    bills = cursor.fetchall()
    return render_template('bills.html', bills=bills)

# Route to delete a bill by its ID
@app.route('/delete_bill/<int:bill_id>')
def delete_bill(bill_id):
    cursor.execute("DELETE FROM Bill WHERE BillID = %s", (bill_id,))
    db.commit()
    return redirect(url_for('view_bills'))  # Redirect to the view bills page

# Route to add a bill
@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        total_amount = request.form['total_amount']
        date = request.form['date']

        cursor.execute(
            "INSERT INTO Billing (PatientID, TotalAmount, Date) VALUES (%s, %s, %s)",
            (patient_id, total_amount, date)
        )
        db.commit()
        return redirect(url_for('view_bills'))

    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    return render_template('add_bill.html', patients=patients)

# Route to update a bill
@app.route('/edit_bill/<int:bill_id>', methods=['GET', 'POST'])
def edit_bill(bill_id):
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        total_amount = request.form['total_amount']
        date = request.form['date']

        cursor.execute(
            "UPDATE Billing SET PatientID=%s, TotalAmount=%s, Date=%s WHERE BillID=%s",
            (patient_id, total_amount, date, bill_id)
        )
        db.commit()
        return redirect(url_for('view_bills'))

    cursor.execute("SELECT * FROM Billing WHERE BillID=%s", (bill_id,))
    bill = cursor.fetchone()
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()

    return render_template('edit_bill.html', bill=bill, patients=patients)

# Route to view list of treatments
@app.route('/treatments')
def view_treatments():
    cursor.execute("""
        SELECT Treatment.TreatmentID, Patient.Name AS PatientName, Doctor.Name AS DoctorName,
               Treatment.Diagnosis, Treatment.Medication, Treatment.Proc
        FROM Treatment
        JOIN Patient ON Treatment.PatientID = Patient.PatientID
        JOIN Doctor ON Treatment.DoctorID = Doctor.DoctorID
    """)
    treatments = cursor.fetchall()
    return render_template('treatments.html', treatments=treatments)

# Route to add a treatment
@app.route('/add_treatment', methods=['GET', 'POST'])
def add_treatment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        medication = request.form['medication']
        procedure = request.form['procedure']

        cursor.execute(
    "INSERT INTO Treatment (PatientID, DoctorID, Diagnosis, Medication, Proc) VALUES (%s, %s, %s, %s, %s)",
    (patient_id, doctor_id, diagnosis, medication, procedure)
)
        db.commit()
        return redirect(url_for('view_treatments'))

    cursor.execute("SELECT PatientID, Name FROM Patient")
    patients = cursor.fetchall()
    cursor.execute("SELECT DoctorID, Name FROM Doctor")
    doctors = cursor.fetchall()

    return render_template('add_treatment.html', patients=patients, doctors=doctors)

# Route to delete a treatment
@app.route('/delete_treatment/<int:treatment_id>')
def delete_treatment(treatment_id):
    cursor.execute("DELETE FROM Treatment WHERE TreatmentID = %s", (treatment_id,))
    db.commit()
    return redirect(url_for('view_treatments'))

# Route to edit a treatment
@app.route('/edit_treatment/<int:treatment_id>', methods=['GET', 'POST'])
def edit_treatment(treatment_id):
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        medication = request.form['medication']
        procedure = request.form['procedure']

        cursor.execute(
    "UPDATE Treatment SET PatientID=%s, DoctorID=%s, Diagnosis=%s, Medication=%s, Proc=%s WHERE TreatmentID=%s",
    (patient_id, doctor_id, diagnosis, medication, procedure, treatment_id)
)

        db.commit()
        return redirect(url_for('view_treatments'))

    cursor.execute("SELECT * FROM Treatment WHERE TreatmentID=%s", (treatment_id,))
    treatment = cursor.fetchone()
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()

    return render_template('edit_treatment.html', treatment=treatment, patients=patients, doctors=doctors)


if __name__ == "__main__":
    app.run(debug=True)


