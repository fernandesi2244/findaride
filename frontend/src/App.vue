<template>
<div id="app" class="box">
    <nav class="navbar">
        <div class="nav-content">
        <div v-if="isLoggedIn">
          <span class = text-size><router-link to="/">findaride</router-link></span>
        </div>
        <div v-else>
          <span class = text-size><router-link to="/">findaride</router-link></span>
        </div>
            <div class="right">
                <router-link to="/about">About</router-link>
                <router-link to="/dashboard">Dashboard</router-link>
                <router-link to="/profile">Profile</router-link>
            </div>
        </div>
    </nav>

    <router-view class="full-height pt-8" style="overflow: auto;"/>
</div>
</template>
<script>
import axios from 'axios';
import { endpoints } from './common/endpoints.js'

export default {
  data() {
    return {
      isLoggedIn: false
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    async checkLoginStatus() {
      const endpoint = endpoints['is-logged-in'];
      const response = await axios.get(endpoint);
      this.isLoggedIn = response.data.isAuthenticated;
    }
  }
};
</script>


<style>
#app {
  font-family: 'Roboto', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #F4F4F8;
}

.box {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.full-height {
  height: 100%;
}

.navbar {
  background: rgb(45, 137, 237);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  color: white;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar a {
  font-weight: bold;
  color: white;
  text-decoration: none;
  padding: 0 15px;
  transition: color 0.3s ease;
}

.navbar a:hover {
  color: #d1e8ff;
}

.text-size {
  font-size: 24px;
}

.right {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0.5rem 1rem;
  }

  .nav-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .right {
    justify-content: flex-start;
    width: 100%;
    margin-top: 10px;
  }

  .navbar a {
    padding: 5px 0;
    display: block;
  }
}

</style>
