<template>
  <div class="doctors-page">
    <Navbar @search="doSearch" />

    <div class="container mt-5">
      

      <div class="table-wrapper shadow-sm">
        <div class="table-responsive">
          
<div class="d-flex justify-content-end mt-3  search-box ">
  <div style="border-radius: 22px; width: 280px;">
    
        <input
          type="text"
          v-model="query"
          class="form-control "
          style="max-width: 280px;"
          placeholder="Search by patient or doctor "
        />
        
        </div>
      </div>

          <table class="table table-hover align-middle custom-table">
            
            <thead>
              <tr>
                <th scope="col" class="text-center">Patient Name</th>
                <th scope="col" class="text-center">Doctor Name</th>
                <th scope="col" class="text-center">Date</th>
                <th scope="col" class="text-center">Slot</th>
                <th scope="col" class="text-center">Status</th>
                <th scope="col" class="text-center">Payment</th>
                <th scope="col" class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(doctor, index) in filteredAppointments" :key="index">
                <td class="fw-semibold text-center">{{ doctor.patient_name }}</td>
                <td class="fw-semibold text-center">{{ doctor.doctor_name }}</td>
                <td class="text-capitalize text-center">{{ doctor.date }}</td>
                <td class="text-capitalize text-center">{{ doctor.time }}</td>
                <td class="text-center">
                  <span :class="['badge', badgeClass(doctor.status)]">
                    {{ doctor.status }}
                  </span>
                </td>
                <td class="text-capitalize text-center">{{ doctor.payment }}</td>
                <td class="text-center">
                  <button
                    class="btn btn-sm ghost-btn btn-info-outline me-2"
                    data-bs-toggle="modal"
                    data-bs-target="#infoModal"
                    @click="viewInfo(doctor)"
                  >
                    <i class="bi bi-info-circle me-1"></i> Info
                  </button> 
                  <!-- <button
                    class="btn btn-sm ghost-btn btn-book-outline me-1"
                    data-bs-toggle="modal"
                    data-bs-target="#editModal"
                    @click="editappointment(doctor)"
                  >
                    <i class="bi bi-pencil-square me-1"></i> Edit
                  </button>  -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- info modal -->
    <div class="modal fade" id="infoModal" tabindex="-1" aria-labelledby="infoModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow-lg">
          <div class="modal-header">
            <h5 class="modal-title fw-bold" id="infoModalLabel">Doctor Information</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <ul class="list-group list-group-flush">
              <li class="list-group-item"><strong>Diagnosis:</strong> {{ formData.diagnosis }}</li>
              <li class="list-group-item"><strong>Prescription:</strong> {{ formData.prescription }}</li>
              <li class="list-group-item"><strong>Notes:</strong> {{ formData.notes }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>


    <!-- logout modal -->
    <div class="modal fade" id="logoutModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="logoutModalLabel">Confirm Logout</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Do you really want to log out?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              No
            </button>
            <button type="button" class="btn btn-danger" @click="logout">
              Yes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "./admin_navbar.vue";
import axios from "axios";

export default {
  name: "admin_appointment",
  components: { Navbar },
  data() {
    return {
      doctorsList: [],
      query: "",
      token: "",
      formData: {
        email_id: "",
        age: "",
        gender: "",
        name: "",
        password: "",
        department_id: "",
        selected_slot: null,
        doctor_id: null,
        id:""
      },
      appointmentlist: [],
      selectedDoctor: null
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.query) return this.doctorsList;
      const q = this.query.toLowerCase();
      return this.doctorsList.filter((p) => p.name.toLowerCase().includes(q));
    },
    departmentMap() {
      const map = {};
      this.appointmentlist.forEach(d => {
        map[d.id] = d.dept_name;
      });
      return map;
    },
    filteredAppointments() {
      if (!this.query) return this.appointmentlist;
      const q = this.query.toLowerCase();
      return this.appointmentlist.filter(a =>
        (a.patient_name || "").toLowerCase().includes(q) ||
        (a.doctor_name || "").toLowerCase().includes(q) ||
        (a.status || "").toLowerCase().includes(q) ||
        (a.date || "").toLowerCase().includes(q)
      );
    }
  },
  mounted() {
    this.loadToken();
    this.loadDoctors();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);
  },
  methods: {
    doSearch(value) {
      this.query = value;
    },
    loadToken() {
      const token = localStorage.getItem("token");
      if (token) {
        this.token = token;
      }
    },
    async loadDoctors() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/auth/admin_appointment", {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.doctorsList = res.data.doctorsList;
        this.appointmentlist = res.data.appointmentlist;
      } catch (err) {
        console.error(err);
      }
    },
    viewInfo(doctor) {
      this.formData = {
        diagnosis: doctor.diagnosis,
        prescription: doctor.prescription,
        notes: doctor.notes,
        gender: doctor.gender,
        name: doctor.name,
        department_id: doctor.department_id
      };
    },
    editappointment(doctor) {
      this.selectedDoctor = doctor;
      this.formData = {
        doctor_id: doctor.id,
        selected_slot: null,
        app_id:id
      };
    },
    async editinfo() {
      try {
        const res = await axios.post(
          "http://127.0.0.1:5000/auth/admin_appointment",
          {
            doctor_id: this.formData.doctor_id,
            selected_slot: this.formData.selected_slot
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
          }
        );
        if (res.status === 200) {
          alert("Appointment booked successfully!");
          this.loadDoctors();
        }
      } catch (err) {
        console.error(err);
        alert("Error booking appointment");
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const d = new Date(dateStr);
      if (!isNaN(d)) {
        return d.toDateString(); 
      }
      return dateStr.replace(/ 00:00:00.*$/, "");
    },
    badgeClass(status) {
      switch (status.toLowerCase()) {
        case 'completed':
          return 'bg-success text-white'; 
        case 'booked':
          return 'bg-primary text-white'; 
        case 'cancelled':
          return 'bg-danger text-white'; 
        default:
          return 'bg-secondary text-white'; 
      }
    },
    logout() {
      this.token = null;
      localStorage.clear();
      this.$router.push('/');
      setTimeout(() => {
        document.body.classList.remove('modal-open');
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
      }, 100);
    }
  }
};
</script>

<style scoped>
.doctors-page {
  min-height: 100vh;
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );
  font-family: "Poppins", sans-serif;
}

.table-wrapper {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
}

.custom-table thead th {
  text-align: center;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-bottom: 3px solid #dee2e6; 
}

.btn {
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
}
.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.ghost-btn {
  min-width: 90px;
  padding: 0 18px;
  height: 36px;
  font-size: 1rem;
  font-weight: 600;
  border: 2px solid transparent;
  background: transparent;
  border-radius: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, color 0.2s, background 0.2s, box-shadow 0.2s;
}
.btn-info-outline {
  color: #36b9cc;
  border-color: #36b9cc;
}
.btn-info-outline:hover,
.btn-info-outline:focus {
  background: #e6fafd;
  color: #2392a6;
  border-color: #36b9cc;
}
.btn-book-outline {
  color: #007bff;
  border-color: #007bff;
}
.btn-book-outline:hover,
.btn-book-outline:focus {
  background: #eaf5ff;
  color: #0056b3;
  border-color: #007bff;
}
.search-box input {
  border-radius: 20px;
  padding: 5px 12px;
  width: 230px;
  font-size: 0.9rem;
  overflow: hidden;
}
</style>
