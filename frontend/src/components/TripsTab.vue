<template>
    <div v-if="trips.length==0">
        <h4 class="mt-2">No trips yet.</h4>
    </div>
    <div v-else>
      <div class="accordion" id="accordion">
        <div v-for="trip in trips" :key="trip.college+trip.id" class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="'#'+trip.college+trip.id"
            >
              {{ cleanLocation(trip.departure_location) }} &#8594; {{ cleanLocation(trip.arrival_location) }} @
              {{ getTime(trip.departure_time) }} on {{ getDate(trip.departure_time) }}
            </button>
          </h2>
          <div
            :id="trip.college+trip.id"
            class="accordion-collapse collapse"
            data-bs-parent="#accordion"
          >
            <div class="accordion-body">
                <div class='mb-2'>
                    <h5 class="text-start">Members:<br></h5>
                    <!-- put each member on a separate line -->
                    <h6 v-for="participant in trip.participant_list" class="text-start">
                        {{ nameEmail(participant) }}
                    </h6>

                    <h5 class="mt-4 text-start">Join requests:</h5>
                    <div v-if="trip.join_requests.length==0">
                        <h6 class="text-start">No requests to join yet.</h6>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Name</th>
                                    <th scope="col" class="column">Min time</th>
                                    <th scope="col" class="column">Max time</th>
                                    <th scope="col" class="column">Departure</th>
                                    <th scope="col" class="column">Arrival</th>
                                    <th scope="col" class="column">Bags</th>
                                    <th scope="col" class="columnend"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="join in trip.join_requests" :key="join.id">
                                    <td>{{ join.trip_request.user.first_name }} {{ join.trip_request.user.last_name }}</td>
                                    <td>{{ getTime(join.trip_request.earliest_departure_time) }}</td>
                                    <td>{{ getTime(join.trip_request.latest_departure_time) }}</td>
                                    <td>{{ cleanLocation(join.trip_request.departure_location) }}</td>
                                    <td>{{ cleanLocation(join.trip_request.arrival_location) }}</td>
                                    <td>{{ join.trip_request.num_luggage_bags }}</td>
                                    <td>
                                        <div v-if="join.participants_that_accepted.includes(userID)">
                                            <!-- check if there are other members of the trip that need to approve the reqeust -->
                                            <div v-if="join.participants_that_accepted.length < trip.num_participants">
                                                Waiting for other members...
                                            </div>
                                            <div v-else>
                                                Waiting for response...
                                            </div>
                                        </div>
                                        <div class="button-div" v-else>
                                            <button class="btn btn-primary btn-sm me-1" @click="acceptJoinRequest(join.id)">Accept</button>
                                            <button class="btn btn-primary btn-sm ms-1" @click="rejectJoinRequest(join.id)">Reject</button>
                                        </div>
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
import { defineProps, onMounted, reactive } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import { getDate, getDateTime, getTime, cleanLocation, nameEmail } from '../components/common.js'
import { toRefs } from 'vue'

const emit = defineEmits(['refreshTrips']);
const props = defineProps(['trips', 'userID']);
const { trips, userID } = toRefs(props);

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
</script>

<style>
.button-div {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}
</style>
