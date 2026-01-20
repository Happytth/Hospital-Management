from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class User(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    email_id=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(255),nullable=False)
    is_active=db.Column(db.Boolean(),default=True)
    role=db.Column(db.String(255),nullable=False,default="user")
    gender=db.Column(db.String(255),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"),nullable=True)
    availability = db.Column(db.String(255),nullable=True) 
    status = db.Column(db.String(255),nullable=True)
    slot = db.relationship("Slots", backref="user", lazy=True, cascade='all, delete-orphan')
    fees=db.Column(db.Integer,nullable=True)
    

class Appoinment(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    doc_id=db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
   
    slot_id=db.Column(db.Integer,db.ForeignKey("slots.id"),nullable=False)
    
    status=db.Column(db.String(255),nullable=False,default="pending")
    payment=db.Column(db.String(255),nullable=False,default="not done")
    
    patient = db.relationship("User", foreign_keys=[patient_id], backref="patient_appointments")
    doctor = db.relationship("User", foreign_keys=[doc_id], backref="doctor_appointments")
    treatment = db.relationship("Treatment", backref="appointment", uselist=False, cascade='all, delete-orphan')
    
class Treatment(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    appoinment_id=db.Column(db.Integer,db.ForeignKey(Appoinment.id),nullable=False)
    diagnosis=db.Column(db.String(255),nullable=False)
    
    prescription=db.Column(db.String(255),nullable=False)
    notes=db.Column(db.String(255),nullable=False)
    
   
class Department(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    dept_id=db.Column(db.String(255),nullable=False,unique=True)
    dept_name=db.Column(db.String(255),nullable=False)
    description=db.Column(db.String(255),nullable=True)
    
    doc_registred=db.relationship("User", backref="department", lazy=True)
    bg_img=db.Column(db.String(255),nullable=True,unique=False,default="https://i.pinimg.com/236x/79/48/9e/79489e4a15d6a6d71cb6e324ab29bb81.jpg")
        
class Slots(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date,nullable=False)
    slots_time=db.Column(db.String(10),nullable=False)
    is_booked=db.Column(db.Boolean,nullable=False,default=False)
    
    user_id=db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    appoinment = db.relationship("Appoinment", backref="slot", uselist=False, cascade="all, delete-orphan")
    