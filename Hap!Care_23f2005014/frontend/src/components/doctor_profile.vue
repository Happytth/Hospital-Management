<template>
  <div class="profile-page">
    <doctor_navbar @search="doSearch" />

    <div class="container mt-5">
      <div class="card shadow-sm rounded-4">
        <div class="card-header bg-primary text-white d-flex align-items-center">
          <i class="bi bi-person-circle fs-3 me-2"></i>
          <h5 class="mb-0">My Profile</h5>
        </div>
        <div class="card-body p-4">
          <form @submit.prevent="changeprofile">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Name</label>
                <input v-model="formData.name" :placeholder="formData.name" type="text" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Email</label>
                <input v-model="formData.email_id" type="email" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Age</label>
                <input v-model="formData.age" type="number" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Password</label>
                <input v-model="formData.password" type="password" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Fees</label>
                <input v-model="formData.fees" type="number" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label d-block">Gender</label>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" value="male" v-model="formData.gender" />
                  <label class="form-check-label">Male</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" value="female" v-model="formData.gender" />
                  <label class="form-check-label">Female</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" value="other" v-model="formData.gender" />
                  <label class="form-check-label">Other</label>
                </div>
              </div>

           
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

              <div class="col-md-6">
                <label class="form-label">Start Time</label>
                <input v-model="formData.start_time" type="time" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">End Time</label>
                <input v-model="formData.end_time" type="time" class="form-control" />
              </div>

      
              <button
                class="btn btn-danger col-md-2"
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#deleteModal"
              >
                <i class="bi bi-trash sidebar-icon"></i> Delete Account
              </button>

              <div class="col-12">
                <button class="btn btn-primary w-100" type="submit">
                  <i class="bi bi-save me-1"></i> Save Changes
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>


  <div
    class="modal fade"
    id="deleteModal"
    tabindex="-1"
    aria-labelledby="deleteModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="deleteModalLabel">Confirm Delete</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">Do you really want to delete your account permanently?</div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            No
          </button>
          <button type="button" class="btn btn-danger" @click="deleteinfo">
            Yes
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
  name: "doctor_profile",
  components: { doctor_navbar },
  data() {
    return {
      formData: {
        name: "",
        email_id: "",
        age: "",
        gender: "",
        password: "",
        start_time: "",
        end_time: "",
        available_dates: [],
        fees:""
      },
      token: "",
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
    this.loadToken();
    this.loaduser();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem("token");
      if (token) this.token = token;
    },
    async loaduser() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/auth/doctor_profile", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`,
          },
        });
        if (res.status === 200 && res.data.formData) {
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
      } catch (err) {
        console.error("Error loading profile:", err);
      }
    },
    async changeprofile() {
      try {
        const res = await axios.put(
          "http://127.0.0.1:5000/auth/doctor_profile",
          this.formData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        if (res.status === 200) {
          alert(res.data.message);
          this.loaduser();
        }
      } catch (err) {
        alert(err.response?.data?.message || "An error occurred");
      }
    },
    async deleteinfo() {
      try {
        const res = await axios.delete("http://127.0.0.1:5000/auth/doctor_profile", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`,
          },
          data: { email_id: this.formData.email_id },
        });
        if (res.status === 200) {
          alert(res.data.message);
          localStorage.clear();
          this.$router.push("/");
        }
      } catch (err) {
        alert(err.response?.data?.message || "Failed to delete account");
      }
    },
  },
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: repeating-linear-gradient(125deg, #e6f0fa, #b2d8f7, white);
  font-family: "Poppins", sans-serif;
}
.card-header i {
  line-height: 1;
}
</style>
