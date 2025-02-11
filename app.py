import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import secure_filename
from ocr_utils import process_image
import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "patient_records_secret_key"

# Configure uploads folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure SQLite database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Import models after db initialization
from models import Patient

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['POST'])
def add_patient():
    try:
        data = request.form
        file = request.files.get('document')
        ocr_text = None
        image_path = None

        if file:
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = os.path.join('uploads', filename)
            ocr_text = process_image(file)

        patient = Patient(
            name=data['name'],
            age=int(data['age']),
            location=data['location'],
            patient_id=Patient.generate_patient_id(),
            date=datetime.datetime.strptime(data['date'], '%Y-%m-%d'),
            image_path=image_path,
            ocr_text=ocr_text
        )

        db.session.add(patient)
        db.session.commit()
        return jsonify({"success": True, "message": "Patient added successfully"})
    except Exception as e:
        logging.error(f"Error adding patient: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    query = request.args.get('query', '')
    patients = Patient.query.filter(
        (Patient.name.ilike(f'%{query}%')) |
        (Patient.patient_id.ilike(f'%{query}%'))
    ).all()
    return jsonify([p.to_dict() for p in patients])

@app.route('/api/ocr', methods=['POST'])
def ocr_scan():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400

    try:
        text = process_image(file)
        return jsonify({"success": True, "text": text})
    except Exception as e:
        logging.error(f"OCR processing error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400