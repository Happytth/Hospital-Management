from flask import Blueprint, jsonify, request, url_for,send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user
from controllers.model import *
from functools import wraps
import os
from caching import cache 
from datetime import datetime, timedelta, date
from controllers.task import csv_report, month_report, daily_remainder
from celery.result import AsyncResult

auth = Blueprint("auth", __name__)

@auth.route('/login',methods=['POST'])
def login():
    email_id=request.json.get("email_id",None)
   # name=request.json.get("name",None)
    password=request.json.get("password",None)
    # role=request.json.get("role",None)
    # is_active=request.json.get("is_active",0)
    
    user=User.query.filter_by(email_id=email_id).one_or_none()
    if not user or user.password != password:
        return jsonify("Wrong password or email id") , 401
    
    access_token= create_access_token(identity=user)
    return jsonify(access_token=access_token)

@auth.route('/protect' , methods=['GET'])
@jwt_required()
def protected():
  currentUser=get_jwt_identity()
  return jsonify(logged_in_as=currentUser)

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(msg="Access Denied :Role not authorized"),403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@auth.route('/register',methods=['POST'])
def register():
    email_id=request.json.get("email_id",None)
    password=request.json.get("password",None)
    name=request.json.get("name",None)
    age=request.json.get("age",None)
    gender=request.json.get("gender",None)
    
    user=User.query.filter_by(email_id=email_id).one_or_none()
    if not user:
        user = User(
        email_id=email_id,
        password=password,    
        name=name,
        age=age,
        gender=gender
    )
        db.session.add(user)
        db.session.commit()
        access_token=create_access_token(identity=user)
        return jsonify(access_token=access_token) ,200
    else:
        return jsonify("Already an existing user please login to continue"), 400
    
@auth.route('/admin_dashboard')
@role_required("admin")
@cache.cached(timeout=10)
def admin_dashboard():
    user_count = User.query.filter_by(role='user').count()
    doctor_count = User.query.filter_by(role='doctor').count()
    total_appointments = Appoinment.query.count()
    cancelled_appointments = Appoinment.query.filter_by(status="cancelled").count()
    booked_appointments= Appoinment.query.filter_by(status='booked').count()
    departments= Department.query.all()
    
    
    male_count = User.query.filter(User.gender.ilike('male')).count()
    female_count = User.query.filter(User.gender.ilike('female')).count()
    other_count = User.query.filter(User.gender.ilike('other')).count()
    
    department_data = [
        {
            "dept_name": d.dept_name,
            "doctor_count": len(d.doc_registred)
        }
        for d in departments
    ]

    return jsonify({
        "user_count": user_count,
        "doctor_count": doctor_count,
        "total_appointments": total_appointments,
        "gender_data": {'male': male_count, 'female': female_count, 'others': other_count},
        "cancelled_appointments": cancelled_appointments,
        "appointments": {'booked': booked_appointments, 'completed': total_appointments-booked_appointments-cancelled_appointments
                         , 'cancelled': cancelled_appointments},
        "departments":department_data
    })
    
@auth.route("/admin_patients", methods=['GET','POST','PUT','DELETE'])
@role_required("admin")
def admin_patients():
    if request.method == "GET":
        patients = User.query.all()
        patientsList = [
            {
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "gender": p.gender,
                "email_id": p.email_id,
                "role": p.role,
                "is_active": p.is_active,
                "password": p.password
            }
            for p in patients if p.role == "user"
        ]
        return jsonify({"patientsList": patientsList})

    elif request.method == "PUT":
        data = request.get_json()
        user_id = data.get("id")  

        patient = User.query.filter_by(id=user_id).one_or_none()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        patient.email_id = data.get("email_id", patient.email_id)
        patient.password = data.get("password", patient.password)
        patient.name = data.get("name", patient.name)
        patient.age = data.get("age", patient.age)
        patient.gender = data.get("gender", patient.gender)
        patient.is_active = data.get("is_active", patient.is_active)

        db.session.commit()
        return jsonify({"message": "Patient updated successfully"}), 200
    
    elif request.method =="POST":
        email_id=request.json.get("email_id",None)
        password=request.json.get("password",None)
        name=request.json.get("name",None)
        age=request.json.get("age",None)
        gender=request.json.get("gender",None)
        
        user=User.query.filter_by(email_id=email_id).one_or_none()
        if not user:
            user = User(
            email_id=email_id,
            password=password,    
            name=name,
            age=age,
            gender=gender
        )
            db.session.add(user)
            db.session.commit()
            access_token=create_access_token(identity=user)
            return jsonify(access_token=access_token) ,200
        else:
            return jsonify("Already an existing user please login to continue"), 400
    else:
        data=request.get_json()
        d_id=data.get("id")
        department=User.query.filter_by(id=d_id).one_or_none()
        db.session.delete(department)    
        db.session.commit()
        return jsonify({"message": "Patient removed successfully"}), 200
        
@auth.route('/admin_doctors',methods=['GET','PUT','POST','DELETE'])
@role_required("admin")
def admin_doctor():
    if request.method=='GET':
        doctors = User.query.all()
        department=Department.query.all()
        doctorsList = [{
            "id": d.id,
            "name": d.name,
            "email_id": d.email_id,
            "role": d.role,
            "age": d.age,
            "gender": d.gender,
            "is_active": d.is_active,
            "department_id": d.department_id
        } for d in doctors if d.role == "doctor"
        ]
        departmentList=[{
            "id":d.id,
            "dept_id":d.dept_id,
            "dept_name":d.dept_name,
            "description":d.description,
            "doc_registred": [doc.name for doc in doctors if doc.department_id == d.id and doc.role == "doctor"]

            
        } for d in department]
        
        return jsonify({"doctorsList": doctorsList,
                        "departmentList": departmentList})
    
    elif request.method == 'PUT':
        data = request.get_json()
        doctor_id = data.get("id")

        if not doctor_id:
            return jsonify({"error": "Doctor ID is required"}), 400

        doctor = User.query.filter_by(id=doctor_id).one_or_none()
        if not doctor or doctor.role != "doctor":
            return jsonify({"error": "Doctor not found"}), 404

        doctor.email_id = data.get("email_id", doctor.email_id)
        doctor.age = data.get("age", doctor.age)
        doctor.gender = data.get("gender", doctor.gender)
        doctor.is_active = data.get("is_active", doctor.is_active)
        doctor.name = data.get("name", doctor.name)
        doctor.department_id =data.get("department_id", doctor.department_id)

        db.session.commit()
        return jsonify({"message": "Doctor updated successfully"}), 200

    
    elif request.method=='POST':
        email_id=request.json.get("email_id",None)
        password=request.json.get("password",None)
        name=request.json.get("name",None)
        age=request.json.get("age",None)
        gender=request.json.get("gender",None)
        department_id=request.json.get("department_id",None)
        
        user=User.query.filter_by(email_id=email_id).one_or_none()
        if not user:
            user= User(
                email_id=email_id,
                password=password,
                role='doctor',
                gender=gender,
                name=name,
                age=age,
                department_id=department_id
            )
            db.session.add(user)
            db.session.commit()
            access_token=create_access_token(identity=user)
            return jsonify(access_token=access_token) ,200
        return jsonify("Doctor already exists"), 404
    else:
        data=request.get_json()
        d_id=data.get("id")
        department=User.query.filter_by(id=d_id).one_or_none()
        db.session.delete(department)    
        db.session.commit()
        return jsonify({"message": "Doctor removed successfully"}), 200
    
@auth.route('/admin_department',methods=["GET","POST","PUT","DELETE"])
@role_required("admin")
def department():
    if request.method=="GET":
        department=Department.query.all()
        doctor=User.query.all()
        departmentList=[{
            "id":d.id,
            "dept_id":d.dept_id,
            "dept_name":d.dept_name,
            "description":d.description,
            # "doc_registred":d.doc_registred
            "bg_img":d.bg_img
        } for d in department]
        
        doctorList = [{
            "id": d.id,
            "name": d.name,
            "email_id": d.email_id,
            "role": d.role,
            "age": d.age,
            "gender": d.gender,
            "is_active": d.is_active,
            "department_id": d.department_id
        } for d in doctor if d.role == "doctor"
        ] 
        return jsonify({"departmentList": departmentList,
                        "doctorList": doctorList})
         
    elif request.method=="PUT":
        data = request.get_json()
        department_id = data.get("id")

        if not department_id:
            return jsonify({"message": "Department ID is required"}), 400

        department = Department.query.filter_by(id=department_id).one_or_none()
        if not department:
            return jsonify({"message": "department not found"}), 404
        
        new_dept_id = data.get("dept_id")
        if new_dept_id:
            existing_department = Department.query.filter_by(dept_id=new_dept_id).first()
            if existing_department and existing_department.id != department_id:
                return jsonify({"message": "department id already exists"}), 400
        
        department.dept_id = data.get("dept_id", department.dept_id)
        department.dept_name = data.get("dept_name", department.dept_name)
        department.description = data.get("description", department.description)
    #    department.doc_registred = data.get("doc_registred", department.doc_registred)
        department.bg_img = data.get("bg_img", department.bg_img)

        db.session.commit()
        return jsonify({"message": "department updated successfully"}), 200
    
    elif request.method=="POST":
        dept_id=request.json.get("dept_id")
        dept_name=request.json.get("dept_name")
        description=request.json.get("description")
      #  doc_registred=request.json.get("doc_registred")
        bg_img=request.json.get("bg_img")
        
        department=Department.query.filter_by(dept_id=dept_id).one_or_none()
        if not department:
            new_department=Department(
                dept_id=dept_id,
                dept_name=dept_name,
                description=description,
        #        doc_registred=doc_registred
                bg_img=bg_img
            )
            db.session.add(new_department)
            db.session.commit()
            return jsonify({"message": "Department added successfully"}), 200
        return jsonify({"error": "Department already exists"}), 404
    else:
        data=request.get_json()
        d_id=data.get("id")
        department=Department.query.filter_by(id=d_id).one_or_none()
        db.session.delete(department)    
        db.session.commit()
        return jsonify({"message": "Department removed successfully"}), 200
    

@auth.route("/admin_appointment",methods=['GET','PUT','POST','DELETE'])
@role_required("admin")
def admin_appointment():
    if request.method=='GET':
        appointments=Appoinment.query.all()
        appointmentlist=[{
            "id":a.id,
            "patient_id":a.patient_id,
            "patient_name":a.patient.name,
            "doctor_id":a.doc_id,
            "doctor_name":a.doctor.name,
            "status":a.status,
            "payment":a.payment,
            "date":str(a.slot.date),
            "time":a.slot.slots_time,
            "diagnosis": a.treatment.diagnosis if a.treatment else "N/A",
            "prescription": a.treatment.prescription if a.treatment else "N/A",
            "notes":a.treatment.notes if a.treatment else "N/A"
            
        }for a in appointments]
        
        return jsonify({"appointmentlist":appointmentlist}), 200
    elif request.method=="PUT":
        data=request.get_json()
        app_id = data.get("app_id")
        
        appointment=Appoinment.query.filter_by(id=app_id).one_or_none()
        
        
        if not appointment:
            return jsonify({"message":"Appointment doesn't exists"}), 400
        
        appointment.slot_id=data.get("slot_id",appointment.slot_id)
        appointment.doc_id=data.get("doc_id",appointment.doc_id)
        appointment.patient_id=data.get("patient_id",appointment.patient_id)
        appointment.status=data.get("status",appointment.status)
        appointment.payment=data.get("payment",appointment.payment)
        db.session.commit()
        
        return jsonify({"message": "Appointment details updated successfully "}), 200
    
@auth.route("/patient_dashboard",methods=["GET","POST","PUT","DELETE"])
@role_required("user")
def patient_dashboard():
    if request.method=="GET":
        current_user=get_jwt_identity()
        cur_user=User.query.filter_by(email_id=current_user).one_or_none()
        doctors=User.query.all()
        doctorList=[
            {
            "id": d.id,
            "name": d.name,
            "email_id": d.email_id,
            "role": d.role,
            "age": d.age,
            "gender": d.gender,
            "is_active": d.is_active,
            "department_id": d.department_id,
            "availability": d.availability
            
        } for d in doctors if (d.role=="doctor")
        ]
        patientList=[
            {
                "id":d.id,
                "name": d.name,
                "email_id": d.email_id,
                "role": d.role,
                "age": d.age,
                "gender": d.gender,
                "is_active": d.is_active,
            } for d in doctors if (d.role=="user")
        ]
        
        appointment=Appoinment.query.filter_by(patient_id=cur_user.id).all()
        appointmentslist=[{
            "id":a.id,
            "patient_id":a.patient_id,
            "doc_id":a.doc_id,
            "doctor_name":a.doctor.name,
            "department":a.doctor.department.dept_name,
            "slot": {
        "id": a.slot.id,
        "date": a.slot.date.isoformat(),
        "slots_time": a.slot.slots_time,
        "is_booked": a.slot.is_booked,
        "user_id": a.slot.user_id
    } if a.slot else None,  
    "status": a.status,
    "payment": a.payment
            
        }for a in appointment if a.status=="booked" and a.doctor.is_active==1]
        
        department=Department.query.all()
        departmentList=[{
            "id":d.id,
            "dept_id":d.dept_id,
            "dept_name":d.dept_name,
            "description":d.description,
            # "doc_registred":d.doc_registred
            "bg_img":d.bg_img
        } for d in department]
        
        
        
        
        return jsonify({"doctorList":doctorList,
                        "patientList":patientList,
                        "cur_user": {
        "id": cur_user.id,
        "email_id": cur_user.email_id,
        "name": cur_user.name,
        "gender": cur_user.gender,
        "age": cur_user.age,
    },
                        "appointmentslist":appointmentslist,
                        "departmentList":departmentList})
    
    elif request.method=='PUT':
        
        data = request.get_json()
        app_id = data.get("id")
        status = data.get("status")

        appointment = Appoinment.query.filter_by(id=app_id).one_or_none()
  
        if status:
            if status == "completed":
                treatment = Treatment.query.filter_by(appoinment_id=app_id).one_or_none()
                if not treatment or appointment.id != treatment.appoinment_id:
                    return jsonify({"message": "Cannot complete appointment without treatment"}), 400
                appointment.status = status
                db.session.commit()
                
            elif status =="cancelled":
                appointment.status = status
                appointment.slot.is_booked=0
                db.session.commit()
                return jsonify({"message": 'Appointment cancelled successfully'}), 200
            
        
@auth.route("/patient_doctor",methods=['GET','PUT','POST','DELETE'])
@role_required("user")
def patient_doctor():
    if request.method == 'GET':
        doctors = User.query.filter_by(role="doctor").all()
        departments = Department.query.all()

        departmentList = [{
            "id": d.id,
            "dept_id": d.dept_id,
            "dept_name": d.dept_name,
        } for d in departments]

        doctorsList = []
        for d in doctors:
            
            doctor_slots = Slots.query.filter_by(user_id=d.id).all()
            slot_list = [{
                "id": s.id,
                "date": s.date,
                "slots_time": s.slots_time,
                "is_booked": s.is_booked
            } for s in doctor_slots]

            doctorsList.append({
                "id": d.id,
                "email_id":d.email_id,
                "name": d.name,
                "availability": d.availability,
                "department_id": d.department_id,
                "age": d.age,
                "gender": d.gender,
                "is_active": d.is_active,
                "slots": slot_list,
                "fees": d.fees,
                "dept_name":d.department.dept_name
            })

        return jsonify({
            "doctorsList": doctorsList,
            "departmentList": departmentList
        })
    elif request.method=="POST":
        data = request.get_json()
        doctor_id = data.get("doctor_id")
        slot_id = data.get("selected_slot")

      
        current_user_email = get_jwt_identity()
        patient = User.query.filter_by(email_id=current_user_email).first_or_404()

        doctor = User.query.filter_by(id=doctor_id, role="doctor").first_or_404()
        slot = Slots.query.filter_by(id=slot_id, user_id=doctor_id).first_or_404()

        if slot.is_booked:
            return jsonify({"error": "Slot already booked"}), 400

        slot.is_booked = True
        appointment = Appoinment(patient_id=patient.id,
                                doc_id=doctor.id,
                                slot_id=slot.id,
                                status="booked")

        db.session.add(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment done successfully"}), 200

        
@auth.route("/patient_profile",methods=['GET','PUT','DELETE'])
@role_required("user")
def patient_profile():
    if request.method=='GET':
        user=User.query.get(current_user.id)

        return jsonify({
            "formData":{
                "id":user.id,
                "name":user.name,
                "gender":user.gender,
                "email_id":user.email_id,
                "age":user.age
            }
        })
        
    elif request.method == 'PUT':
        data = request.get_json()

        user = User.query.get(current_user.id)
        if user is None:
            return jsonify({"message": "User not found"}), 404

        new_email_id = data.get("email_id")
        
        if new_email_id and new_email_id != user.email_id:
            existing_user = User.query.filter_by(email_id=new_email_id).first()
            if existing_user:
                return jsonify({"message": "Email ID already exists"}), 409  

    
        user.email_id = data.get("email_id", user.email_id)
        user.name = data.get("name", user.name)
        user.age = data.get("age", user.age)
        user.gender = data.get("gender", user.gender)
        user.password = data.get("password", user.password)  

        db.session.commit()
        return jsonify({"message": "Credentials successfully updated"}), 200

            
    else:
        user=User.query.get(current_user.id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"}), 200    
    
@auth.route("/patient_appointment", methods=["GET", "POST", "PUT", "DELETE"])
@role_required("user")
def patient_appointment():
    if request.method == "GET":
        appointments = Appoinment.query.filter_by(patient_id=current_user.id).all()
        
        upcoming_appointments = []
        past_appointments = []
        today = date.today()

        for appt in appointments:
            appointment_data = {
                "id": appt.id,
                "doctor_name": appt.doctor.name,
                "specialization": appt.doctor.department.dept_name if appt.doctor.department else "N/A",
                "date": str(appt.slot.date),
                "time": appt.slot.slots_time,
                "status": appt.status,
                "payment": appt.payment,
                "diagnosis": appt.treatment.diagnosis if appt.treatment else "N/A",
                "prescription": appt.treatment.prescription if appt.treatment else "N/A",
                "notes":appt.treatment.notes if appt.treatment else "N/A",
                "fees":appt.doctor.fees if appt.doctor.fees else "N/A"
            }

            if appt.slot.date >= today and appt.status=="booked":
                upcoming_appointments.append(appointment_data)
            else:
                past_appointments.append(appointment_data)
        
        return jsonify({
            "upcoming_appointments": upcoming_appointments,
            "past_appointments": past_appointments
        })
        
    elif request.method=="PUT":
        data=request.get_json()
        id=data.get("id")
        
        appointment=Appoinment.query.filter_by(id=id).one_or_none()
        slot=Slots.query.filter_by(id=appointment.slot.id).one_or_none()
        if not appointment:
            return jsonify({"message": "No appointment with this appointment id exists"}), 400
        
        if data.get("status")=='cancelled':
            slot.is_booked=0
            
        appointment.status = data.get("status",appointment.status)
        appointment.payment= data.get("payment",appointment.payment)
        
        db.session.commit()
        appointments = Appoinment.query.filter_by(patient_id=current_user.id).all()
        
        upcoming_appointments = []
        past_appointments = []
        today = date.today()

        for appt in appointments:
            appointment_data = {
                "id": appt.id,
                "doctor_name": appt.doctor.name,
                "specialization": appt.doctor.department.dept_name if appt.doctor.department else "N/A",
                "date": str(appt.slot.date),
                "time": appt.slot.slots_time,
                "status": appt.status,
                "payment": appt.payment,
                "diagnosis": appt.treatment.diagnosis if appt.treatment else "N/A",
                "prescription": appt.treatment.prescription if appt.treatment else "N/A",
            }

            if appt.slot.date >= today and appt.status!="cancelled":
                upcoming_appointments.append(appointment_data)
            else:
                past_appointments.append(appointment_data)
        
        return jsonify({"message": "Appointment successfully cancelled",
            "upcoming_appointments": upcoming_appointments,
            "past_appointments": past_appointments
        }), 200
        

@auth.route("/doctor_dashboard",methods=['GET','PUT','POST','DELETE'])
@role_required("doctor")
def doc_dashboard():
    if request.method=='GET':
        user=get_jwt_identity()
        user=User.query.filter_by(email_id=user).one_or_none()
        
        appointment=Appoinment.query.filter_by(doc_id=user.id).all()
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        appointmentlist=[{
            "id": a.id,
            "patient_name": a.patient.name,
            "specialization": a.doctor.department.dept_name if a.doctor.department else "N/A",
            "date": str(a.slot.date),
            "time": a.slot.slots_time,
            "treatment_id": a.treatment.id if a.treatment else None,
            "status": a.status,
            "payment": a.payment,
            "diagnosis": a.treatment.diagnosis if a.treatment else "N/A",
            "prescription": a.treatment.prescription if a.treatment else "N/A",
            "notes": a.treatment.notes if a.treatment else "N/A"
            
        } for a in appointment if a.patient.is_active==True and a.doc_id==user.id and a.status !="cancelled" and a.status!="completed"]
        
        patientlist=[{
            "id":p.patient.id,
            "name":p.patient.name,
            "gender":p.patient.gender,
            "email_id":p.patient.email_id,
            "age":p.patient.age
            
        }for p in appointment if p.patient.is_active==True and p.doc_id==user.id]
        
        cur_user={
            "id": user.id,
            "name": user.name
        }
        
        return jsonify({"appointmentlist": appointmentlist,
                        "patientlist": patientlist,
                        "user": cur_user
                            }), 200
        
    elif request.method == 'PUT':
    
        data = request.get_json()
        app_id = data.get("id")
        status = data.get("status")
        treatment_id = data.get("treatment_id")

        appointment = Appoinment.query.filter_by(id=app_id).one_or_none()
  
        if status:
            if status == "completed":
                treatment = Treatment.query.filter_by(appoinment_id=app_id).one_or_none()
                if not treatment or appointment.id != treatment.appoinment_id:
                    return jsonify({"message": "Cannot complete appointment without treatment"}), 400
                appointment.status = status
                db.session.commit()
                
            elif status =="cancelled":
                appointment.status = status
                db.session.commit()
                return jsonify({"message": 'Appointment cancelled successfully'}), 200
            

    
        if treatment_id:
            treatment = Treatment.query.filter_by(id=treatment_id).one_or_none()
            if treatment:
                treatment.diagnosis = data.get("diagnosis", treatment.diagnosis)
                treatment.prescription = data.get("prescription", treatment.prescription)
                treatment.notes = data.get("notes", treatment.notes)
                
        def create_slots_for_doctor(doc_id, date, start_time, end_time):
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            start_dt = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H:%M') - timedelta(minutes=1)

            current = start_dt
            while current < end_dt:
                slot_start = current
                slot_end = current + timedelta(minutes=20)
                slot_time = f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                existing_slot = Slots.query.filter_by(
                    date=date_obj, slots_time=slot_time, user_id=doc_id
                ).first()
                if not existing_slot:
                    slot = Slots(
                        date=date_obj,
                        slots_time=slot_time,
                        is_booked=False,
                        user_id=doc_id
                    )
                    db.session.add(slot)
                current += timedelta(minutes=20)

   
        available_dates = data.get("available_dates", [])
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        userr=get_jwt_identity()
        user=User.query.filter_by(email_id=userr).one_or_none()

        if available_dates and start_time and end_time:
         
            old_slots = {
                s.date.strftime('%Y-%m-%d')
                for s in Slots.query.filter_by(user_id=user.id).all()
            }
          
            new_dates = set(available_dates) - old_slots
            for date in new_dates:
                create_slots_for_doctor(user.id, date, start_time, end_time)

        db.session.commit()
        return jsonify({"message": "Slots created Successfully"}), 200

    
    elif request.method=='POST':
        appoinment_id=request.json.get("appoinment_id")
        diagnosis=request.json.get("diagnosis")
        prescription=request.json.get("prescription")
        notes=request.json.get("notes")
        
        new_treatment=Treatment(
            appoinment_id=appoinment_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
    )
        db.session.add(new_treatment)
        appointment=Appoinment.query.filter_by(id=appoinment_id).one_or_none()
        appointment.status="completed"
        db.session.commit()
        return jsonify({"message": "Successfully completed the treatment of the patient"}), 200
    
    
@auth.route("/doctor_profile", methods=['GET', 'PUT', 'DELETE'])
@role_required("doctor")
def doc_profile():
    if request.method == "GET":
        user = User.query.get(current_user.id)
        return jsonify({
            "formData": {
                "id": user.id,
                "name": user.name,
                "gender": user.gender,
                "email_id": user.email_id,
                "age": user.age,
                "fees": user.fees
            }
        })

    elif request.method == 'PUT':
        data = request.get_json()
        user = User.query.get(current_user.id)

        if not user:
            return jsonify({"message": "User not found"}), 404

       
        new_email_id = data.get("email_id")
        if new_email_id and new_email_id != user.email_id:
            existing_user = User.query.filter_by(email_id=new_email_id).first()
            if existing_user:
                return jsonify({"message": "Email ID already exists"}), 409

        
        user.email_id = data.get("email_id", user.email_id)
        user.name = data.get("name", user.name)
        user.age = data.get("age", user.age)
        user.gender = data.get("gender", user.gender)
        user.password = data.get("password", user.password)
        user.fees = data.get("fees", user.fees)

        
        def create_slots_for_doctor(doc_id, date, start_time, end_time):
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            
            start_dt = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H:%M') - timedelta(minutes=1)

            current = start_dt
            while current < end_dt:
                slot_start = current
                slot_end = current + timedelta(minutes=20)
                slot_time = f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                
               
                existing_slot = Slots.query.filter_by(
                    date=date_obj, slots_time=slot_time, user_id=doc_id
                ).first()
                if not existing_slot:
                    slot = Slots(
                        date=date_obj,
                        slots_time=slot_time,
                        is_booked=False,
                        user_id=doc_id
                    )
                    db.session.add(slot)
                current += timedelta(minutes=20)

       
        available_dates = data.get("available_dates", [])
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if available_dates and start_time and end_time:
            
            old_slots = {
                s.date.strftime('%Y-%m-%d')
                for s in Slots.query.filter_by(user_id=user.id).all()
            }
            
            new_dates = set(available_dates) - old_slots
            for date in new_dates:
                create_slots_for_doctor(user.id, date, start_time, end_time)

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    elif request.method == "DELETE":
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"}), 200
    
@auth.route("/doctor_patient",methods=['GET','PUT','POST'])
@role_required("doctor")
def doctor_patient():
    current_user=get_jwt_identity()
    user=User.query.filter_by(email_id=current_user).one_or_none()
    if request.method=='GET':
        
        appointments=Appoinment.query.filter_by(doc_id=user.id).all()
        
        patientslist=[{
            "id":p.patient.id,
            "age":p.patient.age,
            "gender":p.patient.gender,
            "email_id":p.patient.email_id,
            "patient_status":p.patient.is_active,
            "name":p.patient.name,
            "date":str(p.slot.date),
            "time":p.slot.slots_time,
            "status":p.status,
            "payment":p.payment,
            "diagnosis": p.treatment.diagnosis if p.treatment else "N/A",
            "prescription": p.treatment.prescription if p.treatment else "N/A",
            "notes": p.treatment.notes if p.treatment else "N/A"
        }for p in appointments if p.doc_id==user.id and p.patient.is_active==1 ]
        
        seen_ids = set()
        patientlist = []
        for i in patientslist:
            if i["id"] not in seen_ids:
                patientlist.append(i)
                seen_ids.add(i["id"])

        return jsonify({"patientlist":patientlist}), 200
    

@auth.route("/patient_profiledoc/<int:id>",methods=['GET','PUT','POST'])
@role_required("doctor")
def patient_doc(id):
    if request.method=='GET':
        user=User.query.filter_by(id=id).one_or_none()
        appointments=Appoinment.query.filter_by(patient_id=id).all()
        
        appointmentlist=[{
            "id":p.id,
            "age":p.patient.age,
            "gender":p.patient.gender,
            "email_id":p.patient.email_id,
            "patient_status":p.patient.is_active,
            "name":p.patient.name,
            "date":str(p.slot.date),
            "time":p.slot.slots_time,
            "status":p.status,
            "payment":p.payment,
            "treatment_id":p.treatment.id if p.treatment else "N/A",
            "diagnosis": p.treatment.diagnosis if p.treatment else "N/A",
            "prescription": p.treatment.prescription if p.treatment else "N/A",
            "notes": p.treatment.notes if p.treatment else "N/A"
        }for p in appointments]
        patient={
            "id":id,
            "name":user.name,
            "email_id":user.email_id,
            "age":user.age,
            "gender":user.gender
        }
        
        return jsonify({"appointmentlist":appointmentlist,
                        "patient":patient})
    elif request.method=='POST':
        appoinment_id=request.json.get("appoinment_id")
        diagnosis=request.json.get("diagnosis")
        prescription=request.json.get("prescription")
        notes=request.json.get("notes")
        
        new_treatment=Treatment(
            appoinment_id=appoinment_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes 
            )
        db.session.add(new_treatment)
        appointment=Appoinment.query.filter_by(id=appoinment_id).one_or_none()
        appointment.status="completed"
        db.session.commit()
        return jsonify({"message": "Successfully completed the treatment of the patient"}), 200
    
    elif request.method=='PUT':
        data=request.get_json()
        treatment_id=data.get("treatment_id")
        treatment=Treatment.query.filter_by(id=treatment_id).one_or_none()
        
        if not treatment:
            return jsonify({"message": "Patient isn't checked"}), 400
        
        treatment.diagnosis=data.get("diagnosis",treatment.diagnosis)
        treatment.prescription=data.get("prescription",treatment.prescription)
        treatment.notes=data.get("notes",treatment.notes)
        
        db.session.commit()
        return jsonify({"message": "Patient treatment updated successfully"}), 200
    
    
@auth.route('/export_csv')
@jwt_required()
def start_download():
    email_id=get_jwt_identity()
    result=csv_report.delay(email_id)
    return jsonify({
        "id": result.id,
        "result": result.result
    }), 202


@auth.route('/api/report/status/<task_id>')
def check_status(task_id):
    result = AsyncResult(task_id)
    
    if result.state == 'PENDING':
        return jsonify({"status": "pending"})
    elif result.state == 'FAILURE':
        return jsonify({"status": "failed"})
    elif result.state == 'SUCCESS':
        filename = result.result
        return jsonify({
            "status": "success",
            "filename": filename
        })
    else:
        return jsonify({"status": result.state})
    
@auth.route('/api/report/get_file/<filename>')
def get_file(filename):
    file_path = os.path.join("static", filename)
    if os.path.exists(file_path):
        return send_from_directory('static', filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404
    
@auth.route('/api/send_mail')
def send_mail():
    result = month_report.delay()
    return{
        
        "message": result.result
        
    }

@auth.route('/api/daily_remainder', methods=['GET', 'POST'])
@jwt_required()
def daily_mail():
    email_id=get_jwt_identity()
    user=User.query.filter_by(email_id=email_id).one_or_none()
    
    now = datetime.utcnow()
    in_24_hours = now + timedelta(hours=24)
    upcoming_appointment= Appoinment.query.filter_by(patient_id=user.id).all()
    upcoming_appointments = [i for i in upcoming_appointment if i.doctor.is_active==1]
    for i in upcoming_appointments:

        start_time_str = i.slot.slots_time.split(" - ")[0]  
        
        
        slot_time = datetime.strptime(f" {i.slot.date} {start_time_str}", "%Y-%m-%d %H:%M")
        
        if now <= slot_time <= in_24_hours and i.status=='booked':
            result = daily_remainder.delay(user.name, i.doctor.name, slot_time, i.slot.date)

    return jsonify({"message": "Daily remainder sent"})
