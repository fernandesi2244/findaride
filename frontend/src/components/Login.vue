<template>
    <main>
      <!-- <img alt="Vue logo" class="logo" src="/static/logo.svg" width="125" height="125" /> -->
  
      <div class="greetings">
        <h1 class="dark-green">findaride</h1>
        <h3>Go find a ride!</h3>
        <!-- Hearts in action -->
      </div>
  
      <div class="login-container">
          <form @submit.prevent="submitLogIn">
              <input type="text" v-model="email" id="email" placeholder="Email" autocomplete="email" required>
              <br />
              <input type="password" v-model="password" id="password" placeholder="Password" autocomplete="current-password" required>
              <br />
              <button type="submit">Log in</button>
          </form>
          <div class="sign-up">
              <p>Don't have an account yet?</p>
              <a href="/signup">Create one</a>
          </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { axios } from "../common/axios_service.js";
  import { endpoints } from "../common/endpoints.js";
  import { useRouter, useRoute } from 'vue-router'
  
  const router = useRouter()
  const route = useRoute()
  
  const email = ref('')
  const password = ref('')
  
  async function submitLogIn() {
    const endpoint = endpoints["login"];
  
    const data = {
      email: email.value,
      password: password.value
    }
  
    try {
      const response = await axios.post(endpoint, data);
      console.log(response);
      if (route.query.redirect) {
        router.push(route.query.redirect)
      } else {
        router.push('/')
      }
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
  
  .login-container {
      display: flex;
      flex-direction: column;
      justify-content: top;
      align-items: center;
      height: 100vh;
      margin-top: 2rem;
  }
  
  input,
  textarea {
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
  
  .sign-up {
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
    top: -10px;
  }
  
  h3 {
    font-size: 1.2rem;
    font-weight: 400;
  }
  
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
  </style>
  