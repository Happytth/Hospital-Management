<template>
  <div class="doctors-page">
    <patient_navbar @search="doSearch" />

    <div class="container mt-5">
      <div class="table-wrapper shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle custom-table">
            <thead>
              <tr>
                <th scope="col" class="text-center">Name</th>
                <th scope="col" class="text-center">Department</th>
                <th scope="col" class="text-center">Status</th>
                <th scope="col" class="text-center">Fees</th>
                <th scope="col" class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(doctor, index) in doctorsList" :key="index">
                <td class="fw-semibold text-center">{{ doctor.name }}</td>
                <td class="text-capitalize text-center">{{ doctor.dept_name }}</td>
                <td class="text-capitalize text-center">{{ doctor.gender }}</td>
                <td class="text-capitalize text-center">{{ doctor.fees }}</td>
                <td class="text-center">

                  <button
                    class="btn btn-sm ghost-btn btn-info-outline me-2"
                    data-bs-toggle="modal"
                    data-bs-target="#infoModal"
                    @click="viewInfo(doctor)"
                  >
                    <i class="bi bi-info-circle me-1"></i> Info
                  </button> 

                  <button
                    class="btn btn-sm ghost-btn btn-book-outline me-1"
                    data-bs-toggle="modal"
                    data-bs-target="#addModal"
                    @click="bookappointment(doctor)"
                  >
                    <i class="bi bi-plus-circle me-1"></i> Book
                  </button> 
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
          <li class="list-group-item"><strong>Department:</strong> {{ formData.dept_name }}</li>
          <li class="list-group-item"><strong>Fees:</strong> {{ formData.fees }}</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<!-- booking modal -->
<div class="modal fade" id="addModal" tabindex="-1" aria-labelledby="addModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="addModalLabel">Book Appointment</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">

        <div v-if="!selectedDoctor || selectedDoctor.slots.length === 0" class="text-center text-muted">
          No slots available for this doctor
        </div>

        <form v-else @submit.prevent="bookinfo">
          <div class="mb-3">
            <label class="form-label">Select a Slot</label>
            <div class="d-flex flex-wrap gap-2">
              <div v-for="(slot, index) in selectedDoctor.slots" :key="index" class="form-check" >
                <input
                  class="form-check-input"
                  type="radio"
                  :id="'slot' + index"
                  :value="slot.id"
                  v-if="!slot.is_booked"
                  v-model="formData.selected_slot"
                  required
                />
                <label class="form-check-label" v-if="!slot.is_booked" :for="'slot' + index">
                  {{ formatDate(slot.date) }} - {{ slot.slots_time }}
                </label>
              </div>
            </div>
          </div>

          <div class="text-center">
            <button type="submit" class="btn btn-primary w-100">Confirm Booking</button>
          </div>
        </form>

      </div>
    </div>
  </div>
</div>

</div>
</template>

<script>
import patient_navbar from "./patient_navbar.vue";
import axios from "axios";

export default {
  name: "patient_doctor",
  components: { patient_navbar },
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
        dept_name: ""
      },
      departmentList: [],
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
      this.departmentList.forEach(d => {
        map[d.id] = d.dept_name;
      });
      return map;
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
        const res = await axios.get("http://127.0.0.1:5000/auth/patient_doctor", {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.doctorsList = res.data.doctorsList;
        this.departmentList = res.data.departmentList;
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
        department_id: doctor.department_id,
        fees: doctor.fees,
        dept_name: doctor.dept_name
      };
    },
    bookappointment(doctor) {
      this.selectedDoctor = doctor;
      this.formData = {
        doctor_id: doctor.id,
        selected_slot: null
      };
    },
    async bookinfo() {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/auth/patient_doctor",
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
