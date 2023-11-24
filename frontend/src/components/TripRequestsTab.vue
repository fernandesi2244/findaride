<template>
    <div v-if="tripRequests.length==0">
        <h4 class="mt-2">No trip requests yet.</h4>
    </div>
    <div v-else>
      <div class="accordion" id="accordion">
        <div v-for="tripRequest in tripRequests" :key="'tripRequest'+tripRequest.id" class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="'#tripRequest'+tripRequest.id"
            >
              {{ cleanLocation(tripRequest.departure_location) }} &#8594; {{ cleanLocation(tripRequest.arrival_location) }} @
              {{ getTime(tripRequest.earliest_departure_time) }} ~ {{ getTime(tripRequest.latest_departure_time) }},
              {{ getDate(tripRequest.latest_departure_time) }}
            </button>
          </h2>
          <div
            :id="'tripRequest'+tripRequest.id"
            class="accordion-collapse collapse"
            data-bs-parent="#accordion"
          >
          <div class="accordion-body">
                <div class='mb-2'>
                    <h6 class="mt-2 text-start">Join Requests:</h6>
                    <div v-if="tripRequest.join_requests.length==0">
                        <p class="text-start">No requests to join yet.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Time</th>
                                    <th scope="col" class="column"># Luggages</th>
                                    <th scope="col" class="column"># Riders</th>
                                    <th scope="col" class="column">Status</th>
                                    <th scope="col" class="columnend"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="join in tripRequest.join_requests" :key="join.id">
                                    <td>{{ getTime(join.trip.departure_time) }}</td>
                                    <td>{{ join.trip.num_luggage_bags }}</td>
                                    <td>{{ join.trip.num_participants }}</td>
                                    <td>Status</td>
                                    <td>
                                        <button class="btn btn-primary btn-sm ms-1" @click="rejectJoinRequest(join.id)">Withdraw Request</button>
                                    </td>
                                    </tr>
                            </tbody>
                        </table>
                    </div>
                    <h6 class="mt-2 text-start">Cofirmation Requests:</h6>
                    <div v-if="tripRequest.confirmation_requests.length==0">
                        <p class="text-start">No confirmations yet.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Time</th>
                                    <th scope="col" class="column"># Luggages</th>
                                    <th scope="col" class="column"># Riders</th>
                                    <th scope="col" class="columnend"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="confirm in tripRequest.confirmation_requests" :key="confirm.id">
                                    <td>{{ getTime(confirm.join_request.trip.departure_time) }}</td>
                                    <td>{{ confirm.join_request.trip.num_luggage_bags }}</td>
                                    <td>{{ confirm.join_request.trip.num_participants }}</td>
                                    <td>
                                        <button class="btn btn-primary btn-sm me-1" @click="acceptConfirmationRequest(confirm.id)">Accept</button>
                                        <button class="btn btn-primary btn-sm ms-1" @click="rejectConfirmationRequest(confirm.id)">Reject</button>
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
import { getDate, getDateTime, getTime, cleanLocation, nameList } from '../components/common.js'
import { toRefs } from 'vue'

const props = defineProps(['tripRequests']);
const { tripRequests } = toRefs(props);

function acceptConfirmationRequest(confirmationID) {
    const endpoint = `${endpoints["confirmationRequests"]}${confirmationID}/?action=accept`;
    console.log(endpoint)
    try {
        axios.post(endpoint);
    //   getUserTrips();
    //   getConfirmationRequests();
    } catch (error) {
        alert(error);
        return;
    }
}

function rejectConfirmationRequest(confirmationID) {
    const endpoint = `${endpoints["confirmationRequests"]}${confirmationID}/?action=reject`;
    try {
        axios.post(endpoint);
        // getUserTrips();
        // getConfirmationRequests();
    } catch (error) {
        alert(error);
        return;
    }
}
</script>

<style>
</style>
