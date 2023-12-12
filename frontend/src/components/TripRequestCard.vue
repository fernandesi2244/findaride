<template>
<h2 class="accordion-header">
    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
        :data-bs-target="'#tripRequest' + tripRequest.id">
        <span class="location">
        {{ cleanLocation(tripRequest.departure_location) }} &#8594; {{ cleanLocation(tripRequest.arrival_location) }} 
        </span>
        <span class="date">
        {{ getDate(tripRequest.earliest_departure_time) }}
        </span>
        <span class="time">
        <!-- {{ getTime(tripRequest.earliest_departure_time) }} and {{ getTime(tripRequest.latest_departure_time) }}
        {{ getDatePart(tripRequest.earliest_departure_time, tripRequest.latest_departure_time) }} -->
        {{ getTimeRange(tripRequest.earliest_departure_time, tripRequest.latest_departure_time) }} <sup>{{ getDateDiff(tripRequest.earliest_departure_time, tripRequest.latest_departure_time) }}</sup>
        </span>
        <span class="status">
            Waiting for groups
        </span>
    </button>
</h2>
<div :id="'tripRequest' + tripRequest.id" class="accordion-collapse collapse">
    <div class="accordion-body">
        <div class='mb-2'>
            <div class="flex">
                <h5 class="mt-2 text-start">Your requests</h5>
                <div class="hug-right">
                    <button class="btn btn-danger btn-sm ms-1"
                        @click="emit('removeTripRequest', tripRequest.id)">Delete trip</button>
                </div>
            </div>

            <div v-if="tripRequest.join_requests.filter(joinRequest => !hasConfirmationRequest(tripRequest, joinRequest)).length == 0">
                <p class="text-start">You have no active requests.</p>
            </div>
            <div v-else class="table-responsive">
                <p class="text-start">Note: the following information represents the trips
                    <strong>before</strong> your possible addition.</p>
                <table class="table bdr">
                    <thead>
                        <tr>
                            <th scope="col" class="column">Number of riders</th>
                            <th scope="col" class="column">Departure</th>
                            <th scope="col" class="column">Arrival</th>
                            <th scope="col" class="column">Earliest time</th>
                            <th scope="col" class="column">Latest time</th>
                            <th scope="col" class="column">Bags</th>
                            <th scope="col" class="column" style="max-width: 125px;"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- TODO: Fix display when there are no join requests as a result of the filter check on the next line. -->
                        <tr v-for="join in tripRequest.join_requests.filter(joinRequest => !hasConfirmationRequest(tripRequest, joinRequest))"
                            :key="join.id" :class="{ 'join-request-orange': join.status === 'pending' }">
                            <td>{{ join.trip.num_participants }}</td>
                            <td>{{ cleanLocation(join.trip.departure_location) }}</td>
                            <td>{{ cleanLocation(join.trip.arrival_location) }}</td>
                            <td>{{ getTime(join.trip.earliest_departure_time) + " (" +
                                getDate(join.trip.earliest_departure_time) + ")" }}</td>
                            <td>{{ getTime(join.trip.latest_departure_time) + " (" +
                                getDate(join.trip.latest_departure_time) + ")" }}</td>
                            <td>{{ join.trip.num_luggage_bags }}</td>
                            <td>
                                <button class="btn-text withdraw-btn"
                                    @click="emit('rejectJoinRequest', join.id)">Withdraw</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
        <!-- <TripRequestsHelpModal ref="tripRequestsHelpModal"></TripRequestsHelpModal> -->
</template>

<script setup>
import { toRefs, defineProps, defineEmits, computed } from 'vue';
import { getDatePart, getDate, getTime, cleanLocation, getDateDiff, getTimeRange } from '../components/common.js'

const props = defineProps(['tripRequest'])
const { tripRequest } = toRefs(props)

const emit = defineEmits(['removeTripRequest', 'rejectJoinRequest'])

function hasConfirmationRequest(tripRequest, joinRequest) {
    // return false
    return tripRequest.confirmation_requests.some(confirmationRequest => confirmationRequest.join_request.id === joinRequest.id);
}

</script>

<style>
.flex {
    display: flex;
    margin-left: auto;
}

.location {
    width: 30%;
}
.date {
    width: 20%;
}
.time {
    width: 30%;
}
.status {
    width:20%;
    text-align: right;
    padding-right: 10px;
}
</style>