import { createWebHistory, createRouter } from "vue-router";
import Home from "./components/Home.vue";
import register from "./components/register.vue";
import admin_dashboard from "./components/admin_dashboard.vue"
import patients from "./components/patients.vue"
import doctors from "./components/admin_doctor.vue"
import admin_department from "./components/department.vue"
import patient_dashboard from "./components/patient_dashboard.vue"
import patient_navbar from "./components/patient_navbar.vue"
import patient_doctor from "./components/patient_doctor.vue"
import patient_profile from "./components/patient_profile.vue"
import patient_appointment  from "./components/patient_appointment.vue"
import doctor_profile from "./components/doctor_profile.vue"
import doctor_dashboard from "./components/doctor_dashboard.vue"
import doctor_patient from "./components/doctor_patient.vue"
import patient_profiledoc from "./components/patient_profiledoc.vue"
import admin_appointment from "./components/admin_appointments.vue";

const routes=[
    {path:"/", component: Home},
    {path:"/register", component: register},
    {path:"/admin_dashboard", component: admin_dashboard},
    {path:"/admin_patients",component: patients},
    {path:"/admin_doctors",component: doctors},
    {path:"/admin_department",component: admin_department},
    {path:"/patient_dashboard",component: patient_dashboard},
    {path:"/patient_navbar",component: patient_navbar},
    {path:"/patient_doctor",component: patient_doctor},
    {path:"/patient_profile",component: patient_profile},
    {path:"/patient_appointment",component: patient_appointment},
    {path:"/doctor_profile",component: doctor_profile},
    {path:"/doctor_dashboard",component: doctor_dashboard},
    {path:"/doctor_patient",component: doctor_patient},
    {path:"/patient_profiledoc/:id",component: patient_profiledoc, name: "patient_profiledoc", props: true},
    {path:"/admin_appointment",component: admin_appointment}

]

export const router= createRouter({
    history:createWebHistory(),
    routes:routes
})