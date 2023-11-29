<template>
    <div v-if="trips.length==0">
        <h4 class="mt-2">No trips yet.</h4>
    </div>
    <div v-else>
      <div class="accordion" id="accordion">
        <div v-for="trip in sortedTrips" :key="trip.college+trip.id" class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="'#'+trip.college+trip.id"
            >
              {{ cleanLocation(trip.departure_location) }} &#8594; {{ cleanLocation(trip.arrival_location) }} between
              {{ getTime(trip.earliest_departure_time) }} and {{ getTime(trip.latest_departure_time) }} {{ getDatePart(trip.earliest_departure_time, trip.latest_departure_time) }}
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
                        <div class="hug-right">
                            <button class="btn btn-danger" @click="removeTrip(trip.id)">Leave</button>
                        </div>
                    </div>

                    <br>
                    <h5 class="text-start">Number of luggage bags: <span>{{ trip.num_luggage_bags }}</span></h5>

                    <h5 class="mt-4 text-start">Join requests:</h5>
                    <div v-if="trip.join_requests.length==0">
                        <h6 class="text-start">No requests to join yet.</h6>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Name</th>
                                    <th scope="col" class="column">Earliest time</th>
                                    <th scope="col" class="column">Latest time</th>
                                    <th scope="col" class="column">Departure</th>
                                    <th scope="col" class="column">Arrival</th>
                                    <th scope="col" class="column">Bags</th>
                                    <th scope="col" class="column"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <template v-for="join in trip.join_requests" :key="join.id">

                                <tr>
                                    <td class="no-border">{{ join.trip_request.user.first_name }} {{ join.trip_request.user.last_name }}</td>
                                    <td class="no-border">{{ getTime(join.trip_request.earliest_departure_time) + " (" + getDate(join.trip_request.earliest_departure_time) + ")" }}</td>
                                    <td class="no-border">{{ getTime(join.trip_request.latest_departure_time) + " (" + getDate(join.trip_request.latest_departure_time) + ")" }}</td>
                                    <td class="no-border">{{ cleanLocation(join.trip_request.departure_location) }}</td>
                                    <td class="no-border">{{ cleanLocation(join.trip_request.arrival_location) }}</td>
                                    <td class="no-border">{{ join.trip_request.num_luggage_bags }}</td>
                                    <td class="no-border">
                                        <div v-if="join.participants_that_accepted.includes(userID)">
                                            <!-- check if there are other members of the trip that need to approve the reqeust -->
                                            <div v-if="join.participants_that_accepted.length < trip.num_participants">
                                                Waiting for other members...
                                            </div>
                                            <div v-else>
                                                Waiting for response...
                                            </div>
                                        </div>
                                        <div class="" v-else>
                                            <button class="btn btn-accept btn-sm me-1" @click="acceptJoinRequest(join.id)">Accept</button>
                                            <button class="btn btn-reject btn-sm ms-1" @click="rejectJoinRequest(join.id)">Reject</button>
                                        </div>
                                    </td>
                                    
                                </tr>
                                <tr>
                                    <td colspan="30">
                                        <table class="text-muted">
                                            &#x21B3; 
                                            Comments: {{ join.trip_request.comment }}
                                        </table>
                                    </td>
                                </tr>
                                
                            </template>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { defineProps, onMounted, reactive, computed } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import { getDatePart, getDate, getTime, cleanLocation, nameEmail } from '../components/common.js'
import { toRefs } from 'vue'

const emit = defineEmits(['refreshTrips']);
const props = defineProps(['trips', 'userID']);
const { trips, userID } = toRefs(props);
const sortedTrips = computed(() => {
    return [...trips.value].sort((a, b) => {
        return new Date(a.earliest_departure_time) - new Date(b.earliest_departure_time);
    });
});
function acceptJoinRequest(joinID) {
    const endpoint = `${endpoints["joinRequests"]}${joinID}/?action=accept`;
    console.log(endpoint)
    try {
        axios.post(endpoint);
        emit('refreshTrips');
    } catch (error) {
        alert(error);
        return;
    }
}

function rejectJoinRequest(joinID) {
    const endpoint = `${endpoints["joinRequests"]}${joinID}/?action=reject`;
    try {
        axios.post(endpoint);
        emit('refreshTrips');
    } catch (error) {
        alert(error);
        return;
    }
}

function removeTrip(tripRequestID) {
    
    if (confirm('Are you sure you want to remove this trip?')) {
        const endpoint = `${endpoints["deleteTripRequest"]}${tripRequestID}`;
        try {
            axios.post(endpoint);
            emit('refreshTrips');
        } catch (error) {
            alert(error);
            return;
        }
    }
}
</script>

<style>
.flex {
    display: flex;
}

.hug-right {
    margin-left: auto;    
}

.button-div {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}
.btn-accept {
    background-color: green;
    color: white;
}

.btn-reject {
    background-color: red;
    /* color: red; */

}
.btn-reject:hover {
    background-color: #a90505;
    /* color: red; */
    
}

.no-border {
    border: none;
}
</style>
