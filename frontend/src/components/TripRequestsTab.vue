<template>
    <div v-if="tripRequests.length == 0">
        <h4 class="mt-2">No trip requests yet.</h4>
    </div>
    <div v-else>
        <div class="accordion" id="accordion">
            <div v-for="tripRequest in sortedTripRequests" :key="'tripRequest' + tripRequest.id" class="accordion-item"
                :class="{ 'trip-request-blue': tripRequest.status === 'pending' }">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                        :data-bs-target="'#tripRequest' + tripRequest.id">
                        {{ cleanLocation(tripRequest.departure_location) }} &#8594; {{
                            cleanLocation(tripRequest.arrival_location) }} between
                        {{ getTime(tripRequest.earliest_departure_time) }} and {{ getTime(tripRequest.latest_departure_time)
                        }} {{ getDatePart(tripRequest.earliest_departure_time, tripRequest.latest_departure_time) }}
                    </button>
                </h2>
                <div :id="'tripRequest' + tripRequest.id" class="accordion-collapse collapse" data-bs-parent="#accordion">
                    <div class="accordion-body">
                        <div class='mb-2'>
                            <div class="flex">
                                <h5 class="mt-2 text-start">Trip matches:</h5>
                                <div class="hug-right">
                                    <button class="btn btn-danger btn-sm ms-1"
                                        @click="removeTripRequest(tripRequest.id)">Remove trip</button>
                                </div>
                            </div>

                            <div v-if="tripRequest.join_requests.length == 0">
                                <p class="text-start">No requests to join yet.</p>
                            </div>
                            <div v-else class="table-responsive">
                                <p class="text-start">Note: the following information represents the trips
                                    <strong>before</strong> your possible addition.</p>
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
                                        <!-- TODO: Fix display when there are no join requests as a result of the filter check on the next line. -->
                                        <tr v-for="join in tripRequest.join_requests.filter(joinRequest => !hasConfirmationRequest(tripRequest, joinRequest))"
                                            :key="join.id" :class="{ 'join-request-orange': join.status === 'pending' }">
                                            <td>{{ cleanLocation(join.trip.departure_location) }}</td>
                                            <td>{{ cleanLocation(join.trip.arrival_location) }}</td>
                                            <td>{{ getTime(join.trip.earliest_departure_time) + " (" +
                                                getDate(join.trip.earliest_departure_time) + ")" }}</td>
                                            <td>{{ getTime(join.trip.latest_departure_time) + " (" +
                                                getDate(join.trip.latest_departure_time) + ")" }}</td>
                                            <td>{{ join.trip.num_luggage_bags }}</td>
                                            <td>{{ join.trip.num_participants }}</td>
                                            <td>
                                                <button class="btn-text withdraw-btn in-row-btn"
                                                    @click="rejectJoinRequest(join.id)">Withdraw</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <h5 class="mt-2 text-start">Confirmation requests:</h5>
                            <div v-if="tripRequest.confirmation_requests.length == 0">
                                <p class="text-start">No confirmations yet.</p>
                            </div>
                            <div v-else class="table-responsive">
                                <p class="text-start">Note: the following information represents the trips
                                    <strong>after</strong> your possible addition.</p>
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
                                        <tr v-for="confirm in tripRequest.confirmation_requests" :key="confirm.id"
                                            :class="{ 'confirmation-request-green': confirm.status === 'confirmed' }">
                                            <td>{{ cleanLocation(confirm.join_request.trip.departure_location) }}</td>
                                            <td>{{ cleanLocation(confirm.join_request.trip.arrival_location) }}</td>
                                            <td>{{ getTime(confirm.join_request.trip.earliest_departure_time) + " (" +
                                                getDate(confirm.join_request.trip.earliest_departure_time) + ")" }}</td>
                                            <td>{{ getTime(confirm.join_request.trip.latest_departure_time) + " (" +
                                                getDate(confirm.join_request.trip.latest_departure_time) + ")" }}</td>
                                            <td>{{ confirm.join_request.trip.num_luggage_bags + tripRequest.num_luggage_bags
                                            }}</td>
                                            <td>{{ confirm.join_request.trip.num_participants + 1 }}</td>
                                            <td>
                                                <button class="btn-text btn-accept in-row-btn"
                                                    @click="acceptConfirmationRequest(confirm.id)">Accept</button>
                                                <button class="btn-text btn-reject in-row-btn"
                                                    @click="rejectConfirmationRequest(confirm.id)">Reject</button>
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
        <!-- <button @click="toggleHelp" class="need-help-btn">Need Help</button> -->
        <TripRequestsHelpModal ref="tripRequestsHelpModal"></TripRequestsHelpModal>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted, reactive, computed } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import { getDate, getDatePart, getTime, cleanLocation, nameList } from '../components/common.js'
import { toRefs } from 'vue'

const emit = defineEmits(['refreshTrips', 'goToTripsTab', 'goToTripRequestsTab']);
import TripRequestsHelpModal from '../components/TripRequestsHelpModal.vue';

const props = defineProps(['tripRequests']);
const { tripRequests } = toRefs(props);
const tripRequestsHelpModal = ref(null)

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

function hasConfirmationRequest(tripRequest, joinRequest) {
    return tripRequest.confirmation_requests.some(confirmationRequest => confirmationRequest.join_request.id === joinRequest.id);
}

function toggleHelp() {
    tripRequestsHelpModal.value.show();
}

function rejectConfirmationRequest(confirmationID) {
    const endpoint = `${endpoints["confirmationRequests"]}${confirmationID}/?action=reject`;
    try {
        axios.post(endpoint);
        emit('refreshTrips');
        emit('goToTripsTab')  // temp fix to refresh confirmation requests; TODO: STAY ON PAGE unless there are no more confirmation requests
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
        const endpoint = `${endpoints["deleteTripRequest"]}${tripRequestID}/`;
        try {
            await axios.delete(endpoint);
            emit('refreshTrips');
        } catch (error) {
            alert(error);
            return;
        }
    }
}
</script>

<style>
.btn-accept {
    background-color: green;
    color: white;
    width: 60px;
}

.btn-reject {
    background-color: red;
    color: white;
    width: 60px;
}

.withdraw-btn {
    width: 80px;
    background-color: #0d6efd;
    color: white;
}

.btn-text {
    border: none;
    margin: 0;
    padding: 0px 1px 0px 1px;
    cursor: pointer;
    white-space: nowrap;
    /* box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.2); */
}

.in-row-btn {
    border-radius: 6px;
    padding: 1px;
    display: flex;
    justify-content: center;
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

.flex {
    display: flex;
}

.hug-right {
    margin-left: auto;
}

.need-help-btn {
    background-color: var(--primary-color);
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
}

.accordion+.need-help-btn {
    display: block;
    margin-left: auto;
    margin-top: 15px;
}</style>
