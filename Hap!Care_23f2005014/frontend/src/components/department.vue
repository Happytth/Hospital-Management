<template>
<div class="department-page">
  <Navbar @search="doSearch" />
  <div class="card-grid">
    
 
  <div v-for="(department, index) in departmentList" :key="index" class="card shadow-lg border-0 rounded-3" 
  style="width:300px;">
    <img class="card-img-top rounded-top" 
         :src="department.bg_img" 
         alt="Card image" style="height: 200px; object-fit: cover;">
    <div class="card-body text-center">
      <h4 class="card-title fw-bold text-primary">{{ department.dept_name }}</h4>
      <p class="card-text text-muted">Book an appointment with top specialists near you.</p>
      <div class="d-flex justify-content-center gap-2">
      <button class="btn btn-sm btn-info-btn btn-abc" href="#" data-bs-toggle="modal" data-bs-target="#infoModal"
                    @click="viewInfo(department)"><i class="bi bi-info-circle me-1"></i>See Info</button>
      
      <button class="btn btn-sm btn-edit me-2" href="#" data-bs-toggle="modal" data-bs-target="#editModal"
                    @click="editdept(department)"> <i class="bi bi-pencil-square me-1"></i> Edit </button>

          <button class="btn btn-sm btn-block me-2" href="#" data-bs-toggle="modal" data-bs-target="#deleteModal"
                    @click="deletedept(department)"> <i class="bi bi-trash me-1"></i> Delete </button>          
    </div>
  </div>
</div>
</div>

<div class="text-center mt-4">
  <button
    class="btn btn-add-user px-4 py-2"
    data-bs-toggle="modal"
    data-bs-target="#addModal" @click="addDepartment(department)">
    <i class="bi bi-plus-circle me-2"></i> Add Department</button>
</div>

   <div class="modal fade"id="logoutModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
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
  
<!-- <add Modal> -->
  <div class="modal fade" id="addModal" tabindex="-1" aria-labelledby="addModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="addModalLabel"> Add Departments Here<span class="text-primary">!</span></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
  
<form @submit.prevent="addinfo">

  <div class="mb-3">
  <label for="Input1" class="form-label">Department Id</label>
  <input type="name" class="form-control" id="Input1" placeholder= "D100" v-model="formData.dept_id" required >
</div>

<div class="mb-3">
  <label for="Input2" class="form-label">Department Name</label>
  <input type="name" class="form-control" id="Input2" v-model="formData.dept_name" required>
</div>

<div class="mb-3">
    <label for="Input3" class="form-label">Description</label>
    <textarea class="form-control" id="Input3" placeholder="Write description here" v-model="formData.description" ></textarea>
</div>

<div class="mb-3">       
    <label for="Input4" class="form-label">Background Image</label>
    <input type="name" class="form-control" id="Input4"  v-model="formData.bg_img" >
</div>

  <div class="text-center">
    <button type="submit" class="btn btn-primary w-100" >Submit</button>
  </div>
</form>
      </div>
    </div>
  </div>
</div>

</div>

<!-- <editModal> -->

<div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="editModalLabel"> Edit Departments Here<span class="text-primary">!</span></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
  
<form @submit.prevent="editinfo">

  <div class="mb-3">
  <label for="Input1" class="form-label">Department Id</label>
  <input type="name" class="form-control" id="Input1" :placeholder= "formData.dept_id" v-model="formData.dept_id" >
</div>

<div class="mb-3">
  <label for="Input2" class="form-label">Department Name</label>
  <input type="name" class="form-control" id="Input2" v-model="formData.dept_name" :placeholder="formData.dept_name">
</div>

<div class="mb-3">
    <label for="Input3" class="form-label">Description</label>
    <textarea class="form-control" id="Input3" :placeholder="formData.description" v-model="formData.description" ></textarea>
</div>

<div class="mb-3">       
    <label for="Input4" class="form-label">Background Image</label>
    <input type="name" class="form-control" id="Input4"  v-model="formData.bg_img" >
</div>

  <div class="text-center">
    <button type="submit" class="btn btn-primary w-100" >Submit</button>
  </div>
</form>
      </div>
    </div>
  </div>
</div>

    

<!-- <infoModal> -->
  
<div class="modal fade" id="infoModal" tabindex="-1" aria-labelledby="infoModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="infoModalLabel">Department Information</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">

        <ul class="list-group list-group-flush">
          <li class="list-group-item"><strong>Department ID:</strong> {{ formData.dept_id }}</li>
          <li class="list-group-item"><strong>Name:</strong> {{ formData.dept_name }}</li>
          <li class="list-group-item"><strong>Description:</strong> {{ formData.description }}</li>
          <li class="list-group-item"><strong>Total Doctors:</strong> 
           ({{ doctorList.filter(d => d.department_id === formData.id).length }})
          <ul>
          <li v-for="doc in doctorList.filter(d => d.department_id === formData.id)" :key="doc.id">
           {{ doc.name }}
          </li>
          </ul>
          </li>

        </ul>

      </div>
    </div>
  </div>
</div>


   <div class="modal fade"id="logoutModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
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
          <div class="modal-body">Do you really want to delete this department?</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn b tn-secondary"
              data-bs-dismiss="modal"
            >
              No
            </button>
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deletedepartment">
              Yes
            </button>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
import axios from "axios";
import Navbar from "./admin_navbar.vue";
export default {
    name:"admin_department",
    components: { Navbar },
  data() {
    return {
        formData:{
            id:"",
            dept_id:"",
            dept_name:"",
            // doc_registred:"",
            description:"",
            bg_img:""
        },
      departmentList: [],
      doctorList:[],
      token:"",
      query:""
    };
  },computed:{

  },
  mounted() {
    this.loadDepartments();
    this.loadToken();
    setTimeout(() => {
      document.body.classList.remove("modal-open");
      document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
    }, 50);
  },
  methods: {
    loadToken(){
       const token=localStorage.getItem("token")
        if (token){
            this.token=token;
        }
    },
    async loadDepartments() {
        await axios.get("http://127.0.0.1:5000/auth/admin_department",
            {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            }
        ).then(res => {
            console.log("Departmetns fetched successfully",res.data);
            this.departmentList=res.data.departmentList;
            this.doctorList=res.data.doctorList;
        }).catch(err => {console.log(err)})
      
    },
    addDepartment(department){
        this.formData={
            id:department.id,
            dept_id:department.dept_id,
            // doc_registred:department.doc_registred,
            dept_name:department.dept_name,
            description:department.description
        }
    }, 
    async addinfo(){
        await axios.post("http://127.0.0.1:5000/auth/admin_department",this.formData,{
        headers:{
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    }).then(res => {if (res.status==200){
        alert("Department successfully added");
        this.loadDepartments();
    }}).catch(res => {alert("Department already exists")})
  }, 
  logout(){
    this.token=null;
    localStorage.clear();
    this.$router.push("/");
    setTimeout(() => {
        document.body.classList.remove("modal-open");
        document
          .querySelectorAll(".modal-backdrop")
          .forEach((el) => el.remove());
      }, 100);
  },
  viewInfo(department){
    console.log("View info for", department);
    this.formData = {
      id:department.id,
      dept_id: department.dept_id,
      description: department.description,
      dept_name: department.dept_name
    }
  },
  editdept(department){
    console.log("Edit department", department);
    this.formData={
      id:department.id,
      dept_id:department.dept_id,
      description:department.description,
      dept_name:department.dept_name,
      bg_img:department.bg_img
    }
  },
 async editinfo(){
   await axios.put("http://127.0.0.1:5000/auth/admin_department",this.formData,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }).then(res => {if (res.status==200){
      this.loadDepartments();
      alert("Department updated successfully");

    }})

    .catch(error => {
    if (error.response && error.response.status === 400) {
      alert(error.response.data.message || "Department ID already exists");
    } else {
      alert("An error occurred while updating the department");
    }
  });
  },deletedept(department){
    console.log("Delete button clicked");
    this.formData={
      id:department.id,
      dept_id:department.dept_id,
      dept_name:department.dept_name,
      description:department.description
    }
  },deletedepartment(){
    axios.delete("http://127.0.0.1:5000/auth/admin_department",{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },data:this.formData
    }).then(res => {if (res.status==200){
      alert(res.data.message);
      this.loadDepartments();
    }});
  }

  }
}

</script>

<style scoped>
.department-page {
  min-height: 100vh;
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );
  font-family: "Poppins", sans-serif;
}
 .card-body:hover{
      transform: scale(1.05);
      transition: transform 0.3s ease;
      color: #0d6efd;
    }
    .card:hover{
      transform: scale(1.05);
      transition: transform 0.3s ease;
      color: #0d6efd;
    }

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 100px;
  padding: 75px;
}
    
.btn {
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
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
.btn-info-btn {
  background-color: #36b9cc;
  color: #fff;
  border: none;
}
.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
.btn-abc{
   
  display: flex;
  align-items: center;  
  justify-content: center; 
  gap: 6px;  

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
</style>
