<script>
import { RouterLink } from 'vue-router';
import axios from 'axios'
export default{
  data(){
    return{
      formData:{
        email_id:"",
        password:"",
        role:""
      },token:""
    }
  },
  
  methods:{
    async logininfo(){
       await axios.post(
        'http://127.0.0.1:5000/auth/login', JSON.stringify(this.formData),
        
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization":`Bearer ${localStorage.getItem("token")}`
          }
        }
      )
      .then(res => {if (res.status==200){
        this.token=res.data.access_token;
        localStorage.setItem('token',res.data.access_token);

        if (this.formData.email_id=="happytth@gmail.com"){
        this.$router.push("/admin_dashboard")
      }
        else if(this.formData.role=="yes"){
          this.$router.push("/patient_dashboard");
        }
        else{
          this.$router.push("/doctor_dashboard");
        }
        setTimeout(() => {
  document.body.classList.remove('modal-open');
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
}, 100);
      }
  }
  ).catch(err => {
      if (err.response && err.response.status === 401) {
        alert('Invalid credentials, please ensure your credentials are correct')
      } else {
        alert('Something went wrong. Please try again later.')
      }
    })
      
    }
  }
}

</script>

<template>
    
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <RouterLink class="navbar-brand" to="/">Hap!Care</RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        
      </ul>
      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/register"><i class="bi bi-person"></i> Sign Up</RouterLink>
        </li>
         <li class="nav-item">
          <a class="nav-link" href="#" data-bs-toggle="modal" data-bs-target="#loginModal">
            <i class="bi bi-box-arrow-in-right"></i> Login
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<!-- <div class="container mt-4">
  <div class="row align-items-center">
    <div class="col-md-6">
      <h1 class="display-5 fw-bold">Your Health, Our Priority</h1>
      <p>Top doctors, personalized care, and affordable deals—right at your fingertips.</p>
      <a data-bs-toggle="modal" data-bs-target="#loginModal" class="btn btn-primary btn-lg mt-2">Book Appointment</a>
    </div>
    <div class="col-md-6">
      <img src="https://images.pexels.com/photos/371633/pexels-photo-371633.jpeg?cs=srgb&dl=clouds-country-daylight-371633.jpg&fm=jpg" alt="Medical team" class="img-fluid rounded" />
    </div>
  </div>
</div> -->

<div class="container my-5">
  <div class="card shadow border border-0 rounded-4">
    <div class="row align-items-center">
      <div class="col-md-6 px-4"><h1 class="display-5 mt-5 d-flex justify-content-around fw-bold">Facing issues, Don't worry</h1>
      <p class="mb-5" style="margin-left: 40px;">Top doctors, personalized care, <br> and affordable deals—right at your fingertips.</p>
      <a data-bs-toggle="modal" data-bs-target="#loginModal" class="btn btn-primary mb-3 btn-lg ms-4">Book Appointment</a>
      </div>
      <div class="col-md-6" style="background-image: url(https://images.pexels.com/photos/371633/pexels-photo-371633.jpeg?cs=srgb&dl=clouds-country-daylight-371633.jpg&fm=jpg);
      background-blend-mode: hue;
      background-repeat: repeat-y;">
         <img src="https://images.pexels.com/photos/371633/pexels-photo-371633.jpeg?cs=srgb&dl=clouds-country-daylight-371633.jpg&fm=jpg" alt="Medical team" class="img-fluid my-3 rounded" />
      </div>
    </div>
</div>
</div>



<div class="d-flex justify-content-center gap-4 mt-5">

  <div class="card shadow-lg border-0 rounded-3" style="width:300px;">
    <img class="card-img-top rounded-top" 
         src="https://i.pinimg.com/236x/79/48/9e/79489e4a15d6a6d71cb6e324ab29bb81.jpg" 
         alt="Card image" style="height: 250px; object-fit: cover;">
    <div class="card-body text-center">
      <h4 class="card-title fw-bold text-primary">Find Best Doctors</h4>
      <p class="card-text text-muted">Book an appointment with top specialists near you.</p>
      <a data-bs-toggle="modal" data-bs-target="#loginModal" class="btn btn-primary px-4">See List</a>
    </div>
  </div>


  <div class="card shadow-lg border-0 rounded-3" style="width:300px;">
    <img class="card-img-top rounded-top" 
         src="https://plus.unsplash.com/premium_photo-1661410991860-4cd86e2613e7?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8bWVkaWNhbCUyMHRlc3R8ZW58MHx8MHx8fDA%3D" 
         alt="Card image" style="height: 250px; object-fit: cover;">
    <div class="card-body text-center">
      <h4 class="card-title fw-bold text-primary">Find Best Care</h4>
      <p class="card-text text-muted">Go through our website to find best care specialized for your needs.</p>
      <a data-bs-toggle="modal" data-bs-target="#loginModal" class="btn btn-primary px-4">See List</a>
    </div>
  </div>


  <div class="card shadow-lg border-0 rounded-3" style="width:300px;">
    <img class="card-img-top rounded-top" 
         src="https://t4.ftcdn.net/jpg/02/76/80/31/360_F_276803150_yUZGcTLjJErZdmLw0GhDzARQY91S6yrv.jpg" 
         alt="Card image" style="height: 250px; object-fit: cover;">
    <div class="card-body text-center">
      <h4 class="card-title fw-bold text-primary">Find Best Deals </h4>
      <p class="card-text text-muted">Find best deals on meds.</p>
      <a data-bs-toggle="modal" data-bs-target="#loginModal" class="btn btn-primary px-4">See List</a>
    </div>
  </div>
</div>
<br>
<br>

<div class="container mt-5">
  <h2 class="ms-4 fw-semibold">Consult with us</h2>
  <p class="ms-4 text-muted">
    We provide the best care and deals on medicines tailored for your needs.
  </p>
</div>

<div class="container mt-5">
  <div class="row text-center">

    <div class="col-md-3 col-6 mb-4">
      <div class="icon-circle mx-auto">
        <img src="https://img.icons8.com/color/96/female.png" alt="Icon">
      </div>
      <h6 class="mt-3">Period doubts or Pregnancy</h6>
      <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal" class="text-primary fw-bold">CONSULT NOW</a>
    </div>

    <div class="col-md-3 col-6 mb-4">
      <div class="icon-circle mx-auto">
        <img src="https://img.icons8.com/?size=100&id=YqDXkdIG9ggE&format=png&color=000000" alt="Icon">
      </div>
      <h6 class="mt-3">Acne, pimple or skin issues</h6>
      <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal" class="text-primary fw-bold">CONSULT NOW</a>
    </div>


    <div class="col-md-3 col-6 mb-4">
      <div class="icon-circle mx-auto">
        <img src="https://img.icons8.com/color/96/gender.png" alt="Icon">
      </div>
      <h6 class="mt-3">Want to do Surgery</h6>
      <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal" class="text-primary fw-bold">CONSULT NOW</a>
    </div>


    <div class="col-md-3 col-6 mb-4">
      <div class="icon-circle mx-auto">
        <img src="https://img.icons8.com/?size=100&id=DyZBWATXeeiF&format=png&color=000000" alt="Icon">
      </div>
      <h6 class="mt-3">Cold, cough or fever</h6>
      <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal" class="text-primary fw-bold">CONSULT NOW</a>
    </div>

  </div>
</div>
<br>
<br>
<hr>


    <div class="container py-5">
  <div class="row align-items-start">

    <div class="col-lg-4 col-md-5 mb-4 mb-lg-0">
      <h2 class="fw-bold mb-3">Read articles from health experts</h2>
      <p>
        Health articles keep you informed and updated about daily happenings in the medical field.
      </p>
    </div>

    <div class="col-lg-8 col-md-7">
      <div class="row g-4">

        <div class="col-md-6">
          <div class="card h-100 shadow-sm">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDJEK3TeSihht6lWc4otOYYPNjURrhD95yHw&s" class="card-img-top" alt="Article 1"
                 style="width:100%; height:140px; object-fit:cover;" />
            <div class="card-body">
              <small class="text-primary fw-semibold">CORONAVIRUS</small>
              <h5 class="card-title mt-2">
                <a href="https://www.who.int/health-topics/coronavirus#tab=tab_1" class="text-decoration-none text-dark">
                  12 Coronavirus Myths and Facts That You Should Be Aware Of
                </a>
              </h5>
              <p class="card-text text-muted mb-0">Dr. Diana Borgio</p>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card h-100 shadow-sm">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiU1hwUlyX-fx4v8zOMuhLKa_F-ysKY7KqNw&s" class="card-img-top" alt="Article 2"
                 style="width:100%; height:140px; object-fit:cover;" />
            <div class="card-body">
              <small class="text-success fw-semibold">VITAMINS AND SUPPLEMENTS</small>
              <h5 class="card-title mt-2">
                <a href="https://www.medicalnewstoday.com/articles/195878" class="text-decoration-none text-dark">
                  Eating Right to Build Immunity Against Cold and Viral Infections
                </a>
              </h5>
              <p class="card-text text-muted mb-0">Dr. Diana Borgio</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<br>
<hr>
<div class="container-fluid py-5 bg-white" style="min-width: 400px;">
  <div id="testimonialCarousel" class="carousel slide position-relative" data-bs-ride="carousel" data-bs-interval="1500">
    <div class="carousel-inner text-center">
      <div class="carousel-item active">
        <h2 class="fw-bold mb-4" style="font-size:1.3rem;">What our users have to say</h2>
        <p class="fs-5 mb-4" style="font-size: 0.9rem; line-height: 1.3;">
          Very easy to book, maintain history.<br/>
          Hassle free from older versions of booking appointment via telephone..<br/>
          Thanks Hap!Care for making it simple.
        </p>
        <div class="d-flex justify-content-center align-items-center gap-2 mb-3">
          <span class="bg-light rounded-circle p-2 d-inline-flex">
            <i class="fa fa-user fs-5 text-secondary"></i>
          </span>
          <span class="fw-semibold fs-5" style="font-size: 0.9rem;">Jyothi Bhatia</span>
        </div>
      </div>

      <div class="carousel-item">
        <h2 class="fw-bold mb-4" style="font-size:1.3rem;">What our users have to say</h2>
        <p class="fs-5 mb-4" style="font-size: 0.9rem; line-height: 1.3;">
          Quick and easy search with speedy booking. Even maintains history of doctors visited.
        </p>
        <div class="d-flex justify-content-center align-items-center gap-2 mb-3">
          <span class="bg-light rounded-circle p-2 d-inline-flex">
            <i class="fa fa-user fs-5 text-secondary"></i>
          </span>
          <span class="fw-semibold fs-5" style="font-size: 0.9rem;">Amit Sharma</span>
        </div>
      </div>
    </div>

    <button class="carousel-control-prev" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="prev"
      style="width: 40px; height: 40px; background: rgba(0,0,0,0.5); border-radius: 50%; position: absolute; top: 50%; left: 5px; transform: translateY(-50%);">
      <span class="carousel-control-prev-icon" aria-hidden="true"
        style="filter: invert(1) brightness(2); width: 20px; height: 20px;"></span>
      <span class="visually-hidden">Previous</span>
    </button>

    <button class="carousel-control-next" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="next"
      style="width: 40px; height: 40px; background: rgba(0,0,0,0.5); border-radius: 50%; position: absolute; top: 50%; right: 5px; transform: translateY(-50%);">
      <span class="carousel-control-next-icon" aria-hidden="true"
        style="filter: invert(1) brightness(2); width: 20px; height: 20px;"></span>
      <span class="visually-hidden">Next</span>
    </button>

    <div class="carousel-indicators mt-4">
      <button type="button" data-bs-target="#testimonialCarousel" data-bs-slide-to="0" class="active" aria-current="true"></button>
      <button type="button" data-bs-target="#testimonialCarousel" data-bs-slide-to="1"></button>
    </div>
  </div>
</div>

<br>
<br>
<footer class="bg-primary text-white py-5">
  <div class="container text-center">
    <div class="row justify-content-center mb-4 gx-5">
      <div class="col-md-3 mb-3">
        <h5 class="fw-bold">Contact Us</h5>
        <p>📍 Bhadrak, Odisha </p>
        <p>📞 +91 9876543210</p>
        <p>📧 info@yourdomain.com</p>
      </div>
      <div class="col-md-3 mb-3">
        <h5 class="fw-bold">Tests Offered</h5>
        <ul class="list-unstyled">
          <li>Blood Test</li>
          <li>Covid-19 Test</li>
          <li>Glucose Test</li>
          <li>Thyroid Test</li>
          <li>Urine Test</li>
        </ul>
      </div>
      <div class="col-md-3 mb-3">
        <h5 class="fw-bold">Follow Us</h5>
        <div class="d-flex justify-content-center gap-3 fs-4">
          <a href="#" class="text-white" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
          <a href="#" class="text-white" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
          <a href="#" class="text-white" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          <a href="#" class="text-white" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          <a href="#" class="text-white" aria-label="GitHub"><i class="fab fa-github"></i></a>
        </div>
      </div>
    </div>
    <div>
      <h2 class="fw-bold mb-0" style="font-family:sans-serif; letter-spacing: -2px;">
        <span style="color:white;">•</span> Hap!Care <span style="color:#32d0fb;">•</span>
      </h2>
      <small class="text-white-50 mt-2 d-block">© 2025 Hap!Care. All rights reserved.</small>
    </div>
  </div>
</footer>


<div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-4 shadow-lg">
      <div class="modal-header">
        <h5 class="modal-title fw-bold" id="loginModalLabel">Login to <span class="text-primary">Hap!Care</span></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
  
        <form @submit.prevent="logininfo">
          <div class="mb-3">
            <label for="Input1" class="form-label">Username (E-mail)</label>
            <input type="email" class="form-control" id="Input1" placeholder="Happy@gmail.com" v-model="formData.email_id" required>
          </div>
          <div class="mb-3">
            <label for="Input2" class="form-label">Password</label>
            <input type="password" class="form-control" id="Input2" v-model="formData.password" maxlength="10" required>
          </div>

          <label class="form-label d-block">Are you a patient?</label>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="role" id="yes" value="yes" v-model="formData.role" required>
    <label class="form-check-label" for="yes">Yes</label>
  </div>

  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="role" id="no" value="no" v-model="formData.role" required>
    <label class="form-check-label" for="no">No</label>
  </div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary w-100">Login</button>
            <p class="mt-3 mb-0 text-muted">Don't have an account? <a href="/register">Sign up</a></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

</template>

<style scoped>

     .navbar-brand {
      font-family: 'Poppins', sans-serif;
      font-weight: 600;
      font-size: 1.6rem;
      letter-spacing: 1px;
      color: #0d6efd !important; 
      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
      transition: transform 0.3s ease, color 0.3s ease;
    }
    .navbar-brand:hover {
      color: grey !important;
      transform: scale(1.05);
    }
    .navbar {
      padding: 12px 20px;
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

    .icon-circle {
    width: 100px;
    height: 100px;
    background: #f1f5ff;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
  }
  .icon-circle:hover{
    transform: scale(1.05);
    transition: transform 0.3s ease;
    color:#0d6efd
  }
  .icon-circle img {
    width: 60px;
    height: 60px;
    object-fit: contain;
  }

</style>