<template>
  <div class="container-xl pt-4">
    <div class="narrow-container-profile">
      <h2 class="text-start">{{ user.first_name }} {{ user.last_name }} </h2>
      <div class="mt-4">
        <h4 class="text-start">
          Thank you for using findaride!
        </h4>
        <h5 class="text-start mt-3">
          During your time with us, you have
        </h5>
      </div>
      <div class="row mt-4 mb-3">
        <div class="col-4 col-padding px-4">
          <p class="text-start">
            been on
          </p>
          <p class="big-text">
            {{ userStats.number_trips }}
          </p>
          <p class="text-end">
            trips
          </p>
        </div>
        <div class="col-4 col-padding">
          <p class="text-start">
            traveled
          </p>
          <p class="big-text">
            {{ userStats.miles_ridden }}
          </p>
          <p class="text-end">
            miles
          </p>
        </div>
        <div class="col-4 col-padding">
          <p class="text-start">
            shared rides with
          </p>
          <p class="big-text">
            {{ userStats.number_riders }}
          </p>
          <p class="text-end">
            people
          </p>
        </div>
      </div>
      <h4>Your past trips</h4>
      <div v-if="trips.length > 0" class="past-trips accordion" id="accordion">
        <div v-for="trip in trips" :key="trip.college + trip.id" class="accordion-item accordion-profile-item">
          <h2 class="accordion-header accordion-profile-header">
            <button class="accordion-button accordion-profile-button collapsed" type="button" data-bs-toggle="collapse"
              :data-bs-target="'#' + trip.college + trip.id">
              {{ cleanLocation(trip.departure_location) }} &#8594; {{ cleanLocation(trip.arrival_location) }}
              between
              {{ getTime(trip.earliest_departure_time) }} and {{ getTime(trip.latest_departure_time) }} {{
                getDatePart(trip.earliest_departure_time, trip.latest_departure_time) }}
            </button>
          </h2>
          <div :id="trip.college + trip.id" class="accordion-collapse collapse">
            <div class="accordion-body">
              <div class='mb-2'>
                <div class="flex">
                  <h5 class="text-start margin-right-1 header-border">Members<br></h5>
                  <div class="text-start">Luggage bags: <span>{{ trip.num_luggage_bags }}</span></div>
                </div>
                <h6 v-for="participant in trip.participant_list" class="text-start">
                    {{ nameEmail(participant) }}
                </h6>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        You do not have any past trips.
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { getDatePart, getDate, getTime, cleanLocation, nameEmail } from '../components/common.js'
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'

// ground truth data
const user = reactive({ first_name: "", id: -1, })
const userStats = reactive({
  number_riders: 0,
  number_trips: 0,
  miles_ridden: 0,
  past_riders: 0,
  id: -1,
})
const trips = ref([]);
const userID = ref(0);

const addTripModal = ref(null)

async function refreshData() {
  getUserInfo();
  getUserTrips();
}

onMounted(async () => {
  await getUserInfo();
  await getUserTrips();
});

async function getUserInfo() {
  const endpoint = endpoints["me"];
  const response = await axios.get(endpoint);
  Object.assign(user, response.data);
  Object.assign(userStats, response.data.user_stats);
}

async function getUserTrips() {
  const endpoint = `${endpoints["userTrips"]}`;
  const response = await axios.get(endpoint, { params: { when: "past" } });
  trips.value = response.data.trips;

  userID.value = response.data.id;
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
body, .dashboard {
  font-family: 'Roboto', Arial, sans-serif;
  color: #4A4A4A;
  background-color: #F4F4F8;
}

.container-xl {
  padding: 0rem;
}

.narrow-container-profile {
  max-width: 90%;
  margin: 20px auto;
  background: #FFFFFF;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 2rem;
}

h2, h4, h5 {
  color: #333333;
  margin-bottom: 1rem;
}

.text-small {
  font-size: 0.9rem;
  color: #6C757D;
}

.big-text {
  font-size: 4rem;
  color: #007BFF;
}

.row {
  text-align: center;
}

.col-padding {
    padding: 15px;
}

.accordion-profile-header {
  margin-bottom: 10px;
}

@media (min-width: 768px) {
  .narrow-container-profile {
    max-width: 800px;
  }
}
</style>