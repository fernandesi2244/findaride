<template>
    <div>
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
              {{ getTime(trip.departure_time) }}, {{ getDate(trip.departure_time) }}
            </button>
          </h2>
          <div
            :id="trip.college+trip.id"
            class="accordion-collapse collapse"
            data-bs-parent="#accordion"
          >
            <div class="accordion-body">
                <div class='mb-2'>
                    <h5 class="text-start">Members:
                        {{ nameList(trip.participant_list) }}
                    </h5>

                    <h6 class="mt-4 text-start">Join requests</h6>
                    <div v-if="trip.join_requests.length==0">
                        <p class="text-start">No requests to join yet.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table bdr">
                            <thead>
                                <tr>
                                    <th scope="col" class="column">Name</th>
                                    <th scope="col" class="column">Min Time</th>
                                    <th scope="col" class="column">Max Time</th>
                                    <th scope="col" class="column">Departure</th>
                                    <th scope="col" class="column">Arrival</th>
                                    <th scope="col" class="column">Luggage</th>
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
                                        <button class="btn btn-primary btn-sm me-1" @click="acceptJoinRequest(join.id)">Accept</button>
                                        <button class="btn btn-primary btn-sm ms-1" @click="rejectJoinRequest(join.id)">Reject</button>
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

const props = defineProps(['trips']);
const { trips } = toRefs(props);
</script>

<style>
</style>
