<script>
import { RouterLink } from 'vue-router';
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        email_id: "",
        password: "",
        name: "",
        age: "",
        gender: ""
      },
      token: ""
    };
  },
  methods: {
    registerinfo() {
      axios.post(
        'http://127.0.0.1:5000/auth/register',
        JSON.stringify(this.formData),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        }
      ).then(response => {
        if (response.status == 200 || 201  ) {
          this.token = response.data.access_token;
          localStorage.setItem("token",response.data.access_token);
          this.$router.push("/patient_dashboard");
        }
      }).catch(response =>{alert("Already an existing user please login to continue")}
        
      );
    }
  }
}
</script>

<template>
<div class="register-body">
<div id="main">
  <div id="canvas">
    <div id="form-body" class="card shadow-lg p-4 rounded-4">
      <h5 class="text-center mb-4">Hey! Welcome  to <span class="text-primary">Hap!Care</span></h5>
      <form @submit.prevent="registerinfo" method="post">

        <div class="mb-3">
          <label for="Input1" class="form-label">E-mail</label>
          <input type="email" class="form-control" id="Input1" placeholder="Happy@gmail.com" v-model="formData.email_id" required>
        </div>

        <div class="mb-3">
          <label for="Input2" class="form-label">Password</label>
          <input type="password" class="form-control" id="Input2" v-model="formData.password" maxlength="10" required>
        </div>

        <div class="mb-3">
          <label for="Input3" class="form-label">Name</label>
          <input type="name" class="form-control" id="Input1" placeholder="Happy" v-model="formData.name" required>
        </div>
        <div class="mb-3">
            
  <label class="form-label d-block">Gender</label>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="male" value="male" v-model="formData.gender" required>
    <label class="form-check-label" for="male">Male</label>
  </div>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="female" value="female" v-model="formData.gender" required>
    <label class="form-check-label" for="female">Female</label>
  </div>

    <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="gender" id="other" value="other" v-model="formData.gender" required>
    <label class="form-check-label" for="other">Other</label>
  </div>

  <div class="mb-3">
      <label for="Input4" class="form-label">Age</label>
      <input type="number" class="form-control" id="Input4" v-model="formData.age" maxlength="10" required>
    </div>

</div>
        <div class="text-center">
          <button type="submit" class="btn btn-primary w-100">Sign Up</button>
           <!-- <button @click="registerUser" class="btn btn-primary w-100">Sign Up</button> -->
          <p class="mt-3 mb-0 text-muted">Already have an account? <RouterLink to="/">Sign In</RouterLink></p>
        </div>
      </form>
    </div>
  </div>
</div>
</div>
</template>

<style scoped>

.register-body {
  background: url("https://static.vecteezy.com/system/resources/thumbnails/041/859/876/small_2x/national-doctor-s-day-hand-drawn-background-vector.jpg") ;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  backdrop-filter: blur(2px);  
}


#main {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}


#form-body {
  background: #fff;
  max-width: 500px;
  width: 120%;
  justify-content: center;
  border-radius: 20px;
}

.form-control:focus {
  border-color: #2a5298;
  box-shadow: 0 0 0 0.25rem rgba(42, 82, 152, 0.25);
}

.btn-primary {
  background: #2a5298;
  border: none;
  transition: all 0.3s ease-in-out;
}
.btn-primary:hover {
  background: #1e3c72;
  transform: scale(1.03);
}

</style>