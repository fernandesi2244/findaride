<template>
    <main>
      <Sidebar />
      <div :style="{ 'margin-left': sidebarWidth }">
        <router-view />
      </div>
      <div class="main-content" :style="{ 'margin-left': sidebarWidth }">
        <div>
            <h1>Welcome, User</h1>
            How it works <br>  
            1. Add new trip request
            2. Form your group
            3. Monitor people trying to join your group
        </div>
      </div>
    </main>
  </template>
  
  
  <script setup>
 import Sidebar from './../Sidebar/Sidebar.vue'
 import { sidebarWidth } from './../Sidebar/state.js'

  </script>
  
  
  <style scoped>
  
  .column {
      width: 15%
  }
  
  .columnend {
      
  }
  
  .left {
      text-align: left;
  }
  
  .tripinfo {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
  }
  
  .triptitle {
      /* width: 100px; */
      display: inline-block;
  }
  
  .modal {
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    width: 90%;
    max-width: 400px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  input, textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  textarea {
    resize: vertical;
  }
  
  .btn {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .cancel-btn {
    background: #e74c3c;
    color: #fff;
  }
  
  .btn:not(.cancel-btn) {
    background: #2ecc71;
    color: #fff;
  }
  
  .btn:not(.cancel-btn):hover {
    background: #27ae60;
  }
  </style>