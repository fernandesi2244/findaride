<template>
    <div class="dashboard">
      <Sidebar />
      <div :style="{ 'margin-left': sidebarWidth }">
        <router-view />
      </div>
  
      <div class="main-content" :style="{ 'margin-left': sidebarWidth }">
      <h1>Welcome back, {{ user.first_name }}!</h1>
      
      <div class="trips-section">
        <div class="section-header">
          <h2>Your Trips</h2>
        </div>
        
        <div v-if="trips.length">
          <ul class="list-reset">
            <li v-for="trip in trips" :key="trip.id" class="card">
              <button @click="clickTrip(trip)">
                  <div class="trip-info">
                      <div><strong>From:</strong> {{ cleanLocation(trip.departure_location) }}</div>
                      <div><strong>To:</strong> {{ cleanLocation(trip.arrival_location) }}</div>
                      <div><strong>Departure Date:</strong> {{ getDate(trip.departure_time) }}</div>
                      <div><strong>Departure Time:</strong> {{ getTime(trip.departure_time) }}</div>
                      <div><strong>Luggage Count:</strong> {{ trip.num_luggage_bags }}</div>
                  </div>
              </button>
            </li>
            <div v-if="showTrip"> 
                  <li v-for="join in displayedTrip.joinRequests" :key="join.id" class="card">
                      <div><strong>Name:</strong> {{ join.name }}</div>
                      <div><strong>Departure Time:</strong> {{ join.departureTime }}</div>
                      <div><strong>Luggage Count:</strong> {{ join.luggageCount }}</div>
                      <!-- <button @click="acceptJoin(join)">Accept</button>
                      <button @click="rejectJoin(join.id)">Reject</button> -->
                  </li>
              </div>
          </ul>
        </div>
        <div v-else>
          <p class="no-trips-message">You haven't planned any trips yet.</p>
        </div>
  
        <div class="section-header">
          <h2>Your Trip Requests</h2>
          <button @click="showTripForm = true" class="btn add-trip-btn">+ Add New Trip Request</button>
        </div>
        <div v-if="tripRequests.length">
          <ul class="list-reset">
            <li v-for="tripRequest in tripRequests" :key="tripRequest.id" class="card">
                  <div class="trip-info">
                      <div><strong>From:</strong> {{ cleanLocation(tripRequest.departure_location) }}</div>
                      <div><strong>To:</strong> {{ cleanLocation(tripRequest.arrival_location) }}</div>
                      <div><strong>Earliest departure time:</strong> {{ getDateTime(tripRequest.earliest_departure_time) }}</div>
                      <div><strong>Latest departure time:</strong> {{ getDateTime(tripRequest.latest_departure_time) }}</div>
                      <div><strong>Luggage count:</strong> {{ tripRequest.num_luggage_bags }}</div>
                      <div><strong>Comments:</strong> {{ tripRequest.comment }}</div>
                  </div>
              <button @click="removeTripRequest(tripRequest.id)" class="btn btn-danger">Remove</button>
            </li>
          </ul>
        </div>
        <div v-else>
          <p class="no-trips-message">You haven't planned any trips yet.</p>
        </div>
  
        <div class="section-header">
          <h2>Your Confirmation Requests</h2>
        </div>
        <div v-if="confRequests.length">
          <ul class="list-reset">
            <li v-for="conf in confRequests" :key="conf.id" class="card">
              <div class="trip-info">
                <div><strong>Date:</strong> {{ conf.trip.date }}</div>
                <div><strong>From:</strong> {{ conf.trip.from }}</div>
                <div><strong>To:</strong> {{ conf.trip.to }}</div>
                <div><strong>Departure Time:</strong> {{ getTime(conf.trip.departure_time) }}</div>
                <div><strong>Luggage Count:</strong> {{ conf.trip.luggageCount }}</div>
              </div>
              <button @click="acceptConfirmationRequest(conf.id)" class="btn btn-primary">Join</button>
              <button @click="rejectConfirmationRequest(conf.id)" class="btn btn-danger">Reject</button>
            </li>
          </ul>
        </div>
        <div v-else>
          <p class="no-trips-message">You haven't planned any trips yet.</p>
        </div>
      </div>
  
      <AddTripForm v-if="showTripForm" @addTripRequest="addTripRequest" @close="showTripForm = false" />
  
    </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import AddTripForm from '../components/AddTripForm.vue';
  import { endpoints } from '../common/endpoints.js';
  import { axios } from '../common/axios_service.js'
  import Sidebar from '../components/Sidebar/Sidebar.vue'
  import { sidebarWidth } from '../components/Sidebar/state.js'
  
  const user = reactive({
    first_name: "", 
    id: -1,
  });
  
  const trips = ref([]);
  const tripRequests = ref([]);
  const confRequests = ref([]);
  
  onMounted(async () => {
    await getUserInfo();
    await getUserTrips();
    await getConfirmationRequests();
  });
  
  const showTripForm = ref(false);
  const pendingTrips = ref([]);
  
  function clickTrip(trip) {
      showTrip.value = true
      displayedTrip.value = trip
  }
  
  function addTrip(newTrip) {
    trips.push(newTrip);
    showTripForm.value = false;
  }
  
  function removeTrip(id) {
    const index = trips.findIndex(trip => trip.id === id);
    if (index !== -1) {
      trips.splice(index, 1);
    }
  }
  
  function joinTrip(id) {
    // Implement the functionality to join a trip here.
    // This could involve updating the trip's status or adding the user to the trip's list of participants.
    console.log('Joined trip with ID:', id);
  }
  
  async function addTripRequest(newTripRequest) {
  
    //tripRequests.value.push(newTripRequest);
  
    let departure = {
      "address": newTripRequest.from,
      "postal_code": newTripRequest.fromPostalCode,
    }
    let arrival = {
      "address": newTripRequest.to,
      "postal_code": newTripRequest.toPostalCode,
    }
  
    // NOTE: why are we taking the substring again?
    let earliest_departure_time = new Date(newTripRequest.earliestDepartureTime).toUTCString();
    let latest_departure_time = new Date(newTripRequest.latestDepartureTime).toUTCString();
  
    let data = {
      "earliest_departure_time": earliest_departure_time,
      "latest_departure_time": latest_departure_time,
      "num_luggage_bags": newTripRequest.luggageCount,
      "user": user.id,
      "departure_location": departure,
      "arrival_location": arrival,
      "comment": newTripRequest.comment,
    }
  
    const endpoint = endpoints["tripRequest"];
    try {
      await axios.post(endpoint, data);
    } catch (error) {
      alert(formatError(error.response.data.error));
      return;
    }
    
    showTripForm.value = false;
  
    getUserTrips();
  }
  
  async function getUserInfo() {
    const endpoint = endpoints["me"];
    const response = await axios.get(endpoint);
    Object.assign(user, response.data);
  }
  
  async function getUserTrips() {
    const endpoint = `${endpoints["userTrips"]}${user.id}/`;
    const response = await axios.get(endpoint);
    tripRequests.value = response.data.trip_requests;
    trips.value = response.data.trips;
  }
  
  async function getConfirmationRequests() {
    const endpoint = `${endpoints["confirmationRequests"]}`;
    const response = await axios.get(endpoint);
    confRequests.value = response.data;
  }
  
  async function removeTripRequest(id) {
    const index = tripRequests.value.findIndex(trip => trip.id === id);
    if (index !== -1) {
      const endpoint = `${endpoints["deleteTripRequest"]}${id}/`;
      try {
        axios.delete(endpoint);
        tripRequests.value.splice(index, index + 1);
      } catch (error) {
        alert(formatError(error.response.data.error));
        return;
      }
    }
  }
  
  function acceptConfirmationRequest(id) {
      const index = confRequests.findIndex(conf => conf.id === id);
      if (index !== -1) {
        const endpoint = `${endpoints["confirmationRequest"]}${id}/accept/`;
        try {
          axios.delete(endpoint);
          getUserTrips();
          getConfirmationRequests();
        } catch (error) {
          alert(formatError(error.response.data.error));
          return;
        }
      }
  }
  
  function rejectConfirmationRequest(id) {
      const index = confRequests.findIndex(conf => conf.id === id);
      if (index !== -1) {
        const endpoint = `${endpoints["confirmationRequest"]}${id}/reject/`;
        try {
          axios.delete(endpoint);
          getUserTrips();
          getConfirmationRequests();
        } catch (error) {
          alert(formatError(error.response.data.error));
          return;
        }
      }
  }
  
  function getDate(dateString) {
    return new Date(dateString).toLocaleDateString();
  }
  
  function getTime(dateString) {
    return new Date(dateString).toLocaleTimeString();
  }
  
  function getDateTime(dateString) {
    return new Date(dateString).toLocaleString();
  }
  
  function cleanLocation(location) {
    let tokens = location.split(",");
    tokens.splice(-1);
  
    return tokens.join(",");
  }
  
  function formatError(errorDict) {
    if (typeof errorDict === "string") {
      return errorDict;
    }
    try {
      let errorString = "";
      for (const [key, value] of Object.entries(errorDict)) {
        errorString += `${value}\n`;
      }
      return errorString;
    } catch (error) {
      return JSON.stringify(errorDict);
    }
  }
  
  </script>
  
  <style scoped>
  .dashboard {
    max-width: 1000px;
    margin: 40px auto;
    padding: 20px;
    font-family: 'Roboto', sans-serif;
  }
  
  h1 {
    font-size: 2em;
    margin-bottom: 20px;
  }
  
  h2 {
    font-size: 1.5em;
    margin-bottom: 15px;
  }
  
  .trips-section {
    margin-bottom: 30px;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .list-reset {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .card {
    padding: 10px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .trip-info {
    max-width: 60%;
  }
  
  .status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
    color: #fff;
  }
  
  .status-active {
    background-color: #4CAF50;
  }
  
  .status-inactive {
    background-color: #f44336;
  }
  
  .no-trips-message {
    font-style: italic;
    color: #666;
  }
  
  .btn {
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
  }
  
  .btn:hover {
    opacity: 0.9;
  }
  
  .add-trip-btn {
    background-color: #008CBA;
    color: #fff;
  }
    .pending-requests {
      max-width: 1000px;
      margin: 40px auto;
      padding: 20px;
      font-family: 'Roboto', sans-serif;
    }
    
    h1 {
      font-size: 2em;
      margin-bottom: 20px;
    }
    
    .list-reset {
      list-style-type: none;
      padding: 0;
      margin: 0;
    }
    
    .card {
      padding: 10px;
      border: 1px solid #ccc;
      margin-bottom: 10px;
      border-radius: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .trip-info {
      max-width: 60%;
    }
    
    .no-trips-message {
      font-style: italic;
      color: #666;
    }
    
    .btn {
      padding: 8px 15px;
      border: none;
      border-radius: 5px;
      font-size: 1em;
      cursor: pointer;
    }
    
    .btn:hover {
      opacity: 0.9;
    }
    
    .btn-primary {
      background-color: #4CAF50;
      color: #fff;
    }
    
    .btn-danger {
      background-color: #f44336;
      color: #fff;
    }
    
  </style>
  