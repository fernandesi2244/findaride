<template>
  <div class="dashboard">
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
                    <div><strong>Comments:</strong> {{ trip.comments }}</div>
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
                    <div><strong>Departure Date:</strong> {{ getDate(tripRequest.departure_time) }}</div>
                    <div><strong>Departure Time:</strong> {{ getTime(tripRequest.departure_time) }}</div>
                    <div><strong>Luggage Count:</strong> {{ tripRequest.num_luggage_bags }}</div>
                    <div><strong>Comments:</strong> {{ tripRequest.comments }}</div>
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
              <div><strong>Group:</strong> {{ conf.groupName }}</div>
              <div><strong>Date:</strong> {{ conf.trip.date }}</div>
              <div><strong>From:</strong> {{ conf.trip.from }}</div>
              <div><strong>To:</strong> {{ conf.trip.to }}</div>
              <div><strong>Departure Time:</strong> {{ conf.trip.departureTime }}</div>
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
  
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import AddTripForm from '../components/AddTripForm.vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'

const user = reactive({
  first_name: "", 
  id: -1,
});

const trips = ref([]);
const tripRequests = ref([]);

onMounted(async () => {
  await getUserInfo();
  await getUserTrips();
});

/*
const tripRequests = reactive([
    { id: 1, departure_location: 'New York', arrival_location: 'Los Angeles', departure_time: '10:00 AM', num_luggage_bags: '2 Bags', comments: 'No special requirements', status: 'Pending' },
])*/
const confRequests = reactive([
    {
        id: 0,
        groupName: "group1",
        trip: {
            members: ["Dylan"],
            date: "Oct 31",
            from: "a",
            to: "b",
            departureTime: "10:10AM",
            luggageCount: 3,
            joinRequests: [
                {
                    tripid: 1,
                    id: 0,
                    name: "Dylan",
                    departureTime: "10:30AM",
                    luggageCount: 3,
                }
            ]
        }
    }
])
const showTripForm = ref(false);
const pendingTrips = ref([]);
  

// function acceptJoin(id) {
//     const joinI = joinRequests
//     const index = trips.findIndex(trip => trip.id = )
//     displayedTrip.members.push()
// }

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

  let departure_time = `${newTripRequest.departureDate.substring(2)} ${newTripRequest.departureTime}:00`;


  let data = {
    "departure_time": departure_time,
    "num_luggage_bags": newTripRequest.luggageCount,
    "user": user.id,
    "departure_location": departure,
    "arrival_location": arrival,
  }

  const endpoint = endpoints["tripRequest"];
  const response = await axios.post(endpoint, data);
  
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

function removeTripRequest(id) {
  const index = tripRequests.findIndex(trip => trip.id === id);
  if (index !== -1) {
    tripRequests.splice(index, 1);
  }
}

function acceptConfirmationRequest(id) {
    const index = confRequests.findIndex(conf => conf.id === id);
    if (index !== -1) {
        trips.push(confRequests[index].trip)
        confRequests.splice(index, 1);
    }
}

function rejectConfirmationRequest(id) {
    const index = confRequests.findIndex(conf => conf.id === id);
    if (index !== -1) {
        confRequests.splice(index, 1);
    }
}
function rejectTrip(id) {
  if (confirm('Are you sure you want to reject this trip?')) {
    const index = pendingTrips.value.findIndex(trip => trip.id === id);
    if (index !== -1) {
      pendingTrips.value.splice(index, 1);
      console.log('Rejected trip with ID:', id);
    } else {
      console.error('Trip not found');
    }
  }
}

function getDate(dateString) {
  // TODO: figure out timezone?
  let date = new Date(dateString);
  return date.toLocaleDateString();
}
function getTime(dateString) {
  let date = new Date(dateString);
  return date.toLocaleTimeString();
}

function cleanLocation(location) {
  let tokens = location.split(",");
  tokens.splice(-1);

  return tokens.join(",");
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
