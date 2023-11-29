<template>
  <div class="container-xl pt-4">
    <div class="row">
      <div class="col-2">
        <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical"
          style="position: sticky; top: 90px">
          <button class="nav-link text-start" id="v-pills-addtrip-tab" data-bs-toggle="pill"
            data-bs-target="#v-pills-addtrip" type="button" role="tab" aria-controls="v-pills-addtrip"
            aria-selected="false">
            New Trip Request
          </button>
          <button class="nav-link text-start" id="v-pills-trips-tab" data-bs-toggle="pill" data-bs-target="#v-pills-trips"
            type="button" role="tab" aria-controls="v-pills-trips" aria-selected="false" @click="refreshData">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" class="mb-1" fill="currentColor"
              viewBox="0 0 16 16">
              <path
                d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z" />
            </svg>
            Trips
          </button>
          <button class="nav-link text-start" id="v-pills-triprequests-tab" data-bs-toggle="pill"
            data-bs-target="#v-pills-triprequests" type="button" role="tab" aria-controls="v-pills-triprequests"
            aria-selected="false" @click="refreshData">
            <svg class="mb-1" xmlns="http://www.w3.org/2000/svg" height="18" width="18" fill="currentColor"
              viewBox="0 0 20 20">
              <path
                d="M16.254,3.399h-0.695V3.052c0-0.576-0.467-1.042-1.041-1.042c-0.576,0-1.043,0.467-1.043,1.042v0.347H6.526V3.052c0-0.576-0.467-1.042-1.042-1.042S4.441,2.476,4.441,3.052v0.347H3.747c-0.768,0-1.39,0.622-1.39,1.39v11.813c0,0.768,0.622,1.39,1.39,1.39h12.507c0.768,0,1.391-0.622,1.391-1.39V4.789C17.645,4.021,17.021,3.399,16.254,3.399z M14.17,3.052c0-0.192,0.154-0.348,0.348-0.348c0.191,0,0.348,0.156,0.348,0.348v0.347H14.17V3.052z M5.136,3.052c0-0.192,0.156-0.348,0.348-0.348S5.831,2.86,5.831,3.052v0.347H5.136V3.052z M16.949,16.602c0,0.384-0.311,0.694-0.695,0.694H3.747c-0.384,0-0.695-0.311-0.695-0.694V7.568h13.897V16.602z M16.949,6.874H3.052V4.789c0-0.383,0.311-0.695,0.695-0.695h12.507c0.385,0,0.695,0.312,0.695,0.695V6.874z M5.484,11.737c0.576,0,1.042-0.467,1.042-1.042c0-0.576-0.467-1.043-1.042-1.043s-1.042,0.467-1.042,1.043C4.441,11.271,4.908,11.737,5.484,11.737z M5.484,10.348c0.192,0,0.347,0.155,0.347,0.348c0,0.191-0.155,0.348-0.347,0.348s-0.348-0.156-0.348-0.348C5.136,10.503,5.292,10.348,5.484,10.348z M14.518,11.737c0.574,0,1.041-0.467,1.041-1.042c0-0.576-0.467-1.043-1.041-1.043c-0.576,0-1.043,0.467-1.043,1.043C13.475,11.271,13.941,11.737,14.518,11.737z M14.518,10.348c0.191,0,0.348,0.155,0.348,0.348c0,0.191-0.156,0.348-0.348,0.348c-0.193,0-0.348-0.156-0.348-0.348C14.17,10.503,14.324,10.348,14.518,10.348z M14.518,15.212c0.574,0,1.041-0.467,1.041-1.043c0-0.575-0.467-1.042-1.041-1.042c-0.576,0-1.043,0.467-1.043,1.042C13.475,14.745,13.941,15.212,14.518,15.212z M14.518,13.822c0.191,0,0.348,0.155,0.348,0.347c0,0.192-0.156,0.348-0.348,0.348c-0.193,0-0.348-0.155-0.348-0.348C14.17,13.978,14.324,13.822,14.518,13.822z M10,15.212c0.575,0,1.042-0.467,1.042-1.043c0-0.575-0.467-1.042-1.042-1.042c-0.576,0-1.042,0.467-1.042,1.042C8.958,14.745,9.425,15.212,10,15.212z M10,13.822c0.192,0,0.348,0.155,0.348,0.347c0,0.192-0.156,0.348-0.348,0.348s-0.348-0.155-0.348-0.348C9.653,13.978,9.809,13.822,10,13.822z M5.484,15.212c0.576,0,1.042-0.467,1.042-1.043c0-0.575-0.467-1.042-1.042-1.042s-1.042,0.467-1.042,1.042C4.441,14.745,4.908,15.212,5.484,15.212z M5.484,13.822c0.192,0,0.347,0.155,0.347,0.347c0,0.192-0.155,0.348-0.347,0.348s-0.348-0.155-0.348-0.348C5.136,13.978,5.292,13.822,5.484,13.822z M10,11.737c0.575,0,1.042-0.467,1.042-1.042c0-0.576-0.467-1.043-1.042-1.043c-0.576,0-1.042,0.467-1.042,1.043C8.958,11.271,9.425,11.737,10,11.737z M10,10.348c0.192,0,0.348,0.155,0.348,0.348c0,0.191-0.156,0.348-0.348,0.348s-0.348-0.156-0.348-0.348C9.653,10.503,9.809,10.348,10,10.348z">
              </path>
            </svg>
            Trip Requests
          </button>
        </div>
      </div>
      <div class="col-10 tab-content px-4" id="v-pills-tabContent">
        <div class="tab-pane fade" id="v-pills-trips" role="tabpanel" aria-labelledby="v-pills-trips-tab">
          <TripsTab :trips="trips" :userID="userID" @refreshTrips="refreshData" />
        </div>
        <div class="tab-pane fade" id="v-pills-triprequests" role="tabpanel" aria-labelledby="v-pills-triprequests-tab">
          <TripRequestsTab :tripRequests="tripRequests" @refreshTrips="refreshData" @goToTripsTab="goToTripsTab" @goToTripRequestsTab="goToTripRequestsTab" />
        </div>
        <div class="tab-pane fade" id="v-pills-addtrip" role="tabpanel" aria-labelledby="v-pills-addtrip-tab">
          <AddTripForm @addTripRequest="addTripRequest" />
          <div id="add-trip-request-confirmation-modal" class="modal">
            <div class="modal-content">
              <p id="add-trip-request-submit-message"></p>
              <button id="add-trip-request-close-button" class="btn cancel-btn"></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import TripsTab from '../components/TripsTab.vue';
import TripRequestsTab from '../components/TripRequestsTab.vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import AddTripForm from '../components/AddTripForm.vue';
import $ from "jquery";

// ground truth data
const user = reactive({ first_name: "", id: -1, })
//const trips = ref([{id: 0, data: data, participants: participants, joinRequests: joinRequests, confirmationRequests: confirmationRequests}]);
const trips = ref([]);
const tripRequests = ref([]);
const userID = ref(0);

//const tripRequests = ref([{id: 0, data: data, participants: participants, joinRequests: joinRequests, confirmationRequests: confirmationRequests}]);

// display vars
const centerDisplay = ref({ type: "default", id: 0 });
const showTripForm = ref(false)
function toggleTripForm() {
  showTripForm.value = !showTripForm.value;
}

async function refreshData() {
  getUserInfo();
  getUserTrips();
}

onMounted(async () => {
  await getUserInfo();
  await getUserTrips();

  // if the user already has a trip, show the trip tab
  if (trips.value.length > 0) {
    $("#v-pills-trips-tab").click();
  } else if (tripRequests.value.length > 0) {
    $("#v-pills-triprequests-tab").click();
  } else {
    $("#v-pills-addtrip-tab").click();
  }
});

function goToTripsTab() {
  $("#v-pills-trips-tab").click();
}

function goToTripRequestsTab() {
  $("#v-pills-triprequests-tab").click();
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
  tripRequests.value = response.data.trip_requests;

  userID.value = response.data.id;
}

async function addTripRequest(newTripRequest) {
  //tripRequests.value.push(newTripRequest);

  let departure = {
    "address": newTripRequest.from,
    "longitude": newTripRequest.fromLong,
    "latitude": newTripRequest.fromLat,
  }
  let arrival = {
    "address": newTripRequest.to,
    "longitude": newTripRequest.toLong,
    "latitude": newTripRequest.toLat,
  }

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
    // create modal dialog indicating the error that has occurred and to retry
    $("#add-trip-request-submit-message").text("Error submitting trip request:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText));
    $("#add-trip-request-close-button").text("Retry");
    $("#add-trip-request-confirmation-modal").css("display", "block");
    $("#add-trip-request-close-button").click(function () {
      $("#add-trip-request-confirmation-modal").css("display", "none");
    });
    return;
  }

  showTripForm.value = false;

  await getUserTrips(); // force to wait before showing confirmation modal

  // create modal dialog indicating that the trip request has been added
  $("#add-trip-request-submit-message").text("Trip request successfully created!");
  if (trips.value.length > 0) {
    $("#add-trip-request-close-button").text("View trips");
  } else {
    $("#add-trip-request-close-button").text("View trip requests");
  }
  $("#add-trip-request-confirmation-modal").css("display", "block");
  $("#add-trip-request-close-button").click(function () {
    if (trips.value.length > 0) {
      $("#v-pills-trips-tab").click();
    } else {
      $("#v-pills-triprequests-tab").click();
    }
    $("#add-trip-request-confirmation-modal").css("display", "none");
  });
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

function selectTrip(id) {
  centerDisplay.value.type = 'trip';
  centerDisplay.value.id = id
}

function selectTripRequest(id) {
  centerDisplay.value.type = 'request';
  centerDisplay.value.id = id
}

function getTrip(id) {
  const index = trips.value.findIndex(trip => trip.id === id);
  if (index != -1) {
    return trips.value[index]
  }
}

function getTripRequest(id) {
  const index = tripRequests.value.findIndex(tripReq => tripReq.id === id);
  if (index != -1) {
    return tripRequests.value[index]
  }
}

function formatError(errorDict) {
  if (typeof errorDict === "string") {
    return errorDict;
  }
  try {
    let errorString = "";
    let errorNum = 1;
    for (const [key, value] of Object.entries(errorDict)) {
      errorString += `${errorNum++}) ${value}\n`;
    }
    return errorString;
  } catch (error) {
    return JSON.stringify(errorDict);
  }
}

</script>

<style>
.col-2 {
  margin-top: 1.1rem;
}

.dashboard {
  /* max-width: 1000px; */
  height: 100%;
  /* margin: 40px auto; */
  /* padding: 20px; */
  font-family: 'Roboto', sans-serif;
}

.card {
  background-color: #DCDCDC;
  border-color: #DCDCDC;
}

.padding {
  padding: 10px;
  width: 100%;
  height: 100%;
  /* box-sizing: border-box; */
  display: flex;
  border-radius: 20px;
}

/* The Modal (background) */
.modal {
  display: none;
  /* Hidden by default */
  position: fixed;
  /* Stay in place */
  z-index: 1;
  /* Sit on top */
  left: 0;
  top: 0;
  width: 100%;
  /* Full width */
  height: 100%;
  /* Full height */
  overflow: auto;
  /* Enable scroll if needed */
  background-color: rgb(0, 0, 0);
  /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4);
  /* Black w/ opacity */
  white-space: pre;
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 20% auto;
  /* 20% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
}

/* The Close Button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}</style>