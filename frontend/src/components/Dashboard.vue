<template>
  <div class="dashboard">
    <h1>Welcome back, Placeholder!</h1>
    
    <div class="trips-section">
      <div class="section-header">
        <h2>Your Trips</h2>
      </div>
      
      <div v-if="trips.length">
        <ul class="list-reset">
          <li v-for="trip in trips" :key="trip.id" class="card">
            <button @click="clickTrip">
                <div class="trip-info">
                    <div><strong>From:</strong> {{ trip.from }}</div>
                    <div><strong>To:</strong> {{ trip.to }}</div>
                    <div><strong>Departure Time:</strong> {{ trip.departureTime }}</div>
                    <div><strong>Luggage Count:</strong> {{ trip.luggageCount }}</div>
                    <div><strong>Comments:</strong> {{ trip.comments }}</div>
                </div>
            </button>
          </li>
          <div v-if="showTrip"> 
                <li v-for="join in displayedTrip.joinRequests" :key="join.id" class="card">
                    <div><strong>Name:</strong> {{ join.name }}</div>
                    <div><strong>Departure Time:</strong> {{ join.departureTime }}</div>
                    <div><strong>Luggage Count:</strong> {{ join.luggageCount }}</div>
                </li>
            </div>
        </ul>
      </div>
      <div v-else>
        <p class="no-trips-message">You haven't planned any trips yet.</p>
      </div>

      <div class="section-header">
        <h2>Your Trip Requests</h2>
        <button @click="showAddTripRequest = true" class="btn add-trip-btn">+ Add New Trip Request</button>
      </div>
      <div v-if="tripRequests.length">
        <ul class="list-reset">
          <li v-for="tripR in tripRequests" :key="tripR.id" class="card">
            <div class="trip-info">
              <div><strong>From:</strong> {{ tripR.from }}</div>
              <div><strong>To:</strong> {{ tripR.to }}</div>
              <div><strong>Departure Time:</strong> {{ tripR.departureTime }}</div>
              <div><strong>Luggage Count:</strong> {{ tripR.luggageCount }}</div>
              <div><strong>Comments:</strong> {{ tripR.comments }}</div>
            </div>
            <button @click="removeTripRequest(tripR.id)" class="btn btn-danger">Remove</button>
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

    <AddTripForm v-if="showAddTripRequest" @addTripRequest="addTripRequest" @close="showAddTripRequest = false" />

  </div>
  
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import AddTripForm from '../components/AddTripForm.vue';
  
  
const trips = reactive([]);
const showTrip = ref(false);
const displayedTrip = ref();
const tripRequests = reactive([
    { id: 1, from: 'New York', to: 'Los Angeles', departureTime: '10:00 AM', luggage: '2 Bags', comments: 'No special requirements', status: 'Pending' },
])
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
                    id: 0,
                    name: "Dylan",
                    departureTime: "10:30AM",
                    luggageCount: 3,
                }
            ]
        }
    }
])
const showAddTripRequest = ref(false);
const pendingTrips = ref([]);
  
onMounted(() => {
    tripRequests.value = [
        { id: 1, from: 'New York', to: 'Los Angeles', departureTime: '10:00 AM', luggage: '2 Bags', comments: 'No special requirements', status: 'Pending' },
    ];
});

function clickTrip(trip) {
    showTrip.value = true
    displayedTrip.value = trip
}

function addTrip(newTrip) {
  trips.push(newTrip);
  showAddTrip.value = false;
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

function addTripRequest(newTripRequest) {
  tripRequests.push(newTripRequest);
  showAddTripRequest.value = false
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
