<template>
  <div class="doctors-page">
    <Navbar @search="doSearch" />

    <div class="container mt-5">
      <div class="table-wrapper shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle custom-table">
            <thead>
              <tr>
                <th scope="col" class="text-center">Name</th>
                <th scope="col" class="text-center">Age</th>
                <th scope="col" class="text-center">Gender</th>
                <th scope="col" class="text-center">Department</th>
                <th scope="col" class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(doctor, index) in doctorsList" :key="index">
                <td class="fw-semibold text-center">{{ doctor.name }}</td>
                <td class="text-center">{{ doctor.age }}</td>
                <td class="text-capitalize text-center">{{ doctor.gender }}</td>
                <td class="text-capitalize text-center">{{ departmentMap[doctor.department_id] }}</td>
                <td class="text-center">
                  <button
                    class="btn btn-sm btn-edit me-2" href="#" data-bs-toggle="modal" data-bs-target="#editModal"
                    @click="editdoctor(doctor)"
                  >
                  
                    <i class="bi bi-pencil-square me-1"></i> Edit
                  </button>
                  
                  <button v-if="doctor.is_active"
                    class="btn btn-sm btn-block me-2" href="#" data-bs-toggle="modal" data-bs-target="#blockModal"
                    @click="blockdoctor(doctor)"
                  >
                  
                    <i class="bi bi-slash-circle me-1"></i> Block
                  </button>
                  <button
                    v-else
                    class="btn btn-sm btn-success me-2" href="#" data-bs-toggle="modal" data-bs-target="#blockModal"
                    @click="unblockdoctor(doctor)"
                  >
                    <i class="bi bi-check-circle me-1"></i> Unblock
                  </button>

                  <button
                    class="btn btn-sm btn-info-btn me-2" href="#" data-bs-toggle="modal" data-bs-target="#infoModal"
                    @click="viewInfo(doctor)"
                  >
                    <i class="bi bi-info-circle me-1"></i> Info
                  </button>

                  <button class="btn btn-sm btn-block me-2" href="#" data-bs-toggle="modal" data-bs-target="#deleteModal"
                    @click="deletedoc(doctor)"> <i class="bi bi-trash me-1"></i> Delete </button>     
                </td>
              </tr>
            </tbody>
          </table>
      </div>
    </div>

<div class="text-center mt-4">
  <button
    class="btn btn-add-user px-4 py-2"
    data-bs-toggle="modal"
    data-bs-target="#addModal" @click="adddoctor(doctor)"
  >
    <i class="bi bi-plus-circle me-2"></i> Add Doctor
  </button>
</div>

    <div
      class="modal fade"
      id="logoutModal"
      tabindex="-1"
      aria-labelledby="logoutModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="logoutModalLabel">Confirm Logout</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">Do you really want to log out?</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
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

  <!-- <edit modal> -->
<div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="editModalLabel"> Edit Details Here<span class="text-primary">!</span></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
  
        <form @submit.prevent="editinfo">

          <div class="mb-3">
          <label for="Input1" class="form-label">E-mail</label>
          <input type="email" class="form-control" id="Input1" :placeholder= "formData.email_id" v-model="formData.email_id" >
        </div>

        <div class="mb-3">
          <label for="Input2" class="form-label">Password</label>
          <input type="password" class="form-control" id="Input2" v-model="formData.password" maxlength="10" >
        </div>

        <div class="mb-3">
          <label for="Input3" class="form-label">Name</label>
          <input type="name" class="form-control" id="Input1" :placeholder= "formData.name" v-model="formData.name" >
        </div>
        <div class="mb-3">
            
  <label class="form-label d-block">Gender</label>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="male" value="male" v-model="formData.gender" >
    <label class="form-check-label" for="male">Male</label>
  </div>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="female" value="female" v-model="formData.gender" >
    <label class="form-check-label" for="female">Female</label>
  </div>

    <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="other" value="other" v-model="formData.gender" >
    <label class="form-check-label" for="other">Other</label>
  </div>

  <div class="mb-3">
      <label for="Input4" class="form-label">Age</label>
      <input type="number" class="form-control" id="Input4" :placeholder= "formData.age" v-model="formData.age" maxlength="10" >
    </div>

    <div class="mb-3">
  <label for="deptSelect" class="form-label">Select Department</label>
  <select class="form-select" id="deptSelect" v-model="formData.department_id" required>
    <option disabled value="">-- Select Department --</option>
    <option v-for="dept in departmentList" :key="dept.id" :value="dept.id">
      {{ dept.dept_name }}
    </option>
  </select>
</div>

</div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary w-100" data-bs-dismiss="modal">Submit</button>
      
          </div>
        </form>
      </div>
    </div>
  </div>
</div>


<!-- <info modal> -->

<div class="modal fade" id="infoModal" tabindex="-1" aria-labelledby="infoModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="infoModalLabel">doctor Information</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">

        <ul class="list-group list-group-flush">
          <li class="list-group-item"><strong>Email:</strong> {{formData.email_id }}</li>
          <li class="list-group-item"><strong>Name:</strong> {{formData.name }}</li>
          <li class="list-group-item"><strong>Gender:</strong> {{formData.gender }}</li>
          <li class="list-group-item"><strong>Age:</strong> {{formData.age }}</li>
          <li class="list-group-item"> <strong>Department:</strong> 
          {{ selectedDepartment ? selectedDepartment.dept_name : '' }}</li>
          
        </ul>

      </div>
    </div>
  </div>
</div>


<!-- <block modal> -->

  <div
      class="modal fade"
      id="blockModal"
      tabindex="-1"
      aria-labelledby="blockModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="blockModalLabel" v-if="!formData.is_active">Confirm blocking</h5>
            <h5 class="modal-title" id="blockModalLabel" v-else>Confirm unblocking</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body" v-if="!formData.is_active">Do you really want to block the doctor?</div>
          <div class="modal-body" v-else>Do you really want to unblock the doctor?</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              No
            </button>
            <button type="button" class="btn btn-danger" v-if="formData.is_active" @click="blockinfo" data-bs-dismiss="modal">
              Yes
            </button>
            <button type="button" class="btn btn-danger" v-else @click="unblockinfo" data-bs-dismiss="modal">
              Yes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

<!-- <add modal> -->

  <div class="modal fade" id="addModal" tabindex="-1" aria-labelledby="addModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="addModalLabel"> Add doctors Here<span class="text-primary">!</span></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
  
        <form @submit.prevent="addinfo">

          <div class="mb-3">
          <label for="Input1" class="form-label">E-mail</label>
          <input type="email" class="form-control" id="Input1" placeholder= "Happy@gmail.com" v-model="formData.email_id" required >
        </div>

        <div class="mb-3">
          <label for="Input2" class="form-label">Password</label>
          <input type="password" class="form-control" id="Input2" v-model="formData.password" maxlength="10" required>
        </div>

        <div class="mb-3">
          <label for="Input3" class="form-label">Name</label>
          <input type="name" class="form-control" id="Input1" placeholder= "Happy" v-model="formData.name" required>
        </div>
        <div class="mb-3">
            
  <label class="form-label d-block">Gender</label>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="male" value="male" v-model="formData.gender" required>
    <label class="form-check-label" for="male">Male</label>
  </div>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="female" value="female" v-model="formData.gender" >
    <label class="form-check-label" for="female">Female</label>
  </div>

    <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="other" value="other" v-model="formData.gender" >
    <label class="form-check-label" for="other">Other</label>
  </div>

  <div class="mb-3">
      <label for="Input4" class="form-label">Age</label>
      <input type="number" class="form-control" id="Input4"  v-model="formData.age" maxlength="10" required>
    </div>

</div>

<div class="mb-3">
  <label for="deptSelect" class="form-label">Select Department</label>
  <select class="form-select" id="deptSelect" v-model="formData.department_id" required>
    <option disabled value="">-- Select Department --</option>
    <option v-for="dept in departmentList" :key="dept.id" :value="dept.id">
      {{ dept.dept_name }}
    </option>
  </select>
</div>

          <div class="text-center">
            <button type="submit" class="btn btn-primary w-100" >Submit</button>
      
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- <deleteModal> -->

<div class="modal fade"id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Confirm Deleting</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">Do you really want to delete the doctor's account?</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn b tn-secondary"
              data-bs-dismiss="modal"
            >
              No
            </button>
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deletedoctor">
              Yes
            </button>
          </div>
        </div>
      </div>
    </div>

</template>



<script>
import Navbar from "./admin_navbar.vue";
import axios from "axios";

export default {
  name: "doctors",
  components: { Navbar },
  data() {
    return {
      doctorsList: [],
      query: "",
      token: "",
      formData: {
        email_id:"",
        age: "",
        gender: "",
        name: "",
        password: "",
        department_id: ""
      },
      departmentList:[]
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.query) return this.doctorsList;
      const q = this.query.toLowerCase();
      return this.doctorsList.filter((p) => p.name.toLowerCase().includes(q));
    },
    selectedDepartment() {
    return this.departmentList.find(
      d => d.id === this.formData.department_id
    );
  },departmentMap() {
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

    loadDoctors() {
      axios.get("http://127.0.0.1:5000/auth/admin_doctors", {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((res) => {
          this.doctorsList = res.data.doctorsList;
          this.departmentList=res.data.departmentList;
        })
        .catch((err) => {
          console.error(err);
        });
    },

  editdoctor(doctor) {
   this.formData = {
    id:doctor.id,
    email_id: doctor.email_id,
    age: doctor.age,
    gender: doctor.gender,
    name: doctor.name,
    password: doctor.password,
    department_id: doctor.department_id
};
  },

  async editinfo(){
    await axios.put('http://127.0.0.1:5000/auth/admin_doctors', this.formData,{
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }
    ).then(res => {if (res.status==200){
      console.log("Doctor info successfully updated",res.data);
      alert("User information updated successfully");
      this.loadDoctors();
      
    }})
  },

  blockdoctor(doctor) {
    console.log("Block doctor", doctor);
     this.formData = {
      id: doctor.id,
      is_active: false,   
      email_id: doctor.email_id,
      age: doctor.age,
      gender: doctor.gender,
      name: doctor.name,
      password: doctor.password,
      department_id: doctor.department_id
    };
  },
  async blockinfo(){
    await axios.put('http://127.0.0.1:5000/auth/admin_doctors',this.formData,{
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }).then(res => {if (res.status==200){
      console.log("doctor blocked successfully",res.data);
      this.loadDoctors();
  }})
  },
  unblockdoctor(doctor){
    console.log("Block doctor", doctor);
     this.formData = {
      id: doctor.id,
      is_active: true,   
      email_id: doctor.email_id,
      age: doctor.age,
      gender: doctor.gender,
      name: doctor.name,
      password: doctor.password,
      department_id: doctor.department_id
    };
  },
  async unblockinfo(){
     await axios.put('http://127.0.0.1:5000/auth/admin_doctors',this.formData,{
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }).then(res => {if (res.status==200){
      console.log("doctor blocked successfully",res.data);
      this.loadDoctors();
  }})

  },

    viewInfo(doctor) {
      console.log("View info for", doctor);
      this.formData = {
        id: doctor.id,
        email_id: doctor.email_id,
        password: doctor.passoword,
        age: doctor.age,
        gender: doctor.gender,
        name: doctor.name,
        department_id: doctor.department_id
      }
    },
    adddoctor(doctor){
      console.log("add doctor",doctor);
      this.formData = {
      is_active: true,   
      email_id: doctor.email_id,
      age: doctor.age,
      gender: doctor.gender,
      name: doctor.name,
      password: doctor.password,
      department_id: doctor.department_id
    }
   },
   async addinfo(){
    await axios.post('http://127.0.0.1:5000/auth/admin_doctors',this.formData,{
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }).then(res => {
      if (res.status == 200 ) {
       alert("doctor added successfully"), 200;
        this.loadDoctors();
        
      }
    }).catch(res => (alert("Email id exists please try with a different email id")))

    },

    logout() {
      this.token = null;
      localStorage.clear();
      this.$router.push("/");
      setTimeout(() => {
        document.body.classList.remove("modal-open");
        document
          .querySelectorAll(".modal-backdrop")
          .forEach((el) => el.remove());
      }, 100);
    },deletedoc(doctor){
    console.log("Delete button clicked");
    this.formData = {
      id:doctor.id,
      is_active: true,   
      email_id: doctor.email_id,
      age: doctor.age,
      gender: doctor.gender,
      name: doctor.name,
      password: doctor.password,
      department_id: doctor.department_id
    }
  },deletedoctor(){
    axios.delete("http://127.0.0.1:5000/auth/admin_doctors",{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },data:this.formData
    }).then(res => {if (res.status==200){
      alert(res.data.message);
      this.loadDoctors();
    }});
  }
  },
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
.btn-edit {
  background-color: #4e73df;
  color: #fff;
  border: none;
}
.btn-block {
  background-color: #e74a3b;
  color: #fff;
  border: none;
}
.btn-info-btn {
  background-color: #36b9cc;
  color: #fff;
  border: none;
}
.btn-add-user {
  background: repeating-linear-gradient(90deg, #4cafef, #007bff);
  color: #fff;
  font-weight: 600;
  font-size: 1.05rem;
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
  transition: all 0.3s ease-in-out;
}

.btn-add-user:hover {
  background: repeating-linear-gradient(90deg, #007bff, #4cafef);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
}

</style>
