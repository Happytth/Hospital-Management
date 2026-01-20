<script>
import axios from 'axios'
import Navbar from './admin_navbar.vue'
import GenderChart from './GenderChart.vue'
import Appointments_Status from './Appointments_Status.vue'
import Docs_in_Dept from './Docs_in_Dept.vue'
export default{
  components: {
    Navbar,
    GenderChart,
    Appointments_Status,
    Docs_in_Dept
  },
    data(){
        return{
           token:"",
           user_count:0,
           doctor_count:0,
           total_appointments:0,
           chart_url:"",
           cancelled_appointments:0,
           gender_data: { male: 0, female: 0, other: 0 },
           appointments: {booked:0, completed:0, cancelled:0},
           departments:[]
        }
    },mounted(){
        this.loadtoken();
        this.loadthings();
        setTimeout(() => {
    document.body.classList.remove('modal-open');
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
  }, 50);
    },
    methods:{
        loadtoken(){
            const token= localStorage.getItem("token");
           
            if (token){
            this.token= token;
        }
   },
        loadthings(){
            const response = axios.get('http://127.0.0.1:5000/auth/admin_dashboard',{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response.then(res => {
                this.user_count=res.data.user_count;
                this.doctor_count=res.data.doctor_count;
                this.total_appointments=res.data.total_appointments;
                this.cancelled_appointments=res.data.cancelled_appointments;
                // this.chart_url = `${res.data.chart_url}?t=${Date.now()}`;
                this.gender_data = res.data.gender_data || { male: 0, female: 0, other: 0 };
                this.appointments = res.data.appointments || { booked:0, completed:0, cancelled:0 };
                this.departments = res.data.departments

            })
            .catch(err => {console.log("Error")})
        },
        logout(){
            this.token=null;
            localStorage.clear();
            this.$router.push('/');
            setTimeout(() => {
    document.body.classList.remove('modal-open');
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
  }, 100);
        }
    }
}
</script>

<template>

<div v-if="token">
<Navbar @search="doSearch" />
<div class="dashboardnew">

<div class="container-fluid p-4">
  <div class="dashboard-header">Dashboard Analytics</div>
  <div class="row g-4">

    <div class="col-lg-3 col-md-4 col-sm-6">
      <div class="card text-center p-3">
        <div class="card-body">
          <div class="card-title">Total patients</div>
          <div class="kpi-value">{{ user_count }}</div>
          <div class="kpi-trend trend-up">↑ 2</div>
          <small class="text-muted">vs previous 7 days</small>
        
        
        </div>
      </div>
      <div class="card text-center p-3 mt-3">
        <div class="card-body">
          <div class="card-title">Total Doctors</div>
          <div class="kpi-value">{{ doctor_count }}</div>
          <div class="kpi-trend trend-up">↑ 8%</div>
          <small class="text-muted">vs previous 7 days</small>
        </div>
      </div>
      <div class="card text-center p-3 mt-3">
        <div class="card-body">
          <div class="card-title">Total Appointments</div>
          <div class="kpi-value">{{ total_appointments }}</div>
          <div class="kpi-trend trend-down">↑ 1%</div>
          <small class="text-muted">vs previous 7 days</small>
        </div>
      </div>
      <div class="card text-center p-3 mt-3">
        <div class="card-body">
          <div class="card-title">Appointment Cancellations</div>
          <div class="kpi-value">{{ cancelled_appointments }}</div>
          <div class="kpi-trend trend-up">↑ 2</div>
          <small class="text-muted">vs previous 7 days</small>
        </div>
      </div>
    </div>

    <div class="col-lg-9 col-md-8">
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card p-3">
            <div class="card-body">
              <div class="card-title">Gender Distribution</div>
              <GenderChart :genderData="gender_data" />
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card p-3">
            <div class="card-body">
              <div class="card-title">Appointments</div>
              <Appointments_Status :appointment_data="appointments" />
            </div>
          </div>
        </div>
      </div>

      <div class="card p-3 mt-3">
        <div class="card-body">
          <div class="card-title">Doctors in Departments</div>
          <Docs_in_Dept :Docs_in_Dept="departments" />
        </div>
      </div>
    </div>
  </div>
</div>
</div>
</div>
<div v-else> <h1>Please Login to continue</h1> </div>


<div
  class="modal fade"
  id="logoutModal"
  tabindex="-1"
  aria-labelledby="logoutModalLabel"
  aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="logoutModalLabel">Confirm Logout</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"></button>
      </div>
      <div class="modal-body">
        Do you really want to log out?
      </div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-dismiss="modal">
          No
        </button>
        <button
          type="button"
          class="btn btn-danger"
          @click="logout">
          Yes
        </button>
      </div>
    </div>
  </div>
</div>

</template>



<style scoped>

.dashboardnew{
      background: linear-gradient(135deg, #f0f4ff, #567bca);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .card {
      border-radius: 12px;
      box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    }
    .card-title {
      font-weight: 600;
      font-size: 1.1rem;
      margin-bottom: 10px;
    }
    .kpi-value {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 5px;
    }
    .kpi-trend {
      font-size: 1rem;
      font-weight: 600;
    }
    .trend-up {
      color: #28a745; /* Bootstrap success green */
    }
    .trend-down {
      color: #dc3545; /* Bootstrap danger red */
    }
    .chart-img {
      max-height: 300px;
      object-fit: contain;
      width: 100%;
    }
    .dashboard-header {
      font-weight: 700;
      font-size: 2rem;
      margin-bottom: 25px;
      color: #212529;
    }

</style>