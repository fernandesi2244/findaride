<template>
  <div class="dashboard">
    <h1>Welcome back, Placeholder!</h1>
    
    <div class="trips-section">
      <div class="section-header">
        <h2>Your Trips</h2>
        <button @click="showAddTrip = true" class="btn add-trip-btn">+ Add New Trip</button>
      </div>
      
      <div v-if="trips.length">
        <ul class="list-reset">
          <li v-for="trip in trips" :key="trip.id" class="card">
            <div class="trip-info">
              <div><strong>Date:</strong> {{ trip.date }}</div>
              <div><strong>From:</strong> {{ trip.from }}</div>
              <div><strong>To:</strong> {{ trip.to }}</div>
              <div><strong>Departure Time:</strong> {{ trip.departureTime }}</div>
              <div><strong>Luggage Count:</strong> {{ trip.luggageCount }}</div>
              <div><strong>Comments:</strong> {{ trip.comments }}</div>
            </div>
            <span :class="['status', trip.status === 'Active' ? 'status-active' : 'status-inactive']">{{ trip.status }}</span>
            <button @click="joinTrip(trip.id)" class="btn btn-primary">Join</button>
            <button @click="removeTrip(trip.id)" class="btn btn-danger">Remove</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p class="no-trips-message">You haven't planned any trips yet.</p>
      </div>
    </div>
    
    <AddTripForm v-if="showAddTrip" @addTrip="addTrip" @close="showAddTrip = false" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import AddTripForm from '../components/AddTripForm.vue';

const trips = reactive([]);
const showAddTrip = ref(false);

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
</style>
