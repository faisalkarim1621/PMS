from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define db here instead of importing from app.py

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    ocr_text = db.Column(db.Text, nullable=True)

    @staticmethod
    def generate_patient_id():
        import uuid
        return str(uuid.uuid4())[:8]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "location": self.location,
            "patient_id": self.patient_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "image_path": self.image_path,
            "ocr_text": self.ocr_text,
        }
