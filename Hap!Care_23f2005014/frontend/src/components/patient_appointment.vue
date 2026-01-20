<template>
  <div class="patients-page">
    <patient_navbar @search="doSearch" />


    <div class="container-fluid py-4">
      <div class="card shadow-sm upcoming-card mb-4">
        <div class="card-header bg-primary text-white rounded-top">
          <h5 class="mb-0">Upcoming Appointments</h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>Date</th>
                  <th>Slot</th>
                  <th>Payment</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(appointment, index) in upcomingAppointments" :key="index">
                  <td class="fw-semibold">{{ appointment.doctor_name }}</td>
                  <td>{{ appointment.specialization }}</td>
                  <td>{{ appointment.date }}</td>
                  <td>{{ appointment.time }}</td>
                  <td v-if="appointment.payment==='done'">
                    <span class='badge bg-warning'>Completed</span>
                  </td>
                  <td v-else>
                    <button
                      class="btn btn-sm btn-outline-success" data-bs-toggle="modal" data-bs-target="#paymentModal"
                      @click="pay(appointment)">
                      Pay now
                    </button>
                  </td>

                  <td>
                    <span
                      class="badge"
                      :class="appointment.status === 'Confirmed' ? 'bg-success' : 'bg-warning'">
                      {{ appointment.status }}
                    </span>
                  </td>
                  <td>
                    <button
                      class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#cancelModal"
                      @click="cancelAppointment(appointment)">
                      Cancel
                    </button>
                  </td>
                </tr>
                <tr v-if="upcomingAppointments.length === 0">
                  <td colspan="6" class="text-center text-muted py-4">
                    No upcoming appointments
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  
    <div class="container-fluid py-4">
      <div class="card shadow-sm upcoming-card mb-4">
        <div class="card-header bg-black text-white rounded-top">
          <h5 class="mb-0">Past Appointments</h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                <th>Date</th>
                <th>Doctor</th>
                <th>Diagnosis</th>
                <th>Status</th>
                <th>Prescription</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(pappointment, index) in pastAppointments" :key="index">
                <td>{{ pappointment.date }}</td>
                <td class="fw-semibold">{{ pappointment.doctor_name }}</td>
                <td>{{ pappointment.diagnosis }}</td>
                <td>
                  <span class="badge"
                      :class="pappointment.status === 'completed' ? 'bg-success' : 'bg-danger'">
                      {{ pappointment.status }}
                    </span>
                  </td>
                <td>
                <span v-if="pappointment.status == 'cancelled'" class="text-muted">N/A</span>
                <a v-else href="#" class="btn btn-sm btn-outline-secondary" 
                data-bs-toggle="modal" data-bs-target="#prescriptionModal" 
                @click="viewinfo(pappointment)">
                  View Prescription
                </a>
              </td>
              </tr>
                <tr v-if="pastAppointments.length === 0">
                  <td colspan="6" class="text-center text-muted py-4">
                    No upcoming appointments
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div>



  <div class="modal fade" id="cancelModal" tabindex="-1" aria-labelledby="cancelModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="cancelModalLabel">Confirm Slot Cancellation</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">Do you really want to Cancel the slot?</div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-dismiss="modal"
        >
          No
        </button>
        <button type="button" class="btn btn-danger" @click="cancelinfo">
          Yes
        </button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="prescriptionModal" tabindex="-1" aria-labelledby="prescriptionModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="prescriptionModalLabel">Doctor Information</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <ul class="list-group list-group-flush">

          <li class="list-group-item"><strong>Email:</strong> {{ formData.diagnosis }}</li>
          <li class="list-group-item"><strong>Name:</strong> {{ formData.prescription }}</li>
          <li class="list-group-item"><strong>Notes:</strong> {{ formData.notes }}</li>
          
        </ul>
      </div>
    </div>
  </div>
</div>


<!-- <payment modal> -->

  <div class="modal fade" id="paymentModal" tabindex="-1" aria-labelledby="paymentModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="paymentModalLabel">Confirm Payment</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body"> Do you really confirm paying {{ selectedAppointment.fees }} rupees?</div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-dismiss="modal"
        >
          No
        </button>
        <button type="button" class="btn btn-danger" @click="payinfo">
          Yes
        </button>
      </div>
    </div>
  </div>
</div>


</template>

<script>
import patient_navbar from './patient_navbar.vue';
import axios from "axios";

export default {
  name: "patient_appointment",
  components: { patient_navbar },
  data() {
    return {
      upcomingAppointments: [],
      pastAppointments: [],
      selectedAppointment: [],
      formData: {
        doc_id: "",
        date_id: "",
        slot_id: "",
        payment: "",
      },
      slotslist: [],
      datelist: [],
      doctorlist: []
    }
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
      try {
        const res = await axios.get("http://127.0.0.1:5000/auth/patient_appointment", {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        });
        if (res.status === 200) {
          this.upcomingAppointments = res.data.upcoming_appointments;
          this.pastAppointments = res.data.past_appointments;
        }
      } catch (err) {
        console.error(err);
      }
    },
    cancelAppointment(appointment) {
      
      console.log(`Cancelling appointment with ID: ${appointment.id}`);
      this.formData={
        id:appointment.id,
        status:"cancelled"
      }
      
    },cancelinfo(){
      axios.put("http://127.0.0.1:5000/auth/patient_appointment",
        this.formData,{
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        }
      ).then(res => {if (res.status==200){
        alert("Appointment succssfully cancelled");

        this.upcomingAppointments = res.data.upcoming_appointments;
        this.pastAppointments = res.data.past_appointments;
      }})
    },
    viewinfo(pappointment){

      this.formData={
        "diagnosis":pappointment.diagnosis,
        "prescription":pappointment.prescription,
        "notes":pappointment.notes
      }

    },
    pay(appointment){
      this.formData={
        payment:"done",
        id:appointment.id
      }
      this.selectedAppointment = appointment;
    },
    payinfo(){
      axios.put("http://127.0.0.1:5000/auth/patient_appointment",
        this.formData,{
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        }
      ).then(res => {if (res.status==200){
        alert("Payment done succssfully");

        this.upcomingAppointments = res.data.upcoming_appointments;
        this.pastAppointments = res.data.past_appointments;
      }})
    }
  }
};
</script>

<style scoped>

.patients-page {
  min-height: 100vh;
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );
  font-family: "Poppins", sans-serif;
}


.container-fluid {
  margin-top: 20px;
}


.card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  border-bottom: 1px solid #eaeaea;
}


.table {
  margin: 0;
  border-radius: 12px;
  overflow: hidden;
}

.table th {
  font-weight: 600;
  font-size: 0.9rem;
}

.table td {
  font-size: 0.9rem;
  vertical-align: middle;
}


.table-hover tbody tr:hover {
  background-color: #f1f7ff;
}


.badge {
  padding: 0.5em 0.75em;
  font-size: 0.75rem;
  border-radius: 8px;
}

/* Cancel button */
.btn-outline-danger {
  font-size: 0.8rem;
  border-radius: 6px;
  padding: 4px 10px;
}

</style>