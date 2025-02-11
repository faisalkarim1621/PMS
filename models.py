from app import db
from datetime import datetime
import os

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(500))
    ocr_text = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'location': self.location,
            'patient_id': self.patient_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'ocr_text': self.ocr_text
        }

    @staticmethod
    def generate_patient_id():
        last_patient = Patient.query.order_by(Patient.id.desc()).first()
        if last_patient:
            last_id = int(last_patient.patient_id)
            new_id = str(last_id + 1).zfill(5)
        else:
            new_id = "00001"
        return new_id