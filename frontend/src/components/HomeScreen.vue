<template>
    <div class="home">
        <div class="container mx-auto row d-flex align-items-center px-4">
          <div class="col-xl px-4">
            <div style="max-width: 750px" class="mx-auto">
              <h3>Welcome to findaride!</h3>
              <h4>Connect with fellow students for shared, budget-friendly rides.</h4>
              <p class="tagline">
                Looking for a ride without breaking the bank? findaride makes it easy to connect with
                others who are heading in the same direction. Whether it's daily commutes, trips to events,
                or weekend adventures, we bring you together for a more economical and sociable ride.
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
<style >
body {
  margin: 0;
  padding: 0;
  background-color: #F4F4F8;
  font-family: 'Roboto', Arial, sans-serif;
  color: #4A4A4A; 
}
.home {
  padding: 20px;
  text-align: center;
}

h3, h4, .tagline {
  margin-bottom: 15px;
}

h3 {
  font-size: 2.5rem;
  color: #333;
}

h4 {
  font-size: 1.8rem;
  color: #4A4A4A;
}

.tagline {
  font-size: 1.3rem;
  color: #666;
  line-height: 1.6;
}

.btn-login {
  font-size: 1.3rem;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  padding: 15px 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login:hover {
  background-color: #0056b3;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .home {
    padding: 15px;
  }

  h3 {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1.1rem;
  }

  .btn-login {
    padding: 12px 24px;
  }
}

.img-fluid {
  max-width: 100%;
  height: auto;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.col-xl {
  padding: 15px;
}

</style>
