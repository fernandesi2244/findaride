<template>
  <div class="trip-request-form">

    <h3 class>Create a new trip request</h3>
    <!-- to do: add tooltip -->
    <!-- <h2 class="tooltip">Top Tooltip
      <h3 class="tooltiptext">Top Tooltip</h3>
    </h2> -->
    
    <form @submit.prevent="submit" class="form-container">
      <div class="form-group">
        <label for="from">Pickup Location:</label>
        <input id="from" ref="fromRef" v-model="trip.from" placeholder="Start typing to see results..." required />
      </div>
      <div class="form-group">
        <label for="to">Dropoff Location:</label>
        <input id="to" ref="toRef" v-model="trip.to" placeholder="Start typing to see results..." required />
      </div>
      <div class="form-group">
        <label for="pickup-time">Earliest departure time:</label>
        <input id="pickup-time" v-model="trip.earliestDepartureTime" type="datetime-local" required />
      </div>
      <div class="form-group">
        <label for="dropoff-time">Latest departure time:</label>
        <input id="dropoff-time" v-model="trip.latestDepartureTime" type="datetime-local" required />
      </div>
      <div class="form-group">
        <label for="pickup-walking-distance">Maximum walking distance to pickup (in minutes):</label>
        <input id="pickup-walking-distance" v-model.number="trip.pickupWalkingDistance" type="number" min="0" required />
      </div>
      <div class="form-group">
        <label for="dropoff-walking-distance">Maximum walking distance from dropoff (in minutes):</label>
        <input id="dropoff-walking-distance" v-model.number="trip.dropoffWalkingDistance" type="number" min="0" required />
      </div>
      <div class="form-group">
        <label for="luggage-count">Number of luggage bags:</label>
        <input id="luggage-count" v-model.number="trip.luggageCount" type="number" min="0" required />
      </div>
      <div class="form-group">
        <label for="comments">Additional comments:</label>
        <textarea id="comments" v-model="trip.comment" placeholder="Any special accommodations, considerations, etc." maxlength="255"></textarea>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn primary">Create trip request</button>
        <button @click="closeModal" class="btn cancel-btn">Reset</button>
      </div>
    </form>
  </div>
</template> 
 
 
<script setup>
import { ref, reactive, defineEmits, onMounted } from 'vue';
const emit = defineEmits(['addTripRequest', 'close']);


const fromRef = ref();
const toRef = ref();


const trip = reactive({
  from: '',
  fromLat: 0,
  fromLong: 0,
  to: '',
  toLat: 0,
  toLong: 0,
  departureDate: '',
  earliestDepartureTime: '',
  latestDepartureTime: '',
  luggageCount: 0,
  comment: '',
  status: 'Pending',
});


function submit() {
  console.log("Submitting trip:", trip);
  emit('addTripRequest', { ...trip });
  resetForm();
}


function closeModal() {
  emit('close');
  resetForm();
  //router.push('/dashboard');
}


function resetForm() {
  trip.from = '';
  trip.fromLat = 0;
  trip.fromLong = 0;
  trip.to = '';
  trip.toLat = 0;
  trip.toLong = 0;
  trip.departureDate = '';
  trip.earliestDepartureTime = '';
  trip.latestDepartureTime = '';
  trip.luggageCount = 0;
  trip.comment = '';
}


onMounted(() => {
  const acFrom = new google.maps.places.Autocomplete(fromRef.value, {
    types: ["transit_station"],
    fields: ["geometry"]
  });


  const acTo = new google.maps.places.Autocomplete(toRef.value, {
    types: ["transit_station"],
    fields: ["geometry"]
  });


  google.maps.event.addListener(acFrom, "place_changed", () => {
    let place = acFrom.getPlace().geometry.location;
    trip.fromLat = place.lat();
    trip.fromLong = place.lng();
    trip.from = document.getElementById('from').value;
  });


  google.maps.event.addListener(acTo, "place_changed", () => {
    let place = acTo.getPlace().geometry.location;
    trip.toLat = place.lat();
    trip.toLong = place.lng();
    trip.to = document.getElementById('to').value;
  });
});
</script>
<style>
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --input-border-color: #ccc;
  --hover-opacity: 0.9;
}


.trip-request-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* left-align all elements */
  text-align: left;
}


.trip-request-form h3 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}


/* Style for form groups */
.form-group {
  margin-bottom: 15px;
}


.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}


.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}


.form-group textarea {
  height: 100px;
  resize: vertical;
}


/* Style for buttons */
.form-actions {
  text-align: right;
  padding-top: 10px;
}


.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}


.btn.primary {
  background-color: #007bff;
  color: white;
}


.btn.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
}


.btn:hover {
  opacity: 0.9;
}


/* Additional styles for responsiveness and interactivity */
@media (max-width: 768px) {
  .trip-request-form {
    padding: 10px;
  }
}


input:focus,
textarea:focus {
  border-color: #007bff;
  outline: none;
}

.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 50%;
  margin-left: -60px;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
 
 
 