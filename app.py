from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Function to create a connection to the SQLite database
def create_connection():
    connection = sqlite3.connect('hospital.db')
    return connection

# Home page route
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Validate username and password (you can replace this with your authentication logic)
        username = request.form['username']
        password = request.form['password']

        # Dummy validation, replace with your logic
        if username == 'admin' and password == 'password':
            # Example: Set a session variable to indicate the user is logged in
            session['user_id'] = 1  # Replace with the actual user ID
            return redirect(url_for('patient_details'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    # Clear the session variables
    session.clear()

    flash('Logout successful', 'success')
    return redirect(url_for('home'))

# Patient details route
@app.route('/patient_details', methods=['POST', 'GET'])
def patient_details():
    if request.method == 'POST':
        # Get patient details from the form
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        patient_gender = request.form['patient_gender']
        patient_address = request.form['patient_address']
        patient_symptoms = request.form['patient_symptoms']
        medicine_details = request.form['medicine_details']
        follow_up_date = request.form['follow_up_date']

        # Save patient details to the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO patients (name, age, gender, address, symptoms, medicine_details, follow_up_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (patient_name, patient_age, patient_gender, patient_address, patient_symptoms, medicine_details, follow_up_date))
        connection.commit()
        connection.close()

        flash('Patient details saved successfully', 'success')

    return render_template('patient_details.html')


# All patients route
@app.route('/all_patients', methods=['GET'])
def all_patients():
    # Retrieve all patient details from the database
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    connection.close()

    return render_template('all_patients.html', patients=patients)

# Medicine details route
@app.route('/medicine_details/<int:patient_id>', methods=['GET'])
def medicine_details(patient_id):
    # Retrieve medicine details for the specified patient ID
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    connection.close()

    return render_template('medicine_details.html', patient=patient)

# Search route for ID or Name
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']

    # Search patients by ID or name
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM patients WHERE id=? OR name LIKE ?', (search_query, f'%{search_query}%'))
    patients = cursor.fetchall()
    connection.close()

    return render_template('all_patients.html', patients=patients)



# Download patient details as Excel route with date range
@app.route('/download_excel_date_range/<start_date>/<end_date>', methods=['GET'])
def download_excel_date_range(start_date, end_date):
    try:
        # Parse start_date and end_date to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Retrieve patient details within the date range from the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM patients WHERE follow_up_date BETWEEN ? AND ?', (start_date, end_date))
        patients = cursor.fetchall()
        connection.close()

        # Create a DataFrame from the patient details
        df = pd.DataFrame(patients, columns=['ID', 'Name', 'Age', 'Gender', 'Address', 'Symptoms', 'Medicine Details', 'Follow-up Date'])

        # Save the DataFrame to an Excel file
        excel_file_path = 'patient_details_date_range.xlsx'
        df.to_excel(excel_file_path, index=False)

        # Return the Excel file as a downloadable response
        return send_file(excel_file_path, as_attachment=True)

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('all_patients'))


# Back to home page route
@app.route('/back_to_home', methods=['GET'])
def back_to_home():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
