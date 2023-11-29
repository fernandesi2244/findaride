<template>
  <div class="trip-request-form">

    <div class="header-container">
      <h3>Create a new trip request</h3>
      <button @click="() => TogglePopup('buttonTrigger')" class="need-help-btn">Need Help</button>
    </div>
		<Popup 
			v-if="popupTriggers.buttonTrigger" 
			:TogglePopup="() => TogglePopup('buttonTrigger')">
      <h2>Tutorial</h2>
      <p class="popup-text">
        Creating a Trip Request<br>
        - To start, click 'Create a new trip request'. This opens the form to input your trip details.<br>
        Filling Out the Form<br>
        - Pickup Location: Enter your start location in the 'Pickup Location' field, using suggestions<br> 
        that appear as you type.<br>
        - Dropoff Location: Similarly, input your end location in the 'Dropoff Location' field.<br>
        - Departure Times: Choose your 'Earliest Departure Time' and 'Latest Departure Time' using <br>
        the datetime pickers.<br>
        - Walking Distance: Specify your maximum walking distance to and from pickup and dropoff <br>
        points in minutes.<br>
        - Luggage: Indicate the number of luggage bags.<br>
        - Additional Comments: Use the 'Additional comments' section for special requests or <br>
        considerations.<br>
        This could include preferences like a child seat, assistance for <br>
        differently-abled passengers, etc. There's a character limit to ensure concise <br>
        communication.<br>
        Submitting the Form<br>
        - Click 'Create trip request' to submit. Use the 'Reset' button to clear all fields if needed.<br>
        - After Submission - You'll receive an email notification about the status of your trip request <br>
        after submission.<br>
        - Accessing Trip Requests: Navigate to the 'Trip Requests' tab to view your submitted requests.<br>
        - Trip Request Details: Each request is listed with details like departure and arrival locations, <br>
        and departure times.<br>
        Status and Actions:<br>
        - Each request shows its current status (e.g., pending, confirmed).<br>
        - You can withdraw a request or accept/reject join requests for your trip.<br>
        - After Submission - You'll receive an email notification about the status of your trip request 
        <br>after submission.
      </p>
      </Popup>
		
    <form @submit.prevent="submit" class="form-container">
      <div class="form-group">
        <label for="from">Pickup location:</label>
        <input id="from" ref="fromRef" v-model="trip.from" placeholder="Start typing to see results..." required />
      </div>
      <div class="form-group">
        <label for="to">Dropoff location:</label>
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
import Popup from '../components/Popup.vue';
const popupTriggers = ref({
  buttonTrigger: false,
  timedTrigger: false
});
const TogglePopup = (trigger) => {
  popupTriggers.value[trigger] = !popupTriggers.value[trigger]
}


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

.need-help-btn {
  background-color: var(--primary-color);
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.need-help-btn:hover {
  background-color: darken(var(--primary-color), 10%);
}
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

</style>