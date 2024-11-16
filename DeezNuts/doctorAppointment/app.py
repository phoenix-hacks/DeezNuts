from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Doctor data
doctors = [
    {"name": "Dr. Smith", "specialty": "General Physician", "diseases": ["fever", "sore_throat"], "patientsAhead": 3},
    {"name": "Dr. Jane", "specialty": "Endocrinologist", "diseases": ["diabetes"], "patientsAhead": 5},
    {"name": "Dr. John", "specialty": "ENT Specialist", "diseases": ["sore_throat"], "patientsAhead": 2},
    {"name": "Dr. Sarah", "specialty": "General Physician", "diseases": ["fever", "diabetes"], "patientsAhead": 4}
]

# Disease times in minutes
disease_time = {
    "fever": 15,
    "diabetes": 60,
    "sore_throat": 10
}

# Cost calculation parameters
fee_per_minute_usd = 1  # reduced cost
usd_to_inr_rate = 82

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    age = data.get("age")
    disease = data.get("disease")
    doctor = data.get("doctor")

    # Validation checks
    if not all([name, phone, age, disease, doctor]):
        return jsonify({"error": "All fields are required"}), 400
    
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({"error": "Phone number must be 10 digits"}), 400

    if int(age) <= 0:
        return jsonify({"error": "Age must be a positive number"}), 400

    # Return success message for booking
    return jsonify({"message": "Appointment booked successfully!"}), 200

@app.route("/get_doctors", methods=["POST"])
def get_doctors():
    data = request.json
    disease = data.get("disease")
    if not disease:
        return jsonify({"error": "Disease not provided"}), 400

    # Filter doctors who can treat the disease
    available_doctors = [
        {"name": doctor["name"], "specialty": doctor["specialty"], "patientsAhead": doctor["patientsAhead"]}
        for doctor in doctors if disease in doctor["diseases"]
    ]
    return jsonify(available_doctors)

@app.route("/calculate_fees", methods=["POST"])
def calculate_fees():
    data = request.json
    doctor_name = data.get("doctor_name")
    disease = data.get("disease")

    if not doctor_name or not disease:
        return jsonify({"error": "Doctor name or disease not provided"}), 400

    # Find the doctor and calculate the total time and fees
    doctor = next((doc for doc in doctors if doc["name"] == doctor_name), None)
    if not doctor or disease not in disease_time:
        return jsonify({"error": "Invalid doctor or disease"}), 400

    patients_ahead = doctor["patientsAhead"]
    time_per_patient = disease_time[disease]
    total_time = patients_ahead * time_per_patient
    total_fee_usd = total_time * fee_per_minute_usd
    total_fee_inr = round(total_fee_usd * usd_to_inr_rate)

    return jsonify({
        "patients_ahead": patients_ahead,
        "total_time": total_time,
        "total_fee_inr": total_fee_inr
    })

if __name__ == "__main__":
    app.run(debug=True)
