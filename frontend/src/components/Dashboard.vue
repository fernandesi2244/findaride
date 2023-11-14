<template>
    <div class="dashboard">
        <Sidebar @selectTrip="selectTrip" @selectTripRequest="selectTripRequest" @showTripForm="showTripForm = true" :trips="trips" :tripRequests="tripRequests"/>

        <div class="padding">
            <div class="card padding">
                <div v-if="centerDisplay.type === 'trip'"><TripPage :trip="getTrip(centerDisplay.id)"/></div>
                <div v-else-if="centerDisplay.type === 'request'"><TripRequestPage :reqid="centerDisplay.id"/></div>
                <div v-else><FrontPage v-bind:user="'user'"/></div>
            </div>
        </div>

        <AddTripForm v-if="showTripForm" @addTripRequest="addTripRequest" @close="showTripForm = false" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import AddTripForm from '../components/AddTripForm.vue';
import TripPage from '../components/Center/TripPage.vue';
import TripRequestPage from '../components/Center/TripRequestPage.vue';
import FrontPage from '../components/Center/FrontPage.vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import Sidebar from '../components/Sidebar/Sidebar.vue'
import { sidebarWidth } from '../components/Sidebar/state.js'

const data = reactive(
    {minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "Me", email:"me@princeton.edu", phone:"666-666-6666", luggage: 3},
)

const participants = reactive([
    {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
])

const joinRequests = reactive([
    {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
])

const confirmationRequests = reactive([
    {id: 0, status: "Sent", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    {id: 1, status: "Rejected", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
])

// ground truth data
const user = reactive({ first_name: "", id: -1, })
const trips = ref([{id: 0, data: data, participants: participants, joinRequests: joinRequests, confirmationRequests: confirmationRequests}]);
const tripRequests = ref([{id: 0, data: data, participants: participants, joinRequests: joinRequests, confirmationRequests: confirmationRequests}]);

// display vars
const centerDisplay = ref({ type: "default", id: 0 });
const showTripForm = ref(false)

onMounted(async () => {
    await getUserInfo();
    await getUserTrips();
});

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
}

async function addTripRequest(newTripRequest) {
    //tripRequests.value.push(newTripRequest);

    let departure = {
        "address": newTripRequest.from,
        "postal_code": newTripRequest.fromPostalCode,
    }
    let arrival = {
        "address": newTripRequest.to,
        "postal_code": newTripRequest.toPostalCode,
    }

    // NOTE: why are we taking the substring again?
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
        alert(formatError(error.response.data.error));
        return;
    }
    
    showTripForm.value = false;

    getUserTrips();
}

async function editTrip(id, changes) {
     
}

async function getConfirmationRequests() {
    const endpoint = `${endpoints["confirmationRequests"]}`;
    const response = await axios.get(endpoint);
    confRequests.value = response.data;
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
  
  function acceptConfirmationRequest(id) {
      const index = confRequests.findIndex(conf => conf.id === id);
      if (index !== -1) {
        const endpoint = `${endpoints["confirmationRequest"]}${id}/accept/`;
        try {
          axios.delete(endpoint);
          getUserTrips();
          getConfirmationRequests();
        } catch (error) {
          alert(formatError(error.response.data.error));
          return;
        }
      }
  }
  
  function rejectConfirmationRequest(id) {
      const index = confRequests.findIndex(conf => conf.id === id);
      if (index !== -1) {
        const endpoint = `${endpoints["confirmationRequest"]}${id}/reject/`;
        try {
          axios.delete(endpoint);
          getUserTrips();
          getConfirmationRequests();
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

</script>

<style>
.dashboard {
    /* max-width: 1000px; */
    height: 100%;
    /* margin: 40px auto; */
    /* padding: 20px; */
    font-family: 'Roboto', sans-serif;
}

.card {
    background-color:  	#DCDCDC;
    border-color:  	#DCDCDC;
}
.padding {
    padding: 10px;
    width: 100%;
    height: 100%;
    /* box-sizing: border-box; */
    display: flex;
    border-radius: 20px;
}
</style>
