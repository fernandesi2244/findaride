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
          <AddTripModal @addTripRequest="addTripRequest" @refreshTrips="refreshData" ref="addTripModal"></AddTripModal>
        <ul class="mt-2 nav nav-pills" role="tablist">
            <li class="nav-item" role="presentation">
            <button class="nav-link btn-sm" id="triprequests-tab" data-bs-toggle="tab" data-bs-target="#triprequests" type="button"
              role="tab" aria-selected="false" @click="refreshData">
              Matched Trips
            </button>
          </li>
          <li class="nav-item" role="presentation" style="margin-right: 10px;">
            <button class="nav-link active btn-sm" id="trips-tab" data-bs-toggle="tab" data-bs-target="#trips" type="button"
              role="tab" aria-selected="false" @click="refreshData">
              Created Trips
            </button>
          </li>
          <button @click="toggleHelp" class="btn btn-primary need-help-btn" style="background-color: #95a1ac; font-size:small; width: 42px; height: 42px; margin-left: 1em">?</button>
          <TripHelpModal ref="tripHelpModalRef"></TripHelpModal>
      </ul>
        <div class="col-10 tab-content fill pt-4" id="v-pills-tabContent">
          <div class="tab-pane fade show active" id="trips" role="tabpanel" aria-labelledby="v-pills-trips-tab">
            <TripsTab :trips="activeTrips" :userID="userID" @refreshTrips="refreshData" />
          </div>
          <div class="tab-pane fade" id="triprequests" role="tabpanel" aria-labelledby="v-pills-triprequests-tab">
            <TripRequestsTab :tripRequests="activeTripRequests" @refreshTrips="refreshData" @goToTripsTab="goToTripsTab"
              @goToTripRequestsTab="goToTripRequestsTab" />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed } from 'vue';
  import TripsTab from '../components/TripsTab.vue';
  import TripRequestsTab from '../components/TripRequestsTab.vue';
  import { endpoints } from '../common/endpoints.js';
  import { axios } from '../common/axios_service.js'
  import AddTripModal from '../components/AddTripForm.vue';
  import ConfirmDialogue from "../components/ConfirmDialogue.vue";
  import TripHelpModal from '../components/TripHelpModal.vue';
  import PopupModal from './PopupModal.vue';
  import { formatError } from './common.js';
  import $ from "jquery";
  
  // ground truth data
  const user = reactive({ first_name: "", id: -1, })
  const trips = ref([]);
  const tripRequests = ref([]);
  const userID = ref(0);
  const tripHelpModalRef = ref(null);
  
  const loading = ref(false);
  
  
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
  const showTripForm = ref(true)
  
  const addTripModal = ref(null)
  const confirmDialogue = ref(null);
  
  function toggleTripModal() {
    addTripModal.value.show();
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
    await getUserTrips();
    toggleTripModal();
    // if the user already has a trip, show the trip tab
    if (trips.value.length > 0) {
      $("#trips-tab").click();
    } else if (tripRequests.value.length > 0) {
      $("#triprequests-tab").click();
    } else {
      $("#triprequests-tab").click();
      $("#add-trip-btn").click();
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
  
    userID.value = response.data.id;
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
  
      if (response.data.message==="Trip request created") {
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