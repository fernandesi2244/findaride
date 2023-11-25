<template>
  <div class="trip-request-form">
    <h3>Add a New Trip Request</h3>
    <form @submit.prevent="submit" class="form-container">
      <!-- Pickup Location -->
      <div class="form-group">
        <label for="from">Pickup Location:</label>
        <input id="from" ref="fromRef" v-model="trip.from" placeholder="From" required />
      </div>
      <!-- Dropoff Location -->
      <div class="form-group">
        <label for="to">Dropoff Location:</label>
        <input id="to" ref="toRef" v-model="trip.to" placeholder="To" required />
      </div>
      <!-- Time Fields -->
      <div class="form-group">
        <label for="pickup-time">Earliest Departure Time:</label>
        <input id="pickup-time" v-model="trip.earliestDepartureTime" type="datetime-local" required />
      </div>
      <div class="form-group">
        <label for="dropoff-time">Lastest Departure Time:</label>
        <input id="dropoff-time" v-model="trip.latestDepartureTime" type="datetime-local" required />
      </div>
      <!-- Luggage Count -->
      <div class="form-group">
        <label for="luggage-count">Luggage Count:</label>
        <input id="luggage-count" v-model.number="trip.luggageCount" type="number" min="0" required />
      </div>
      <!-- Additional Comments -->
      <div class="form-group">
        <label for="comments">Additional Comments:</label>
        <textarea id="comments" v-model="trip.comment" placeholder="Other comments" maxlength="255"></textarea>
      </div>
      <!-- Buttons -->
      <div class="form-actions">
        <button type="submit" class="btn primary">Add Trip Request</button>
        <button @click="closeModal" class="btn cancel-btn">Cancel</button>
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
 fromPostalCode: '',
 /*
 fromLat: 0,
 fromLong: 0, */
 to: '',
 toPostalCode: '',
 /*
 toLat: 0,
 toLong: 0,*/
 departureDate:'',
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
 trip.fromPostalCode = '';
 /*
 trip.fromLat = 0;
 trip.fromLong = 0;*/
 trip.to = '';
 trip.toPostalCode = '';
 /*
 trip.toLat = 0;
 trip.toLong = 0;*/
 trip.departureDate='';
 trip.earliestDepartureTime = '';
 trip.latestDepartureTime = '';
 trip.luggageCount = 0;
 trip.comment = '';
 }
 
 
 onMounted(()=>{
 const acFrom = new google.maps.places.Autocomplete(fromRef.value, {
  types: ["transit_station"],
  fields: ["address_components"]
 });
 
 
 const acTo = new google.maps.places.Autocomplete(toRef.value, {
  types: ["transit_station"],
  fields: ["address_components"]
 });
 
 
 google.maps.event.addListener(acFrom, "place_changed", () => {
  console.log(acFrom.getPlace().address_components)
  let postalCode = acFrom.getPlace().address_components.pop();
  /*
  trip.fromLat = place.lat();
  trip.fromLong = place.lng();*/
  trip.fromPostalCode = postalCode.long_name;
  trip.from = document.getElementById('from').value;
 });
 
 
 google.maps.event.addListener(acTo, "place_changed", () => {
  let postalCode = acTo.getPlace().address_components.pop();
  /*
  trip.toLat = place.lat();
  trip.toLong = place.lng();*/
  trip.toPostalCode = postalCode.long_name;
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
 
 
 .form-group input[type="text"],
 .form-group input[type="datetime-local"],
 .form-group input[type="number"],
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
 
 
 input:focus, textarea:focus {
 border-color: #007bff;
 outline: none;
 }
 
 
 </style>
 
 
 