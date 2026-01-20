<template>
<patient_navbar @search="doSearch" />
<div class="patients-page">
<div class="container-fluid py-4">

  <!-- Welcome Section -->
  <div class="mb-4 text-center">
    <h2 class="fw-bold">Welcome, {{ cur_user.name }}</h2>
    <p class="text-muted">Here’s an overview of your recent activities</p>
  </div>


 <div class="card mb-4 shadow-sm">
  <div class="card-header bg-primary text-white">
    <h5 class="mb-0">Upcoming Appointments</h5>
  </div>
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-light">
        <tr v-if="appointmentslist.length>0">
          <th>Doctor</th>
          <th>Department</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
        <tr v-else>
          No Upcoming Appointments
        </tr>
      </thead>
      <tbody>
        <tr v-for="(appointment, index) in appointmentslist" :key="index">
          <td class="fw-semibold">{{ appointment.doctor_name }}</td>
          <td>{{ appointment.department }}</td>
          <td>{{ appointment.slot.date }}</td>
          <td>{{ appointment.slot.slots_time }}</td>
          <td>
            <span
              class="badge"
              :class="appointment.status === 'Confirmed' ? 'bg-success' : 'bg-warning'" >
              {{ appointment.status }}
            </span>
          </td>
          <td>
            <button
              class="btn btn-sm btn-outline-danger"
              @click="cancelAppointment(index, 'cancelled')"
             
            >
              Cancel
            </button>

          </td>
        </tr>
        
      </tbody>
    </table>
  </div>
</div>



  <div class="card mb-4 shadow-sm">
  <div class="card-header bg-light">
    <h5 class="mb-0">Available Specializations / Departments</h5>
  </div>
  <div class="card-body">
    <div class="row g-4">
      <div
        class="col-6 col-md-4 col-lg-3"
        v-for="(dept,index) in departmentList"
        :key="index">
        <div class="dept-card p-4 text-center">
          <div class="dept-icon mb-3">
            <i class="bi bi-heart-pulse"></i>
          </div>
          <p class="dept-name mb-0">{{ dept.dept_name }}</p>
        </div>
      </div>
    </div>
  </div>
</div>


  <div class="card mb-4 shadow-sm">
  <div class="card-header bg-light py-2">
    <h6 class="mb-0">Available Doctors (Next 7 Days)</h6>
  </div>
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-6 col-lg-4" v-for="(doc,index) in doctorList" :key="index">
        <div class="card h-100 border-0 shadow-sm text-center rounded-3 hover-shadow">
          
          <!-- Doctor Image -->
          <div class="pt-3">
            <img src="https://cdn-icons-png.flaticon.com/512/8815/8815112.png"
                 alt="Doctor Photo"
                 class="rounded-circle border"
                 width="60" height="60">
          </div>
          
          <!-- Doctor Info -->
          <div class="card-body py-2">
            <h6 class="fw-bold mb-0">{{ doc.name }}</h6>
            <small class="text-muted">{{ doc.specialization || 'Specialization' }}</small>
            <div class="mt-1">
              <span class="badge bg-success me-1">Tue</span>
              <span class="badge bg-success me-1">Wed</span>
              <span class="badge bg-success">Fri</span>
            </div>
          </div>
          
          <!-- Button -->
          <div class="card-footer bg-white border-0 py-2">
            <RouterLink to="/patient_doctor" class="btn btn-sm btn-primary w-100 fw-semibold">
              Book Appointment
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>



 
</div>
</div>


</template>

<script>
import { RouterLink } from "vue-router";
import patient_navbar from "./patient_navbar.vue"
import axios from 'axios'
export default {
  name: "patient_dashboard",
  components:{ patient_navbar },
  data() {
    return {
      formData:{
        id:"",
        email_id:"",
        password:"",
        name:"",
        gender:"",
        age:"",
        is_active:""
      },
      token:"",
      appointmentslist:[],
      doctorList:[],
      patientList:[],
       cur_user:{
        id:"",
        email_id:"",
        password:"",
        name:"",
        gender:"",
        age:"",
        is_active:""
      },
      departmentList:[]
      
    }
  },
  mounted(){
    this.loadtoken();
    this.loadpatients();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);
  },
  computed:{
    filteredDoctors() {
      if (!this.selectedSpecialization) return this.doctors
      return this.doctors.filter(
        d => d.specialization === this.selectedSpecialization
      )
    }
  },
  methods: {
    loadtoken(){
     const token=localStorage.getItem("token");
      if (token){
      this.token=token;
    }
  },
  loadpatients(){
    axios.get("http://127.0.0.1:5000/auth/patient_dashboard",{
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }).then(res => {if (res.status==200){
      this.appointmentslist=res.data.appointmentslist;
      this.cur_user=res.data.cur_user;
      this.departmentList=res.data.departmentList;
      this.doctorList=res.data.doctorList
    }})
  },
  cancelAppointment(index, status) {
      const appointmentid = this.appointmentslist[index].id;
      axios.put("http://127.0.0.1:5000/auth/patient_dashboard", {
        id: appointmentid,
        status: status
      }, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      }).then(res => {
        if (res.status == 200) {
          this.loadpatients();
          alert(res.data.message);
          this.appointmentlist[index].status = status;
          
        }
      }).catch(err => {
        alert(err.response.data.message);
      })
    }    
    
    }
  }

</script>

<style scoped>

.patients-page{
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );

}
.content {
  margin-top: 60px;
  padding: 20px;
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(200px,1fr));
  gap: 20px;
}
.card {
  background: #fff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: center;
}
.card img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}
.dept-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.dept-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.12);
  cursor: pointer;
}
.dept-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto;
  border-radius: 50%;
  background: #e8f0ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #007bff;
}
.dept-name {
  font-weight: 600;
  text-transform: capitalize;
  font-size: 1rem;
}
.hover-shadow:hover {
  transform: translateY(-5px);
  transition: all 0.3s ease-in-out;
  box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15) !important;
}
</style>