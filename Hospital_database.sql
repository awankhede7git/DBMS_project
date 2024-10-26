-- Create the database
CREATE DATABASE HospitalDB;

-- Use the database
USE HospitalDB;

-- Create the Patient table
CREATE TABLE Patient (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Contact VARCHAR(15),
    MedicalHistory TEXT
);

-- Create the Doctor table
CREATE TABLE Doctor (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Specialization VARCHAR(100),
    Contact VARCHAR(15),
    Availability BOOLEAN
);

-- Create the Appointment table
CREATE TABLE Appointment (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    Date DATE,
    Time TIME,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Create the Treatment table
CREATE TABLE Treatment (
    TreatmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    Diagnosis TEXT,
    Medication TEXT,
    Procedure TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Create the Ward table
CREATE TABLE Ward (
    WardID INT AUTO_INCREMENT PRIMARY KEY,
    WardType VARCHAR(50),
    BedCount INT,
    Availability BOOLEAN
);

-- Create the Billing table
CREATE TABLE Billing (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    TotalAmount DECIMAL(10, 2),
    Date DATE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);
