<template>
  <div v-show="loading">
    <div class="loading-overlay">
    </div>
    <div class="spinner">
      <div class="spinner-border" style="z-index: 104; width: 6rem; height: 6rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5>Finding matches...</h5>
    </div>
  </div>
  <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
  <div class="container-xl" style="row-gap: 20px;">
    <div class="narrow-container">
      <div class="d-flex justify-content-between">
        <h2 class="text-start">Welcome, {{ user.first_name }}!</h2>
      </div>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" data-bs-toggle="tab" data-bs-target="#addTrip" type="button">Plan
            a new trip</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" data-bs-target="#manageTrip" type="button">Manage my trips</a>
        </li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane fade show active pt-4 px-3" id="addTrip" role="tabpanel">
          <AddTripForm @getTrips="getFilteredTrips" @addTripRequest="addTripRequest" @refreshTrips="refreshData" ref="addTripModal"></AddTripForm>
          <button v-tooltip="'Would you like to create a trip?'" id="add-trip-btn" @click="addManualTripRequest" class="btn btn-primary">Create a new trip</button>
          <button @click="joinSelectedTrips" class="btn btn-primary">
            Join Selected Trips
          </button>
          <v-data-table
          :items="filteredTrips"
          :headers="headers"
          item-key="id"
          >
            <!-- <template v-slot:item.data-table-select="{ item }">
              <v-checkbox :checked="isSelected(item.id)" @change="toggleSelection(item.id)"></v-checkbox>
            </template> -->
            <template v-slot:item.latest_departure_time="{ item }">
              <div class="text-start">{{ getDateOrRange(item.earliest_departure_time, item.latest_departure_time) }}</div>
            </template>
            <template v-slot:item.is_full="{ item }">
              <div class="text-start">
                 {{ true }}
                 <!-- <v-checkbox :checked="true" @change="toggleSelection(item.id)"></v-checkbox> -->
              </div>
            </template>
            <template v-slot:item.earliest_departure_time="{ item }">
              <div class="text-start">{{ getTime(item.earliest_departure_time) }}~{{ getTime(item.latest_departure_time) }}</div>
            </template>
            <template v-slot:item.departure_location="{ item }">
              <div class="text-start">{{ cleanLocation(item.departure_location) }}</div>
            </template>
            <template v-slot:item.arrival_location="{ item }">
              <div class="text-start">{{ cleanLocation(item.arrival_location) }}</div>
            </template>
            <template v-slot:item.num_luggage_bags="{ item }">
              <div class="text-start">{{ item.num_luggage_bags }}</div>
            </template>
        </v-data-table>
        </div>
        <div class="tab-pane fade" id="manageTrip" role="tabpanel">
            <ManageTripsTab :trips="userTrips" :tripRequests="tripRequests" :userID="user.id"></ManageTripsTab>
        </div>
      </div>

    </div>
  </div>
</template>
  
<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import AddTripForm from '../components/AddTripForm.vue';
import ConfirmDialogue from "../components/ConfirmDialogue.vue";
import ManageTripsTab from './ManageTripsTab.vue';
import TripHelpModal from '../components/TripHelpModal.vue';
import PopupModal from './PopupModal.vue';
import { getDate, getDatePart, getDateOrRange, getTime, cleanLocation, nameEmail, formatError } from '../components/common.js'
import $ from "jquery";

// ground truth data
const user = reactive({ first_name: "", id: -1, })
const filteredTrips = ref([]);
const userTrips = ref([]);
const tripRequests = ref([]);
const userID = ref(0);
const tripHelpModalRef = ref(null);

const loading = ref(false);

// display vars
const showTripForm = ref(true)
const tripComment = ref("");
const addTripModal = ref(null)
const confirmDialogue = ref(null);
const selectedTrips = ref([]);

const headers = ref([
{
    text: 'Select',
    value: 'select',
    sortable: false, 
  },{
    title: 'Departure date',
    align: 'start',
    sortable: true,
    key: 'latest_departure_time',
  },
  {
  title: 'hehe',
  align: 'start',
  sortable: false,
  },
  {
    title: 'Departure time range',
    align: 'start',
    sortable: false,
    key: 'earliest_departure_time',
  },
  {
    title: 'From',
    align: 'start',
    sortable: true,
    key: 'departure_location',
  },
  {
    title: 'To',
    align: 'start',
    sortable: true,
    key: 'arrival_location',
  },
  {
    title: '# luggage bags',
    align: 'start',
    sortable: true,
    key: 'num_luggage_bags',
  },
])

function toggleTripModal() {
  addTripModal.value.show();
}
function isSelected(tripId) {
  return selectedTrips.value.includes(tripId);
}

function toggleSelection(tripId) {
  const index = selectedTrips.value.indexOf(tripId);
  if (index >= 0) {
    selectedTrips.value.splice(index, 1);
  } else {
    selectedTrips.value.push(tripId);
  }
}

function toggleHelp() {
  if (tripHelpModalRef.value) {
    tripHelpModalRef.value.show();
  }
}

async function refreshData() {
  getUserInfo();
  getUserTrips();
}
onMounted(async () => {
  await getUserInfo();
  await getFilteredTrips({});
  await getUserTrips();
});

function goToTripsTab() {
  $("#trips-tab").click();
}

function goToTripRequestsTab() {
  $("#triprequests-tab").click();
}
function goToManageTrips() {
    $("#manageTrip").click();
  }

async function getUserInfo() {
  const endpoint = endpoints["me"];
  const response = await axios.get(endpoint);
  Object.assign(user, response.data);
}

async function getUserTrips() {
  const endpoint = `${endpoints["userTrips"]}${user.id}/`;
  const response = await axios.get(endpoint, { params: { when: "upcoming" } });
  tripRequests.value = response.data.trip_requests;
  userTrips.value = response.data.trips;

  userID.value = response.data.id;
}

async function getFilteredTrips(params) {
  let endpoint = `${endpoints["trip"]}?`;

  for (const [key, value] of Object.entries(params)) {
    if (value !== "") {
      if (key === "earliestDepartureTime" || key === "latestDepartureTime") {
        let str = new Date(value).toUTCString();
        endpoint += `${key}=${str}&`;
      } else {
        endpoint += `${key}=${value}&`;
      }
    }
  }
  console.log(endpoint)
  const response = await axios.get(endpoint);
  filteredTrips.value = response.data;
}

async function addTripRequest(newTripRequest) {
  //tripRequests.value.push(newTripRequest);
  loading.value = true;

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
    const response = await axios.post(endpoint, data);

    await refreshData(); // force to wait before showing confirmation modal

    loading.value = false;

    if (response.data.message === "Trip request created") {
      goToTripRequestsTab();
      confirmDialogue.value.show({
        title: "You have a match!",
        message: "Congrats! We found matching trips. We have sent requests to join on your behalf, and you will receive an email if they accept.",
        cancelButton: "Close"
      });
    }
    else {
      goToTripsTab();
      const confirm = await confirmDialogue.value.show({
        title: "Create Trip Request",
        message: "There were no matching trips. Would you like to create a new trip?",
        okButton: "Yes",
        cancelButton: "No",
      });
      if (!confirm) {
        const endpoint = `${endpoints["trip"]}${newTripRequest.id}/`;
        try {
          axios.patch(endpoint, null, {
            params: {
              action: 'removeUser'
            }
          });
          emit('refreshTrips');
        } catch (error) {
          confirmDialogue.value.show({
            title: "Error",
            message: "Error leaving trip:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
            cancelButton: "Close",
            okClass: "btn btn-danger",
          });
          return;
        }
      }
    }
  } catch (error) {

    loading.value = false;
    // create modal dialog indicating the error that has occurred and to retry
    confirmDialogue.value.show({
      title: "Error",
      message: "Error submitting trip request:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
      cancelButton: "Close",
    });
    return;
  }
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
  async function joinSelectedTrips() {
    if (selectedTrips.value.length === 0) {
      alert("Please select at least one trip.");
      return;
    }  
    loading.value = true;
    try {
        const response = await axios.post(endpoints["tripRequest"], { trips: selectedTrips.value });
        if (response.status === 200) {
          confirmDialogue.value.show({
            title: "You have successfully joined the trip!",
            message: "Congrats! You have successfully requested joined the trip. We have sent requests to join on your behalf, and you will receive an email if they accept.",
            cancelButton: "Close"
          });
          console.log("Trips joined successfully:", response.data);
        } else {
            console.error("Failed to join trips:", response.data);
        }
    } catch (error) {
        console.error("Error joining trips:", error);
        alert("Error joining trips: " + error.message);
    } finally {
        loading.value = false;
    }
    
    goToManageTrips();
  }

  

</script>
  
<style>
.nav-link {
  --bs-nav-link-color: #3B3B3B;
  --bs-nav-pills-link-active-color: #fff;
  --bs-nav-pills-link-active-bg: #3B3B3B;
  --bs-nav-pills-border-radius: 30px;
  --bs-nav-link-hover-color: none;
  border: 2px solid #1A1A1A;
  display: inline-block;
  padding: 10px;
  text-align: center;
  transition: all 300ms cubic-bezier(.23, 1, 0.32, 1);
}

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

.fill {
  width: 100%;
  height: 100%;
}

.narrow-container {
  max-width: 1000px;
  /* padding: 20px; */
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
}

.loading-overlay {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background-color: #000000;
  opacity: 0.4;
  z-index: 2;
}

.spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 1;
  margin: 0 auto;
  z-index: 101;
  color: rgb(255, 255, 255);
}
</style>