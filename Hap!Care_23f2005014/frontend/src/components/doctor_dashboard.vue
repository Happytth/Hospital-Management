<template>
  <div class="doctors-page">
   
    <doctor_navbar @search="doSearch" />
    <div class="container ">

      <div class="mt-4 mb-5">
        <p style="font-family: Verdana, Geneva, Tahoma, sans-serif; font-weight: 700;" 
           class="text-dark d-flex justify-content-start display-6">
          {{ user.name }}'s Dashboard
        </p>
        <small class="text-secondary fs-4 ">
          Manage your appointments, patients, and availability with ease
        </small>
      </div>

      <div class="row g-4">

        <div class="col-lg-8">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-primary text-white fw-bold">
              <i class="bi bi-calendar-check me-2"></i> Upcoming Appointments
            </div>
            <div class="card-body p-0">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="ms-4">Patient</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th class="px-4">Status</th>
                    <th class="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody class="p-2">
                  <tr v-for="(appt, index) in appointmentlist" :key="index">
                    <td class="fw-semibold">{{ appt.patient_name }}</td>
                    <td>{{ appt.date }}</td>
                    <td>{{ appt.time }}</td>
                    <td>
                      <span
                        class="badge rounded-pill px-3 py-2"
                        :class="{
                          'bg-success': appt.status === 'completed',
                          'bg-danger': appt.status === 'cancelled',
                          'bg-warning text-dark': appt.status === 'booked'
                        }"
                      >
                        {{ appt.status }}
                      </span>
                    </td>
                    <td class="text-center">
                      <button
                        class="btn btn-sm btn-outline-success me-2"
                        @click="markStatus(index, 'completed')"
                      >
                        <i class="bi bi-check-circle me-1"></i> Complete
                      </button>
                      
                      <button
                        class="btn btn-sm btn-outline-success"
                        @click="markStatus(index, 'booked')"
                        v-if="appt.status==='cancelled'"
                      >
                        <i class="bi bi-check-circle me-1"></i> Booked
                      </button>

                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="markStatus(index, 'cancelled')"
                        v-else
                      >
                        <i class="bi bi-x-circle me-1"></i> Cancel
                      </button>
                    </td>
                  </tr>
                  <tr v-if="appointmentlist.length === 0">
                    <td colspan="5" class="text-center text-muted py-3">
                      No appointments scheduled this week.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>


        <div class="col-lg-4">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-primary text-white fw-bold">
              <i class="bi bi-people me-2"></i> My Patients
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between align-items-center text-dark">
                <span class="fw-bold">Patients</span>
                <span class="fw-bold">Treatment</span> 
              </li>
              <li
                v-for="(patient, i) in appointmentlist"
                :key="i"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <span class="fw-semibold">{{ patient.patient_name }}</span>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="selectPatient(patient)"
                  data-bs-toggle="modal"
                  data-bs-target="#historyModal"
                  v-if="patient.status==='completed'"
                >
                  <i class="bi bi-pencil-square me-1"></i> Update
                </button>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="selectPatient(patient)"
                  data-bs-toggle="modal"
                  data-bs-target="#historyModal"
                  v-else-if="patient.status !== 'cancelled'"
                >
                  <i class="bi bi-pencil-square me-1"></i> Checkup
                </button>
              </li>
              <li v-if="patientlist.length === 0" class="list-group-item text-muted text-center text-muted py-4" colspan="5" >
                <i class="bi bi-emoji-frown fs-4 d-block mb-2"></i>
                No appointments found.
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Availability -->
      <div class="card shadow-sm border-0 mt-4">
        <div class="card-header bg-primary text-white fw-bold">
          <i class="bi bi-clock-history me-2"></i> Provide Availability (Next 7 Days)
        </div>
        <div class="card-body">
        <div class="col-md-12">
                <label class="form-label">Select Available Dates</label>
                <div class="d-flex flex-wrap gap-2">
                  <div v-for="day in next7Days" :key="day.value" class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="day.value"
                      :value="day.value"
                      v-model="formData.available_dates"
                    />
                    <label class="form-check-label" :for="day.value">
                      {{ day.label }}
                    </label>
                  </div>
                </div>
              </div>

              <div class="row mb-4 mt-2">
                <div class="col-md-6">
                  <label class="form-label">Start Time</label>
                  <input v-model="formData.start_time" type="time" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">End Time</label>
                  <input v-model="formData.end_time" type="time" class="form-control" />
                </div>
              </div>

              <button class="btn btn-primary w-100" type="submit" @click="updateAvailability">
                  <i class="bi bi-save me-1"></i> Save Changes
                </button>
        </div>
      </div>
      
    </div>

 
    <div
      class="modal fade"
      id="historyModal"
      tabindex="-1"
      aria-hidden="true"
      ref="historyModal"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="bi bi-journal-medical me-2"></i> Update History - {{ selectedPatient?.patient_name }}
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
              data-bs-dismiss="modal"
            >
              <i class="bi bi-save me-1"></i> Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import doctor_navbar from "./doctor_navbar.vue";

export default {
  name: "doctor_dashboard",
  components: { doctor_navbar },
  data() {
    return {
      appointmentlist: [],
      patientlist: [],
      selectedPatient: null,
      token: "",
      availability: [],     
      user: {},
      formData: {
        id: "",
        diagnosis: "",
        prescription: "",
        notes: "",
        appoinment_id:"",
        start_time:"",
        end_time:"",    
        available_dates:[]
      }
    };
  },
    computed: {
    next7Days() {
      const days = [];
      const today = new Date();
      for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        days.push({
          value: date.toISOString().split("T")[0], 
          label: date.toDateString(),
        });
      }
      return days;
    },
  },
  watch: {
    "formData.available_dates"(newVal) {
      console.log("Selected dates:", newVal);
    },
  },
  mounted() {
    this.loadtoken();
    this.loadappointments();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);
  },
  methods: {
    loadtoken() {
      const token = localStorage.getItem("token");
      if (token) {
        this.token = token;
      }
    },
    async loadappointments() {
      await axios.get("http://127.0.0.1:5000/auth/doctor_dashboard", {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      }).then(res => {
        if (res.status == 200) {
          this.appointmentlist = res.data.appointmentlist;
          this.patientlist = res.data.patientlist;
          this.user = res.data.user;
          const data = res.data.formData;
          this.formData = {
            ...this.formData,
            ...data,
            available_dates: Array.isArray(data.available_dates)
              ? data.available_dates
              : (() => {
                  try {
                    return JSON.parse(data.available_dates || "[]");
                  } catch {
                    return [];
                  }
                })(),
          };
        }
      })
    },
    markStatus(index, status) {
      const appointmentid = this.appointmentlist[index].id;
      axios.put("http://127.0.0.1:5000/auth/doctor_dashboard", {
        id: appointmentid,
        status: status
      }, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      }).then(res => {
        if (res.status == 200) {
          alert(res.data.message);
          this.appointmentlist[index].status = status;
          this.loadappointments();
        }
      }).catch(err => {
        alert(err.response.data.message);
      })
    },
    selectPatient(patient) {
      this.selectedPatient = patient;
      this.formData = {
        id: patient.treatment_id || "",
        diagnosis: patient.treatment?.diagnosis || "",
        prescription: patient.treatment?.prescription || "",
        notes: patient.treatment?.notes || "",
        appoinment_id:patient.id
      }
    },
    addinfo() {
      axios.post("http://127.0.0.1:5000/auth/doctor_dashboard", this.formData, {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      }).then(res => {
        if (res.status == 200) {
          alert(res.data.message);
          this.loadappointments();
        }
      }).catch(err => {
        alert(err.response.data.message);
      })
    },
    saveHistory() {
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

  axios.put("http://127.0.0.1:5000/auth/doctor_dashboard", payload, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  }).then(res => {
    if (res.status === 200) {
      alert(res.data.message);
      this.loadappointments();
    }
  }).catch(err => {
    alert(err.response?.data?.message || err.message);
  });
},
    updateAvailability() {
  axios.put("http://127.0.0.1:5000/auth/doctor_dashboard", {
    available_dates: this.formData.available_dates,
    start_time: this.formData.start_time,
    end_time: this.formData.end_time
  }, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  }).then(res => {
    alert(res.data.message);
    this.loadappointments();
  }).catch(err => {
    alert(err.response?.data?.message || err.message);
  });
},
    doSearch(query) {
      console.log("Search from navbar:", query);
    },
  },
};
</script>

<style scoped>
.doctors-page{
  min-height: 110vh;
  background: linear-gradient(115deg, #e5f6fe 18%, #f8fbff 48%, #c9e7fd 71%, #f1f8ff 100%);
}

.card {
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(15, 97, 219, 0.08);
  border: none;
}

.card-header {
  background: linear-gradient(90deg, #1769aa 0%, #5fbbfa 100%);
  color: white;
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: 0.05em;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  box-shadow: 0 2px 8px rgba(45, 92, 140, 0.12);
  display: flex;
  align-items: center;
}

.card-header i {
  background: #e4f2ff;
  color: #1769aa;
  border-radius: 50%;
  padding: 0.5rem;
  font-size: 1.3rem;
  margin-right: 0.6rem;
}

.table td,
.table th {
  vertical-align: middle;
  transition: background 0.15s;
}

.table-hover tbody tr:hover {
  background-color: #e9f5fd;
}

.badge {
  font-size: 0.91rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  border-radius: 1em;
  box-shadow: 0 2px 6px rgba(150,200,250,0.14);
}

.btn-outline-success, .btn-outline-danger, .btn-outline-primary {
  border-radius: 0.4rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.modal-content {
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(21, 60, 170, 0.13);
}

.modal-header {
  background: linear-gradient(90deg, #1769aa 0%, #5fbbfa 100%);
  color: white;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}

.modal-footer {
  background: #f4f9ff;
  border-bottom-left-radius: 1rem;
  border-bottom-right-radius: 1rem;
}

.list-group-item {
  cursor: pointer;
  padding-top: 0.68em;
  padding-bottom: 0.68em;
  border-radius: 0.4em !important;
  transition: background 0.18s;
}

.list-group-item:hover {
  background-color: #e3f0fa !important;
  color: #1769aa !important;
}

.list-group-item.text-dark:hover {
  background-color: inherit;
}

.form-control,
.form-check-input {
  border-radius: 0.5em;
}

.form-label {
  font-weight: 600;
  color: #178de8;
  margin-bottom: 0.4em;
}

.fs-4 {
  font-weight: 500;
  font-size: 1.15rem;
}

</style>
