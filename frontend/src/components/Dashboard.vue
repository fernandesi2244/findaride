<template>
  <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
  <div class="container-xl pt-4">
    <div class="narrow-container">
      <div class="d-flex justify-content-between">
        <h2 class="text-start">Welcome, {{ user.first_name }}!</h2>
        <button @click="toggleTripModal" class="btn btn-primary">Plan a new trip</button>
        <AddTripModal @addTripRequest="addTripRequest" ref="addTripModal"></AddTripModal>
      </div>

      <ul class="mt-2 nav nav-pills" role="tablist">
        <!--
        <li class="nav-item" role="presentation">
            <button
                class="nav-link active"
                id="addtrip-tab"
                data-bs-toggle="tab"
                data-bs-target="#addtrip"
                type="button"
                role="tab"
                aria-selected="true"
            >
                Plan a new trip
            </button>
        </li>-->
        <li class="nav-item" role="presentation">
            <button
                class="nav-link active"
                id="trips-tab"
                data-bs-toggle="tab"
                data-bs-target="#trips"
                type="button"
                role="tab"
                aria-selected="false"
            >
                My confirmed trips
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button
                class="nav-link"
                id="triprequests-tab"
                data-bs-toggle="tab"
                data-bs-target="#triprequests"
                type="button"
                role="tab"
                aria-selected="false"
            >
                My pending trips
            </button>
        </li>
    </ul>
      <div class="col-10 tab-content mx-auto pt-4" id="v-pills-tabContent">
        <div class="tab-pane fade show active" id="trips" role="tabpanel" aria-labelledby="v-pills-trips-tab">
          <TripsTab :trips="activeTrips" :userID="userID" @refreshTrips="refreshData" />
        </div>
        <div class="tab-pane fade" id="triprequests" role="tabpanel" aria-labelledby="v-pills-triprequests-tab">
          <TripRequestsTab :tripRequests="tripRequests" @refreshTrips="refreshData" @goToTripsTab="goToTripsTab" @goToTripRequestsTab="goToTripRequestsTab" />
        </div>
        <!--
        <div class="tab-pane fade show active" id="addtrip" role="tabpanel" aria-labelledby="v-pills-addtrip-tab">
          <AddTripForm @addTripRequest="addTripRequest" />
          <div id="add-trip-request-confirmation-modal" class="modal">
            <div class="modal-content">
              <p id="add-trip-request-submit-message"></p>
              <button id="add-trip-request-close-button" class="btn cancel-btn"></button>
            </div>
          </div>
        </div>-->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed} from 'vue';
import TripsTab from '../components/TripsTab.vue';
import TripRequestsTab from '../components/TripRequestsTab.vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import AddTripModal from '../components/AddTripModal.vue';
import ConfirmDialogue from "../components/ConfirmDialogue.vue";
import $ from "jquery";

// ground truth data
const user = reactive({ first_name: "", id: -1, })
const trips = ref([]);
const tripRequests = ref([]);
const userID = ref(0);

const activeTrips = computed(() => {
  return trips.value.filter((item) => {
    return item.is_active;
  });
})

const activeTripRequests = computed(() => {
  return tripRequests.value.filter((item) => {
    return item.is_active;
  });
})

// display vars
const centerDisplay = ref({ type: "default", id: 0 });
const showTripForm = ref(false)

const addTripModal = ref(null)
const confirmDialogue = ref(null);

function toggleTripModal() {
  addTripModal.value.show();
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
    $("#trips-tab").click();
  } else if (tripRequests.value.length > 0) {
    $("#v-pills-triprequests-tab").click();
  } else {
    $("#v-pills-addtrip-tab").click();
  }
});

function goToTripsTab() {
  $("#trips-tab").click();
}

function goToTripRequestsTab() {
  $("#triprequests-tab").click();
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
      confirmDialogue.value.show({
        title: "Error",
        message: "Error submitting trip request:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
        cancelButton: "Close",
      });
    return;
  }

  showTripForm.value = false;

  await getUserTrips(); // force to wait before showing confirmation modal

  const confirm = await confirmDialogue.value.show({
    title: "Created",
    message: "Trip request successfully created!",
    cancelButton: "Close"
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
      errorString += `${errorNum++} ${value}\n`;
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
  height: 100%;
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

.narrow-container {
  max-width: 800px;
  margin: 0 auto;
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