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
        <h2 class="text-start">Welcome, {{ user.first_name == "" ? 'fellow ridesharer' : user.first_name }}!</h2>
      </div>
      <ul class="nav nav-tabs no-border-bottom">
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

          <v-data-table no-data-text="No trips matching the provided filters" v-model="selectedTrips" :headers="headers" :items="filteredTrips"
            item-key="id" show-select>
            <template v-slot:item.latest_departure_time="{ item }">
              <div class="text-start">{{ getDateOrRange(item.earliest_departure_time, item.latest_departure_time) }}</div>
            </template>
            <template v-slot:item.earliest_departure_time="{ item }">
              <div class="text-start">{{ getTime(item.earliest_departure_time) }} - {{ getTime(item.latest_departure_time)
              }}</div>
            </template>
            <template v-slot:item.departure_location="{ item }">
              <div :title="item.departure_location" class="text-start">{{ cleanLocation(item.departure_location) }}</div>
            </template>
            <template v-slot:item.arrival_location="{ item }">
              <div :title="item.arrival_location" class="text-start">{{ cleanLocation(item.arrival_location) }}</div>
            </template>
            <template v-slot:item.num_luggage_bags="{ item }">
              <div class="text-start">{{ item.num_luggage_bags }}</div>
            </template>
            <template v-slot:item.num_pending_requests="{ item }">
              <div class="text-start">{{ item.num_pending_requests }}</div>
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
import { getDate, getDatePart, getDateOrRange, getTime, cleanLocation, formatError } from '../components/common.js'
import $ from "jquery";

// ground truth data
const user = reactive({ first_name: " ", id: -1, })
const filteredTrips = ref([]);
const userTrips = ref([]);
const tripRequests = ref([]);

const loading = ref(false);
const loadingTripCreation = ref(false);

// display vars
const addTripModal = ref(null)
const confirmDialogue = ref(null);
const joinTripsRef = ref(null);
const selectedTrips = ref([]);

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
    title: '# Luggage bags',
    align: 'start',
    sortable: true,
    key: 'num_luggage_bags',
  },
  {
    title: '# Pending requests to join',
    align: 'start',
    sortable: true,
    key: 'num_pending_requests',
  },
])

async function refreshData(deletedTripID=null, manageTrips=false) {
    await getUserTrips();

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
        cancelButton: "Close",
        message: "Your trip has been created. You can manage your trips in the 'Manage my trips' tab.",
      });
    } else {
      confirmDialogue.value.show({
        title: "Error",
        message: "Error creating trip:\n" + (response.data.error !== undefined ? formatError(response.data.error) : response.data.message),
      });
    }
  } catch (error) {
    loadingTripCreation.value = false;
    // create modal dialog indicating the error that has occurred and to retry
    confirmDialogue.value.show({
      title: "Error",
      message: "Error creating trip:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
    });
    return;
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
  loading.value = true;
  try {
    const response = await axios.post(endpoints["joinSelectedTrips"], { selected_trip_ids: selectedTrips.value, ...data });
    if (response.status === 200) {
      confirmDialogue.value.show({
        title: "Requested to join the selected trip(s)!",
        cancelButton: "Close",
        message: "You will receive an email notification when any group accepts.",
      });
      loading.value = false;
      for (var trip of selectedTrips.value) {
            const index = filteredTrips.value.findIndex(obj => obj.id == trip);
            if(index > -1) {
                filteredTrips.value.splice(index, 1);
            }
      }
      selectedTrips.value = [];
      goToManageTrips();
      refreshData();
    } else {
      console.error("Request to join trips failed:", response.data);
    }
  } catch (error) {
    if (error?.response?.data?.error) {
      alert(formatError(error.response.data.error));
      console.error("Error requesting to join selected trips:", error.response.data.error);
    } else {
      alert("Error requesting to join selected trips: " + error.message);
      console.error("Error requesting to join selected trips:", error.message);
    }
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
  border-top-right-radius: var(--bs-border-radius);
  border-bottom-left-radius: var(--bs-border-radius);
  border-bottom-right-radius: var(--bs-border-radius);
  border-color: var(--bs-border-color);

}

.no-border-bottom {
    border-bottom: none !important;;
}
/* .nav-tabs {
  border-bottom: none;
} */

.nav-link {
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
  background-color: #F4F4F8;
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
  padding: 20px; 
  margin: 0 auto;
  background-color: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
}

.btn-secondary {
  color: white;
}

.spinner-border {
  width: 6rem;
  height: 6rem;
  color: #007bff;
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

@media (max-width: 768px) {
  .narrow-container {
    padding: 15px;
  }

  .nav-link {
    padding: 8px 12px;
  }
}
</style>