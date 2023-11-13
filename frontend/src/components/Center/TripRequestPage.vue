<template>
    <div class="fill">
        <Sidebar />
      <div :style="{ 'margin-left': sidebarWidth }">
        <router-view />
      </div>
      <div class="main-content" :style="{ 'margin-left': sidebarWidth }">
          <div class="tripinfo">
              <span><h2>{{ from }}  -> {{ to }}</h2> </span>
              <div class="triptitle"><h3>{{ props.date }}  {{ props.time }}</h3></div>
          </div>
  
          <!-- <div class="trip-info">
              <div><strong>To:</strong> {{ props.to }}</div>
              <div><strong>Departure Time:</strong> {{ props.departureTime }}</div>
              <div><strong>Luggage Count:</strong> {{ props.luggageCount }}</div>
              <div><strong>Comments:</strong> {{ props.comments }}</div>
          </div> -->
  
          <div class="left">
              <h4>Group members</h4>
          </div>
  
          <div class="table-responsive">
              <table class="table table-striped bdr">
                  <thead>
                      <tr>
                          <th scope="col" class="column">Name</th>
                          <th scope="col" class="column">Email</th>
                          <th scope="col" class="column">Phone Number</th>
                          <th scope="col" class="column">Luggage</th>
                          <th scope="col" class="column"></th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="participant in participants" :key="participant.id">
                      <td>{{ participant.name }}</td>
                      <td>{{ participant.email }}</td>
                      <td>{{ participant.phone }}</td>
                      <td>{{ participant.luggage }}</td>
                      <td></td>
                  </tr>
                  </tbody>
              </table>
          </div>
  
          <div class="left">
              <h4>Join requests</h4>
          </div>
  
          <div class="table-responsive">
              <table class="table table-striped bdr">
                  <thead>
                      <tr>
                          <th scope="col" class="column">Name</th>
                          <th scope="col" class="column">Email</th>
                          <th scope="col" class="column">Phone Number</th>
                          <th scope="col" class="column">Luggage</th>
                          <th scope="col" class="column"></th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="participant in participants" :key="participant.id">
                      <td>{{ participant.name }}</td>
                      <td>{{ participant.email }}</td>
                      <td>{{ participant.phone }}</td>
                      <td>{{ participant.luggage }}</td>
                      <td>
                          <button>Accept</button>
                          <button>Reject</button>
                      </td>
                  </tr>
                  </tbody>
              </table>
          </div>
  
          <div class="left">
              <h4>Confirmation requests</h4>
          </div>
  
          <div class="table-responsive">
              <table class="table table-striped table-responsive bdr">
                  <thead>
                      <tr>
                          <th scope="col" class="column">Name</th>
                          <th scope="col" class="column">Email</th>
                          <th scope="col" class="column">Phone Number</th>
                          <th scope="col" class="column">Luggage</th>
                          <th scope="col" class="column"></th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="participant in participants" :key="participant.id">
                      <td>{{ participant.name }}</td>
                      <td>{{ participant.email }}</td>
                      <td>{{ participant.phone }}</td>
                      <td>{{ participant.luggage }}</td>
                      <td>
                          Sent
                      </td>
                  </tr>
                  </tbody>
              </table>
          </div>
  
  
      </div>
      </div>
  </template>
  
  
  <script setup>
    import { defineProps, onMounted, reactive } from 'vue';
    import Sidebar from './../Sidebar/Sidebar.vue'
    import { sidebarWidth } from './../Sidebar/state.js'
      const props = defineProps([
          'id'
      ])
  
      const from = "Princeton"
      const to = "EWR"
  
      const participants = reactive([
          {id: 0, name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
          {id: 1, name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
      ])
  
      onMounted(()=> {
          // participants.values = props.participants
      });
  
      function acceptJoinRequest() {
  
      }
  
      function rejectJoinRequest() {
  
      }
  </script>
  
  
  <style scoped>
  
  .bdr {
      border-radius: 10px;
      overflow: hidden;
  }
  
  .fill {
      /* height: 100vh;
      box-sizing: border-box; */
      /* position:absolue (or fixed);
      width:100%;
      height:100%;
      top: 0;
      left: 0; */
      /* display: table-cell; */
      align-items: stretch;
  }
  
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