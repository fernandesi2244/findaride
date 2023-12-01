<template>
    <div class="container-xl pt-4">
      <div class="narrow-container">
        <h2 class="text-start">{{ user.first_name }} {{ user.last_name }} <span class="text-secondary text-small">({{ user.college_display }})</span></h2>
        <!--TODO: insert cute section with ur stats eg how many trips, how many miles traveled etc-->
        <h4>Your past trips</h4>
        <div class="accordion" id="accordion">
            <div v-for="trip in pastTrips" :key="trip.college+trip.id" class="accordion-item">
            <h2 class="accordion-header">
                <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="'#'+trip.college+trip.id"
                >
                    {{ cleanLocation(trip.departure_location) }} &#8594; {{ cleanLocation(trip.arrival_location) }} on {{ getDate(trip.latest_departure_time) }}
                </button>
            </h2>
            <div
                :id="trip.college+trip.id"
                class="accordion-collapse collapse"
                
            >
                <div class="accordion-body">
                    <div class='mb-2'>
                        <div class="flex">
                            <div>
                                <h5 class="text-start">Members:<br></h5>
                                <!-- put each member on a separate line -->
                                <h6 v-for="participant in trip.participant_list" class="text-start">
                                    {{ nameEmail(participant) }}
                                </h6>
                            </div>
                        </div>

                        <br>
                        <h5 class="text-start">Number of luggage bags: <span>{{ trip.num_luggage_bags }}</span></h5>
                    </div>
                </div>
            </div>
            </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed} from 'vue';
  import { getDatePart, getDate, getTime, cleanLocation, nameEmail } from '../components/common.js'
  import { endpoints } from '../common/endpoints.js';
  import { axios } from '../common/axios_service.js'
  
  // ground truth data
  const user = reactive({ first_name: "", id: -1, })
  const trips = ref([]);
  const userID = ref(0);
  
  const pastTrips = computed(() => {
    return trips.value.filter((item) => {
      return !item.is_active;
    });
  })
  

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
  }
  
  async function getUserTrips() {
    const endpoint = `${endpoints["userTrips"]}${user.id}/`;
    const response = await axios.get(endpoint);
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
  }

  .text-small {
    font-size: 16px;
  }
  
  .accordion {
    height: 500px;
    overflow-y: scroll;
    border: 2px solid rgb(203, 203, 203);
    border-radius: 5px;
  }
  </style>