<template>
    <div class="home">
        <div class="container mx-auto row d-flex align-items-center px-4">
          <div class="col-xl px-4">
            <div style="max-width: 750px" class="mx-auto">
              <h3>Welcome to findaride!</h3>
              <h4>Your one-stop solution to find affordable, timely rides back home.</h4>
              <p class="tagline">
                Are you tired of the hassle in finding a ride? Our platform revolutionizes the way people connect
                for shared journeys. Whether you're heading to work, a concert, or just a weekend getaway, findaride
                is here to help.
              </p>
              <button @click="goToLogin" class="btn-login">
                Get Started
              </button>
            </div>
          </div>
          <div class="col-xl">
            <img class="img-fluid" src="static/home.svg" alt="Rideshare Image">
          </div>
        </div>
    </div>
  </template>

  <script>
  export default {
    name: 'HomeScreen',
    methods: {
      goToLogin() {
        window.location.href = '/dashboard/';
      },
    },
  };
  </script>
<style scoped>
.home-content {
  padding: 20px;
  text-align: center;
}

h3 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.tagline {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.btn-login {
  font-size: 1.2rem;
  color: #fff;
  background-color: #4CAF50;
  border: none;
  border-radius: 5px;
  padding: 15px 25px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.btn-login:hover {
  background-color: #3e8e41;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .home-content {
    padding: 10px;
  }

  h3 {
    font-size: 1.5rem;
  }

  .tagline {
    font-size: 1rem;
  }
}
</style>