<template>
    <main>
      <!-- <img alt="Vue logo" class="logo" src="/static/logo.svg" width="125" height="125" /> -->
  
      <div class="greetings">
          <h1 class="dark-green">findaride</h1>
          <h3>Join us and find a ride!</h3>
      </div>
  
      <div class="signup-container">
          <form @submit.prevent="submitSignUp">
              <input type="text" v-model="email" placeholder="Email" autocomplete="email" required>
              <input type="text" v-model="phone_number" placeholder="Phone Number">
              <input type="text" v-model="first_name" placeholder="First Name" required>
              <input type="text" v-model="last_name" placeholder="Last Name" required>
              <input type="password" v-model="password" placeholder="Password" required>
              <input type="password" v-model="confirm_password" placeholder="Confirm Password" required>
              <button type="submit">Sign up</button>
          </form>
          <div class="log-in">
              <p>Already have an account?</p>
              <a href="/login">Log in</a>
          </div>
      </div>
    </main>
  </template>
  
  <script setup>
    import { ref } from 'vue';
    import { axios } from "../common/axios_service.js";
    import { endpoints } from "../common/endpoints.js";
    import { useRouter } from 'vue-router';
  
    const router = useRouter();
    
    const email = ref('');
    const phone_number = ref('');
    const first_name = ref('');
    const last_name = ref('');
    const password = ref('');
    const confirm_password = ref('');
  
    async function submitSignUp() {
      const endpoint = endpoints["signup"];
    
      const data = {
        email: email.value,
        phone_number: phone_number.value,
        first_name: first_name.value,
        last_name: last_name.value,
        password: password.value,
        confirm_password: confirm_password.value
      };
  
      try {
        const response = await axios.post(endpoint, data);
        console.log(response);
        router.push('/login'); // Redirect to login after successful registration
      } catch (error) {
        console.log(error);
      }
    }
  </script>
  
  <style scoped>
  main {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
  }
  
  .logo {
      display: block;
      margin: 0 auto 2rem;
  }
  
  .signup-container {
      display: flex;
      flex-direction: column;
      justify-content: top;
      align-items: center;
      height: 100vh;
      margin-top: 2rem;
  }
  
  input, textarea {
      width: 25rem;
      border: none;
      padding: 0.5rem;
      margin: 0.5rem 0;
      outline: 0;
      border-bottom: 0.1rem solid var(--color-text);
      background-color: var(--color-light-green);
  }
  
  button {
      width: 25rem;
      padding: 0.5rem;
      border: none;
      border-radius: 5rem;
      background-color: var(--color-main-green);
      color: black;
      cursor: pointer;
      margin-top: 1rem;
  }
  
  .log-in {
      margin-top: 5rem;
      display: inline-block;
  }
  
  a {
      margin-left: 0.5rem;
      color: var(--color-main-green);
      text-decoration: none;
  }
  
  h1 {
    font-weight: 500;
    font-size: 2.6rem;
  }
  
  h3 {
    font-size: 1.2rem;
    font-weight: 400;
  }
  
  .greetings h1, .greetings h3 {
    text-align: center;
  }
  </style>
  