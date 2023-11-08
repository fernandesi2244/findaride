<template>
    <div class="home">
        <div class="home-overlay"></div>
        <div class="home-content">
            <h1>Welcome to FindARide!</h1>
            <p class="tagline">
            Your one-stop solution to find affordable, timely rides back home.
            </p>
            <button @click="goToLogin" class="btn-login">
            Log In to Find a Ride
        </button>
        </div>
    </div>
  </template>

  <script>
  export default {
    name: 'HomeScreen',
    methods: {
      goToLogin() {
        window.location.href = '/accounts/login/';
      },
    },
  };
  </script>
<style scoped>
.btn-login {
  font-size: 1rem;
  color: #fff;
  background-color: #4CAF50;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
</style>