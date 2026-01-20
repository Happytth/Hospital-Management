<template>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <!-- Hamburger button to toggle sidebar -->
    <button class="btn btn-outline-light me-2" @click="sidebarOpen = true" aria-label="Toggle sidebar">
      <span class="navbar-toggler-icon"></span>
    </button>

    <a class="navbar-brand" href="#">Hap!Care</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">

      </ul>

      <ul class="navbar-nav">
        <li class="nav-item">
          
        </li>
      </ul>
    </div>
  </div>
</nav>


<div v-if="sidebarOpen" class="sidebar-backdrop" @click.self="sidebarOpen = false">
  <div class="sidebar">
    <div class="sidebar-header mb-4 d-flex align-items-center">
      <img src="https://img.icons8.com/color/96/medical-doctor.png" alt="Avatar" class="sidebar-avatar me-3" />
      <div>
        <div class="sidebar-title">Admin Panel</div>
        <div class="sidebar-subtitle text-muted">Hap!Care</div>
      </div>
      <button class="btn-close ms-auto" @click="sidebarOpen = false"></button>
    </div>
    <!-- <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchquery">
        <input
          class="form-control me-2 search-input"
          type="search"
          v-model="query"
          placeholder="Search doctors,patients,etc."
          required
        />
        <button class="btn search-btn" type="submit">Search</button>
      </form>
    </div> -->
    <ul class="list-unstyled mt-2">
      <li>
        <RouterLink to="/admin_dashboard" class="sidebar-link">
          <i class="bi bi-person-badge sidebar-icon"></i> Dashboard
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/admin_doctors" class="sidebar-link">
          <i class="fa-solid fa-user-doctor sidebar-icon"></i> Doctors
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/admin_patients" class="sidebar-link">
          <i class="bi bi-people sidebar-icon"></i> Patients
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/admin_department" class="sidebar-link">
          <i class="bi bi-calendar-check sidebar-icon"></i> Departments
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/admin_appointment" class="sidebar-link">
          <i class="bi bi-hospital sidebar-icon"></i> Appointments 
        </RouterLink>
      </li>
  
      <li>
        <button class="btn sidebar-logout-btn" data-bs-toggle="modal" data-bs-target="#logoutModal">
          <i class="bi bi-box-arrow-right sidebar-icon"></i> Logout
        </button>
      </li>
    </ul>
  </div>
</div>



</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: "Navbar",
  data() {
    return {
      query: "",
      sidebarOpen: false,
    };
  },
  methods: {
    searchquery() {
      
      this.$emit("search", this.query);
    },
  },
};
</script>


<style scoped>
.navbar-brand {
      font-family: 'Poppins', sans-serif;
      font-weight: 600;
      font-size: 1.6rem;
      letter-spacing: 1px;
      color: #c4d4eb !important; 
      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
      transition: transform 0.3s ease, color 0.3s ease;
    }
.navbar-brand:hover {
      color: grey !important;
      transform: scale(1.05);
    }
.navbar {
  background: radial-gradient(circle at center,rgb(59, 59, 77),rgba(0, 0, 0, 0));
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  padding: 12px 20px;
}

.search-container {
  width: 100%;
  padding: 12px 2rem 0 2rem;
  box-sizing: border-box;
}

.search-form {
  display: flex;
  width: 100%;
}

.search-input {
  flex: 1;
  min-width: 0;
}

.search-btn {
  margin-left: 0.5rem;
  white-space: nowrap;
  background: rgb(188, 178, 163);
}

.search-btn:hover {
  background-color: #333 !important;
}

.sidebar-backdrop {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(17,39,54,0.25);
  z-index: 1050;
  display: flex; align-items: stretch;
  transition: background 0.3s;
}

.sidebar {
  width: 290px;
  max-width: 85vw;
  background: repeating-linear-gradient(125deg,#e6f0fa,#b2d8f7,white );
  height: 100vh;
  box-shadow: 3px 0 18px 0 rgba(0,20,80,0.14);
  border-radius: 0 15px 15px 0;
  position: relative;
  animation: slideIn 0.2s;
  padding: 20px 0 0 0;
  overflow-y: auto;
}

@keyframes slideIn {
  from { transform: translateX(-110%);}
  to   { transform: translateX(0);}
}

.sidebar-header {
  padding: 0 2rem 1rem 2rem;
  border-bottom: 1px solid #e8e8e8;
}

.sidebar-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  box-shadow: 0 3px 12px rgba(91,146,204,0.12);
  margin-right: 18px;
  object-fit: cover;
}

.sidebar-title {
  font-weight: 700;
  font-size: 1.08rem;
  color: #2679e5;
}
.sidebar-subtitle {
  font-size: 0.85rem;
  color: #558ad9;
}

.sidebar-link {
  display: flex;
  align-items: center;
  padding: 1rem 2.5rem;
  font-weight: 600;
  color: #2173cf;
  border-radius: 8px;
  text-decoration: none;
  font-size: 1rem;
  margin-bottom: 8px;
  transition: background 0.16s, color 0.16s, transform 0.1s;
}

.sidebar-link:hover {
  background: #eaf6ff;
  color: #134172;
  transform: scale(1.04) translateX(4px);
}

.sidebar-icon {
  font-size: 1.2rem;
  margin-right: 14px;
  color: #2c8cef;
  transition: color 0.18s;
}

.sidebar-logout-btn {
  display: flex;
  align-items: center;
  width: 90%;
  margin: 1rem auto 0 auto;
  background: #ed6a5a;
  color: #fff;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  padding: 10px 16px;
  border: none;
  transition: background 0.2s;
}

.sidebar-logout-btn:hover {
  background: #d95d43;
  color: #fff;
}
</style>
