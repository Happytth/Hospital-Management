<template>
    <div class="doctors-page">
  <doctor_navbar @search="doSearch" />
  
  <div class="container py-5">


    <div class="card mb-4 border-0 shadow-lg profile-card">
      <div class="card-body d-flex align-items-center">
        <img :src="patient.avatar || defaultAvatar" 
             class="rounded-circle profile-img me-4">
        <div>
          <h3 class="fw-bold mb-1 text-primary">{{ patient.name }}</h3>
          <p class="text-muted mb-1"><i class="bi bi-envelope me-1"></i> {{ patient.email_id }}</p>
          <div class="mt-2">
            <span class="me-2 badge bg-info text-dark px-3 py-2">
              <i class="bi bi-gender-ambiguous me-1"></i>{{ patient.gender }}
            </span>
            <span class="me-2 badge bg-secondary text-light px-3 py-2">
              <i class="bi bi-person me-1"></i>Age: {{ patient.age }}
            </span>
          </div>
        </div>
      </div>
    </div>


    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center shadow border-0 stat-card">
          <div class="card-body">
            <i class="bi bi-calendar-check text-primary fs-2 mb-2"></i>
            <h6 class="text-muted">Total Appointments</h6>
            <h2 class="fw-bold text-primary">{{ appointmentlist.length }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center shadow border-0 stat-card">
          <div class="card-body">
            <i class="bi bi-clipboard2-pulse text-success fs-2 mb-2"></i>
            <h6 class="text-muted">Completed</h6>
            <h2 class="fw-bold text-success">
              {{ appointmentlist.filter(a => a.status === 'completed').length }}
            </h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center shadow border-0 stat-card">
          <div class="card-body">
            <i class="bi bi-exclamation-triangle text-danger fs-2 mb-2"></i>
            <h6 class="text-muted">Cancelled</h6>
            <h2 class="fw-bold text-danger">
              {{ appointmentlist.filter(a => a.status === 'cancelled').length }}
            </h2>
          </div>
        </div>
      </div>
    </div>


    <div class="card shadow-lg border-0">
      <div class="card-header bg-gradient-primary text-white d-flex align-items-center">
        <i class="bi bi-journal-bookmark me-2 fs-5"></i>
        <h5 class="mb-0">Appointment History</h5>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover table-striped mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Slot</th>
              <th>Status</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Notes</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(appt, index) in appointmentlist" :key="index">
              <td><i class="bi bi-calendar-event me-1 text-primary"></i> {{ appt.date }}</td>
              <td>{{ appt.time }}</td>
              <td><span :class="badgeClass(appt.status)">{{ appt.status }}</span></td>
              <td>{{ appt.diagnosis || '—' }}</td>
              <td>{{ appt.prescription || '—' }}</td>
              <td>{{ appt.notes || '—' }}</td>
              <td> 
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="selectPatient(appt)"
                  data-bs-toggle="modal"
                  data-bs-target="#historyModal"
                  v-if="appt.status==='completed'"
                >
                  <i class="bi bi-pencil-square me-1"></i> Update
                </button>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="selectPatient(appt)"
                  data-bs-toggle="modal"
                  data-bs-target="#historyModal"
                  v-else-if="appt.status !== 'cancelled'"
                >
                  <i class="bi bi-pencil-square me-1"></i> Checkup
                </button>

              </td>
            </tr>
            <tr v-if="appointmentlist.length === 0">
              <td colspan="5" class="text-center text-muted py-4">
                <i class="bi bi-emoji-frown fs-4 d-block mb-2"></i>
                No appointments found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    </div>
  </div>


     <div class="modal fade" id="historyModal" tabindex="-1" aria-hidden="true" ref="historyModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="bi bi-journal-medical me-2"></i> Update History - {{ selectedPatient?.name }}
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Diagnosis</label>
              <textarea class="form-control" rows="2" v-model="formData.diagnosis" ></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Prescription</label>
              <textarea class="form-control" rows="2" v-model="formData.prescription" ></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Notes</label>
              <textarea class="form-control" rows="2" v-model="formData.notes" ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-light border" data-bs-dismiss="modal">
              Close
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="saveHistory" 
              v-if="selectedPatient && selectedPatient.status==='completed'" 
              data-bs-dismiss="modal"
            >
              <i class="bi bi-save me-1"></i> Update
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="addinfo" 
              v-else 
              data-bs-dismiss="modal" >
              <i class="bi bi-save me-1"></i> Save
            </button>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
import doctor_navbar from "./doctor_navbar.vue";
import axios from "axios";

export default {
  name: "patient_profiledoc",
  components: { doctor_navbar },
  props: ["id"],
  data() {
    return {
      defaultAvatar: "https://www.w3schools.com/howto/img_avatar.png",
      patient: {},
      appointmentlist: [],
      formData: {
        id:"",
        diagnosis: "",
        prescription: "",
        notes: "",
        appoinment_id: "",
        treatment_id: ""
      },
      token:"",
      selectedPatient:null
    };
  },
  mounted() {
    this.loadtoken();
    this.loadPatientData();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);

  },
  methods: {
    loadtoken(){
        const token=localStorage.getItem("token")
        if (token) {this.token=token;}
    },
    badgeClass(status) {
      if (status === "Completed") return "badge bg-success px-3 py-2";
      if (status === "Cancelled") return "badge bg-danger px-3 py-2";
      if (status === "Booked" || status === "Scheduled") return "badge bg-warning text-dark px-3 py-2";
      return "badge bg-secondary px-3 py-2";
    },
    async loadPatientData() {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/auth/patient_profiledoc/${this.id}`, {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        });
        this.patient = res.data.patient;
        this.appointmentlist = res.data.appointmentlist;
      } catch (err) {
        console.error("Error fetching patient data", err);
      }
    },selectPatient(appt) {
      this.selectedPatient = appt;
      this.formData = {
        id: appt.treatment_id || "",
        diagnosis: appt.treatment?.diagnosis || "",
        prescription: appt.treatment?.prescription || "",
        notes: appt.treatment?.notes || "",
        appoinment_id:appt.id
      }
    },
    addinfo() {
      axios.post(`http://127.0.0.1:5000/auth/patient_profiledoc/${this.id}`, this.formData, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      }).then(res => {
        if (res.status == 200) {
          alert(res.data.message);
          this.loadPatientData();
        }
      }).catch(err => {
        alert(err.response.data.message);
      })
    },saveHistory() {
  const payload = { treatment_id: this.formData.id };

  if (this.formData.diagnosis.trim() !== "") {
    payload.diagnosis = this.formData.diagnosis;
  }
  if (this.formData.prescription.trim() !== "") {
    payload.prescription = this.formData.prescription;
  }
  if (this.formData.notes.trim() !== "") {
    payload.notes = this.formData.notes;
  }

  axios.put(`http://127.0.0.1:5000/auth/patient_profiledoc/${this.id}`, payload, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  }).then(res => {
    if (res.status === 200) {
      alert(res.data.message);
      this.loadPatientData();
    }
  }).catch(err => {
    alert(err.response?.data?.message || err.message);
  });
}
  },

};
</script>

<style scoped>
.doctors-page{
  min-height: 100vh;
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );
}
.profile-card {
  background: linear-gradient(135deg, #f8fbff, #e9f2ff);
  border-left: 6px solid #0d6efd;
}
.profile-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 3px solid #0d6efd;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.stat-card {
  transition: transform 0.2s ease-in-out;
}
.stat-card:hover {
  transform: translateY(-4px);
}

.bg-gradient-primary {
  background: linear-gradient(90deg, #0d6efd, #007bff);
}
</style>
