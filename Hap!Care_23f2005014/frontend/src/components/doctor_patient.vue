<template>
  <div class="doctors-page">
    <doctor_navbar @search="doSearch" />

    <div class="container mt-5">
      <div class="table-wrapper shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle custom-table">
            <thead>
              <tr>
                <th scope="col" class="text-center">Name</th>
                <!-- <th scope="col" class="text-center">Department</th> -->
                <th scope="col" class="text-center">Email</th>
                <th scope="col" class="text-center">Age</th>
                <th scope="col" class="text-center">Gender</th>
                <th scope="col" class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(patient, index) in patientlist" :key="index">
                <td class="fw-semibold text-center">{{ patient.name }}</td>
                <!-- <td class="text-capitalize text-center">{{ departmentMap[patient.department_id] }}</td> -->
                 <td class="text-capitalize text-center">{{ patient.email_id }}</td>
                 <td class="text-capitalize text-center">{{ patient.age }}</td>
                <td class="text-capitalize text-center">{{ patient.gender }}</td>
                <td class="text-center">

                  <button
                    class="btn btn-sm ghost-btn btn-info-outline me-2"
                    data-bs-toggle="modal"
                    data-bs-target="#infoModal"
                    @click="viewInfo(patient)"
                  >
                    <i class="bi bi-info-circle me-1"></i> Info
                  </button> 

                  <RouterLink
                    class="btn btn-sm ghost-btn btn-book-outline me-1"
                     :to="{name : 'patient_profiledoc', params: {id: patient.id} }">
                    <i class="bi bi-archive me-1"></i> History
                  </RouterLink> 
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
          <li class="list-group-item"><strong>Email:</strong> {{ formData.email_id }}</li>
          <li class="list-group-item"><strong>Name:</strong> {{ formData.name }}</li>
          <li class="list-group-item"><strong>Gender:</strong> {{ formData.gender }}</li>
          <li class="list-group-item"><strong>Age:</strong> {{ formData.age }}</li>
          <!-- <li class="list-group-item"><strong>Department:</strong> {{ selectedDepartment ? selectedDepartment.dept_name : '' }}</li> -->
        </ul>
      </div>
    </div>
  </div>
</div>

</div>
</template>

<script>
import doctor_navbar from "./doctor_navbar.vue";
import axios from "axios";

export default {
  name: "doctor_patient",
  components: { doctor_navbar },
  data() {
    return {
      patientlist: [],
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
        doctor_id: null
      },
      selectedDoctor: null
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.query) return this.patientlist;
      const q = this.query.toLowerCase();
      return this.patientlist.filter((p) => p.name.toLowerCase().includes(q));
    },
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
        const res = await axios.get("http://127.0.0.1:5000/auth/doctor_patient", {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.patientlist = res.data.patientlist;
      } catch (err) {
        console.error(err);
      }
    },
    viewInfo(doctor) {
      this.formData = {
        id: doctor.id,
        email_id: doctor.email_id,
        age: doctor.age,
        gender: doctor.gender,
        name: doctor.name,
        department_id: doctor.department_id
      };
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
     
      const d = new Date(dateStr);
      if (!isNaN(d)) {
        return d.toDateString(); 
      }
      
      return dateStr.replace(/ 00:00:00.*$/, "");
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
</style>