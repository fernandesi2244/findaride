<template>
  <div v-show="loading">
    <div class="loading-overlay">
    </div>
    <div class="spinner">
      <div class="spinner-border" style="z-index: 104; width: 6rem; height: 6rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5>Sending requests...</h5>
    </div>
  </div>
  <div v-show="loadingTripCreation">
    <div class="loading-overlay">
    </div>
    <div class="spinner">
      <div class="spinner-border" style="z-index: 104; width: 6rem; height: 6rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5>Creating trip...</h5>
    </div>
  </div>
  <ConfirmDialogue ref="confirmDialogue"> </ConfirmDialogue>
  <JoinTripsModal @joinSelectedTrips="joinSelectedTrips" @refreshTrips="refreshData" :trips="selectedTrips"
    ref="joinTripsRef"></JoinTripsModal>

  <div class="container-xl mb-4" style="row-gap: 20px;">
    <div class="narrow-container">
      <div class="d-flex justify-content-between">
        <h2 class="text-start">Welcome, {{ user.first_name }}!</h2>
      </div>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" data-bs-toggle="tab" data-bs-target="#addTrip" type="button" @click="refreshData">
            Plan a new trip</a>
        </li>
        <li class="nav-item">
          <a id="manage-trips-tab" class="nav-link" data-bs-toggle="tab" data-bs-target="#manageTrip" type="button" @click="refreshData">Manage my trips</a>
        </li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane fade show active pt-4 px-3" id="addTrip" role="tabpanel">
          <AddTripForm @getFilteredTrips="getFilteredTrips" @createTrip="createTrip" @refreshTrips="refreshData"
            ref="addTripModal"></AddTripForm>
          <div class="flex mt-4">
            <button @click="toggleShowJoinTripsModal" :disabled="noTripsSelected" class="btn btn-primary mt-4">
              Request to join
            </button>
            <h3 style="margin: auto; padding-top: 15px;">Trip Matches</h3>
            <div style="visibility: hidden;" class="btn btn-primary mt-4">
              Request to join
            </div>
          </div>

          <v-data-table no-data-text="No matching trips" v-model="selectedTrips" :headers="headers" :items="filteredTrips"
            item-key="id" show-select>
            <template v-slot:item.latest_departure_time="{ item }">
              <div class="text-start">{{ getDateOrRange(item.earliest_departure_time, item.latest_departure_time) }}</div>
            </template>
            <template v-slot:item.earliest_departure_time="{ item }">
              <div class="text-start">{{ getTime(item.earliest_departure_time) }}~{{ getTime(item.latest_departure_time)
              }}</div>
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
          <ManageTripsTab :trips="userTrips" :tripRequests="tripRequests" :userID="user.id" @refreshTrips="refreshData">
          </ManageTripsTab>
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
import JoinTripsModal from './JoinTripsModal.vue';
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
const loadingTripCreation = ref(false);

// display vars
const addTripModal = ref(null)
const confirmDialogue = ref(null);
const joinTripsRef = ref(null);
const selectedTrips = ref([]);
const createTripModalRef = ref(null);

const headers = ref([
  {
    title: 'Departure date',
    align: 'start',
    sortable: true,
    key: 'latest_departure_time',
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

function toggleHelp() {
  if (tripHelpModalRef.value) {
    tripHelpModalRef.value.show();
  }
}

async function refreshData(deletedTripID=null, manageTrips=false) {
  getUserInfo();
  await getUserTrips()

  if (deletedTripID !== null) {
    userTrips.value = userTrips.value.filter(trip => trip.id !== deletedTripID);
  }
  if (manageTrips) {
    goToManageTrips();
  }
}

onMounted(async () => {
  await getUserInfo();
  await getFilteredTrips({});
  await getUserTrips();
});

function goToManageTrips() {
  $("#manage-trips-tab").click();
}

async function getUserInfo() {
  const endpoint = endpoints["me"];
  const response = await axios.get(endpoint);
  Object.assign(user, response.data);
}

async function getUserTrips() {
  const endpoint = `${endpoints["userTrips"]}`;
  const response = await axios.get(endpoint, { params: { when: "upcoming" } });
  tripRequests.value = response.data.trip_requests;
  userTrips.value = response.data.trips;

  userID.value = response.data.id;
}

async function getFilteredTrips(tripDetails) {
  let endpoint = `${endpoints["tripList"]}`;

  let params = {}

  for (const [key, value] of Object.entries(tripDetails)) {
    if (value !== "") {
      if (key === "earliestDepartureTime" || key === "latestDepartureTime") {
        let str = new Date(value).toUTCString();
        params[key] = str;
      } else if (key !== "from" && key !== "to") {
        params[key] = value;
      }
    }
  }
  const response = await axios.get(endpoint, { params: params });
  filteredTrips.value = response.data.trips;
}

async function createTrip(newTrip) {
  //tripRequests.value.push(newTripRequest);
  loadingTripCreation.value = true;

  let departure = {
    "address": newTrip.from,
    "longitude": newTrip.fromLong,
    "latitude": newTrip.fromLat,
  }
  let arrival = {
    "address": newTrip.to,
    "longitude": newTrip.toLong,
    "latitude": newTrip.toLat,
  }

  let earliest_departure_time = new Date(newTrip.earliestDepartureTime).toUTCString();
  let latest_departure_time = new Date(newTrip.latestDepartureTime).toUTCString();

  let data = {
    "earliest_departure_time": earliest_departure_time,
    "latest_departure_time": latest_departure_time,
    "num_luggage_bags": newTrip.luggageCount,
    "user": user.id,
    "departure_location": departure,
    "arrival_location": arrival,
    "trip_nickname": newTrip.nickname,
  }

  const endpoint = endpoints["trip"];
  try {
    const response = await axios.post(endpoint, data);

    await refreshData(); // force to wait before showing confirmation modal

    loadingTripCreation.value = false;

    if (response.data.message === "Trip created") {
      goToManageTrips();
      confirmDialogue.value.show({
        title: "Trip successfully created!",
        message: "Your trip has been created. You can manage your trips in the 'Manage my trips' tab.",
        cancelButton: "Close"
      });
    } else {
      confirmDialogue.value.show({
        title: "Error",
        message: "Error creating trip:\n" + (response.data.error !== undefined ? formatError(response.data.error) : response.data.message),
        cancelButton: "Close",
      });
    }
  } catch (error) {
    loadingTripCreation.value = false;
    // create modal dialog indicating the error that has occurred and to retry
    confirmDialogue.value.show({
      title: "Error",
      message: "Error creating trip:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
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

const noTripsSelected = computed(() => {
  return selectedTrips.value.length === 0;
})

function toggleShowJoinTripsModal() {
  if (noTripsSelected.value) {
    alert("Please select at least one trip.");
    return;
  }
  joinTripsRef.value.show()
}

async function joinSelectedTrips(data) {
  if (noTripsSelected.value) {
    alert("Please select at least one trip.");
    return;
  }
  console.log(data)
  loading.value = true;
  try {
    const response = await axios.post(endpoints["joinSelectedTrips"], { selected_trip_ids: selectedTrips.value, ...data });
    if (response.status === 200) {
      confirmDialogue.value.show({
        title: "Requested to join the selected trip(s)!",
        message: "We have sent requests to join the selected trips on your behalf, and you will receive an email notification when any group accepts.",
        cancelButton: "Close"
      });
      loading.value = false;
      goToManageTrips();
    } else {
      console.error("Request to join trips failed:", response.data);
    }
  } catch (error) {
    console.error("Error requesting to join selected trips:", error);
    alert("Error requesting to join selected trips: " + error.message);
  } finally {
    loading.value = false;
  }
}

</script>
  
<style>
.tab-content {
  background-color: white;
  border: solid;
  border-width: thin;
  /* border-left-width: thin;
    border-right-width: thin;
    border-top-width: 0;
    border-bottom-width: thin; */
  border-top-right-radius: var(--bs-border-radius);
  border-bottom-left-radius: var(--bs-border-radius);
  border-bottom-right-radius: var(--bs-border-radius);
  border-color: var(--bs-border-color);

}

.nav-tabs {
  border-bottom-width: 0;
}

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

button.btn.btn-secondary {
  color: white;
}
</style>