<template>
    <div v-if="tripRequests.length==0">
        <h4 class="mt-2">No trip requests yet.</h4>
    </div>
    <div v-else>
      <div class="accordion" id="accordion">
        <div v-for="tripRequest in sortedTripRequests" :key="'tripRequest'+tripRequest.id" class="accordion-item" :class="{'trip-request-blue': tripRequest.status === 'pending'}">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="'#tripRequest'+tripRequest.id"
            >
              {{ cleanLocation(tripRequest.departure_location) }} &#8594; {{ cleanLocation(tripRequest.arrival_location) }} between
              {{ getTime(tripRequest.earliest_departure_time) }} and {{ getTime(tripRequest.latest_departure_time) }} {{ getDatePart(tripRequest.earliest_departure_time, tripRequest.latest_departure_time) }}
            </button>
            <button class="btn btn-danger btn-sm ms-1" @click="removeTripRequest(tripRequest.id)">Remove Trip</button>
          </h2>
          <div
            :id="'tripRequest'+tripRequest.id"
            class="accordion-collapse collapse"
            data-bs-parent="#accordion"
          >
          <div class="accordion-body">
                <div class='mb-2'>
                    <h5 class="mt-2 text-start">Trip matches:</h5>
                    <div v-if="tripRequest.join_requests.length==0">
                        <p class="text-start">No requests to join yet.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <p class="text-start">Note: the following information represents the trips <strong>before</strong> your possible addition.</p>
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Departure location</th>
                                    <th scope="col" class="column">Arrival location</th>
                                    <th scope="col" class="column">Earliest departure time</th>
                                    <th scope="col" class="column">Latest departure time</th>
                                    <th scope="col" class="column">Luggage bag total</th>
                                    <th scope="col" class="column">Number of riders</th>
                                    <th scope="col" class="columnend"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="join in tripRequest.join_requests" :key="join.id" :class="{'join-request-orange': join.status === 'pending'}">
                                    <td>{{ cleanLocation(join.trip.departure_location) }}</td>
                                    <td>{{ cleanLocation(join.trip.arrival_location) }}</td>
                                    <td>{{ getTime(join.trip.earliest_departure_time) + " (" + getDate(join.trip.earliest_departure_time) + ")" }}</td>
                                    <td>{{ getTime(join.trip.latest_departure_time) + " (" + getDate(join.trip.latest_departure_time) + ")" }}</td>
                                    <td>{{ join.trip.num_luggage_bags }}</td>
                                    <td>{{ join.trip.num_participants }}</td>
                                    <td>
                                        <button class="btn btn-primary btn-sm ms-1" @click="rejectJoinRequest(join.id)">Withdraw Request</button>
                                    </td>
                                    </tr>
                            </tbody>
                        </table>
                    </div>
                    <h5 class="mt-2 text-start">Confirmation requests:</h5>
                    <div v-if="tripRequest.confirmation_requests.length==0">
                        <p class="text-start">No confirmations yet.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <p class="text-start">Note: the following information represents the trips <strong>after</strong> your possible addition.</p>
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Departure location</th>
                                    <th scope="col" class="column">Arrival location</th>
                                    <th scope="col" class="column">Earliest departure time</th>
                                    <th scope="col" class="column">Latest departure time</th>
                                    <th scope="col" class="column">Luggage bag total</th>
                                    <th scope="col" class="column">Number of riders</th>
                                    <th scope="col" class="columnend"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="confirm in tripRequest.confirmation_requests" :key="confirm.id" :class="{'confirmation-request-green': confirm.status === 'confirmed'}">
                                    <td>{{ cleanLocation(confirm.join_request.trip.departure_location) }}</td>
                                    <td>{{ cleanLocation(confirm.join_request.trip.arrival_location) }}</td>
                                    <td>{{ getTime(confirm.join_request.trip.earliest_departure_time) + " (" + getDate(confirm.join_request.trip.earliest_departure_time) + ")"  }}</td>
                                    <td>{{ getTime(confirm.join_request.trip.latest_departure_time) + " (" + getDate(confirm.join_request.trip.latest_departure_time) + ")"  }}</td>
                                    <td>{{ confirm.join_request.trip.num_luggage_bags + tripRequest.num_luggage_bags }}</td>
                                    <td>{{ confirm.join_request.trip.num_participants + 1}}</td>
                                    <td>
                                        <button class="btn btn-accept btn-sm me-1" @click="acceptConfirmationRequest(confirm.id)">Accept</button>
                                        <button class="btn btn-reject btn-sm ms-1" @click="rejectConfirmationRequest(confirm.id)">Reject</button>
                                    </td>
                                </tr>
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
import { getDate, getDatePart, getTime, cleanLocation, nameList } from '../components/common.js'
import { toRefs } from 'vue'

const emit = defineEmits(['refreshTrips', 'goToTripsTab']);
const props = defineProps(['tripRequests']);
const { tripRequests } = toRefs(props);

const sortedTripRequests = computed(() => {
    return [...tripRequests.value].sort((a, b) => {
        return new Date(a.earliest_departure_time) - new Date(b.earliest_departure_time);
    });
});

function acceptConfirmationRequest(confirmationID) {
    const endpoint = `${endpoints["confirmationRequests"]}${confirmationID}/?action=accept`;
    console.log(endpoint)
    try {
        axios.post(endpoint);
        emit('refreshTrips');
        emit('goToTripsTab')
    } catch (error) {
        alert(error);
        return;
    }
}

function rejectConfirmationRequest(confirmationID) {
    const endpoint = `${endpoints["confirmationRequests"]}${confirmationID}/?action=reject`;
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

 async function removeTripRequest(tripRequestID) {
    if (confirm('Are you sure you want to remove this trip request?')) {
        const endpoint = `${endpoints["deleteTripRequest"]}${tripRequestID}`;
        try {
            await axios.post(endpoint);
            emit('refreshTrips');
        } catch (error) {
            alert(error);
            return;
        }
    }
}

// const luggageTotal = computed(() => {
//     // get all trips from trip request join requests
//     tripRequest.join_requests[0].trip
//     const trips =  

//     return trips.value.map(trip => {
//         const totalLuggage = trip.participant_list.reduce((total, participant) => {
//             return total + participant.num_luggage_bags;
//         }, 0);
//         return { ...trip, totalLuggage };
//     });
// });
</script>

<style>
.btn-accept {
    background-color: green;
    color: white;
}

.btn-reject {
    background-color: red;
    color: white;
}
.trip-request-blue {
    background-color: blue;
}

.join-request-orange {
    background-color: orange;
}

.confirmation-request-green {
    background-color: green;
}
</style>
