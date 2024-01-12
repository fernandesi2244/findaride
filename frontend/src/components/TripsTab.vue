<template>
    <ConfirmDialogue ref="confirmDialogue" cancel-color="red"></ConfirmDialogue>
    <div v-if="trips.length == 0">
        <h4 class="mt-2">No trips yet.</h4>
    </div>
    <div v-else>
        <div class="accordion" id="accordion">
            <div v-for="trip in sortedTrips" :key="trip.college + trip.id" class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" @click="checkUpdate(trip.id)"
                        data-bs-toggle="collapse" :data-bs-target="'#' + trip.college + trip.id">
                        <!-- <span v-if="hasUpdate(trip.id)" class="dot"></span> -->
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
                                <div>
                                    <div class="flex">
                                        <h5 class="text-start margin-right-1 header-border">Members<br></h5>
                                        <div class="text-start">Luggage bags: <span>{{ trip.num_luggage_bags }}</span></div>
                                        <div class="">
                                            <label class="form-check-label margin-right-2">
                                                Mark trip as full
                                            </label>                                            
                                            <input @click="toggleTripIsFull(trip.id)" :checked="trip.is_full" class="form-check-input" type="checkbox" value="" :id="'check' + trip.id">
                                        </div>
                                    </div>
                                    <!-- put each member on a separate line -->
                                    <h6 v-for="participant in trip.participant_list" class="text-start">
                                        {{ nameEmail(participant) }}
                                    </h6>
                                    <div class="tooltip" style="margin-bottom: 10px;">
                                        <button class="btn-text copy-emails-btn"
                                            @click="copyEmailsOf(trip.participant_list, trip.id)">
                                            Copy emails
                                        </button>
                                        <span class="tooltiptext" :id="'copyTooltip' + trip.id">Copied to
                                            clipboard</span>
                                    </div>

                                </div>
                                <div class="hug-right">
                                    <button class="btn btn-danger btn-sm" @click="leaveTrip(trip.id)">Leave</button>
                                </div>
                            </div>
                            <h5 class="text-start">Join requests:</h5>
                            <div v-if="trip.join_requests.length == 0">
                                <h6 class="text-start">No requests to join yet.</h6>
                            </div>
                            <div v-else class="table-responsive">
                                <table class="table bdr">
                                    <thead>
                                        <tr>
                                            <th scope="col" class="column">Name</th>
                                            <th scope="col" class="column">Departure</th>
                                            <th scope="col" class="column">Arrival</th>
                                            <th scope="col" class="column">Earliest time</th>
                                            <th scope="col" class="column">Latest time</th>
                                            <th scope="col" class="column">Bags</th>
                                            <th scope="col" class="column"></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <template v-for="join in trip.join_requests" :key="join.id">

                                            <tr>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ join.trip_request.user.first_name }} {{
                                                    join.trip_request.user.last_name }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ cleanLocation(join.trip_request.departure_location)
                                                }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ cleanLocation(join.trip_request.arrival_location)
                                                }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ getTime(join.trip_request.earliest_departure_time)
                                                    + " (" + getDate(join.trip_request.earliest_departure_time) + ")" }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ getTime(join.trip_request.latest_departure_time) +
                                                    " (" + getDate(join.trip_request.latest_departure_time) + ")" }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">{{ join.trip_request.num_luggage_bags }}</td>
                                                <td v-bind:class="join.trip_request.comment?'no-border':''">
                                                    <div v-if="join.participants_that_accepted.includes(userID)">
                                                        <!-- check if there are other members of the trip that need to approve the reqeust -->
                                                        <div
                                                            v-if="join.participants_that_accepted.length < trip.num_participants">
                                                            Waiting for other members...
                                                        </div>
                                                        <div v-else>
                                                            Waiting for response...
                                                        </div>
                                                    </div>
                                                    <div v-else>
                                                        <button class="btn-text accept" role="button"
                                                            style="width:60px; margin-right:5px" @click="acceptJoinRequest(join.id)">Accept</button>
                                                        <button class="btn-text reject" role="button"
                                                            style="width:60px" @click="rejectJoinRequest(join.id)">Reject</button>
                                                    </div>
                                                </td>

                                            </tr>
                                            <tr v-if="join.trip_request.comment">
                                                <td colspan="30" class="">
                                                    <table class="text-muted no-padding">
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
import ConfirmDialogue from "./ConfirmDialogue.vue"
import { ref, defineProps, defineEmits, computed, onMounted } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import { getDatePart, getDate, getTime, cleanLocation, nameEmail, formatError } from '../components/common.js'
import { toRefs } from 'vue'

const emit = defineEmits(['refreshTrips']);
const props = defineProps(['trips', 'userID']);
const { trips, userID } = toRefs(props);
const confirmDialogue = ref(null);
const sortedTrips = computed(() => {
    return [...trips.value].sort((a, b) => {
        return new Date(a.earliest_departure_time) - new Date(b.earliest_departure_time);
    });
});

function toggleTripIsFull(tripID) {
    trips.is_full = !trips.is_full
    const endpoint = `${endpoints["trip"]}${tripID}/`;
    try {
        axios.patch(endpoint, null, {
            params: {
                action: 'toggleIsFullSetting'
            }
        });
        emit('refreshTrips');
    } catch (error) {
        confirmDialogue.value.show({
            title: "Error",
            message: "Error marking trip as full:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
            cancelButton: "Close",
            okClass: "btn btn-danger",
        });
        return;
    }
}

function hasUpdate(tripID) {
    const endpoint = `${endpoints["trip"]}${tripID}/`;

}

function checkUpdate(tripID) {
    /*const endpoint = `${endpoints["trip"]}${tripID}/`;
    try {
        axios.patch(endpoint, null, {
            params: {
                action: 'removeUser'
            }
        });
        emit('refreshTrips');
    } 
    catch (error) {
    }*/
    return;
}

function acceptJoinRequest(joinID) {
    const endpoint = `${endpoints["joinRequests"]}${joinID}/?action=accept`;
    // console.log(endpoint)
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

async function leaveTrip(tripID) {
    const confirm = await confirmDialogue.value.show({
        title: "Confirm",
        message: "Are you sure you want to leave this trip?",
        cancelButton: "Cancel",
        okButton: "Leave",
        okClass: "btn btn-danger",
    });
    if (confirm) {
        const endpoint = `${endpoints["trip"]}${tripID}/`;
        try {
            // TODO: How do these parameters compare to the ones directly in the endpoint URL?
            axios.patch(endpoint, null, {
                params: {
                    action: 'removeUser'
                }
            });
            emit('refreshTrips');
        } catch (error) {
            confirmDialogue.value.show({
                title: "Error",
                message: "Error leaving trip:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
                cancelButton: "Close",
                okClass: "btn btn-danger",
            });
            return;
        }
    }
}

function showTooltip(id) {
    var tooltip = document.getElementById(id);
    tooltip.style.opacity = 1

    setTimeout(function () {
        tooltip.style.opacity = 0
    }, 1000)
}

function copyEmailsOf(participants, id) {
    const emails = participants.map(p => p.email).join(",")
    navigator.clipboard.writeText(emails)
    // console.log("copyTooltip" + id)
    showTooltip("copyTooltip" + id)
}

</script>

<style>
.dot {
    height: 10px;
    width: 10px;
    background-color: blue;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
}

.header-border {
    border-right: 1px;
    border-bottom: 1px;
}

.margin-right-1 {
    margin-right: 50px;
}
.margin-right-2 {
    margin-right: 10px;
}

.btn-text {
    border-radius: 6px;
    border: none;
    margin: 0;
    /* padding: 0px 1px 0px 1px; */
    cursor: pointer;
    white-space: nowrap;
    /* box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.2); */

}

.btn-text:hover {
    transform: translateY(-1px);
}

.btn-text:active {
    transform: translateY(0);
}



.accept {
    background-color: rgb(153, 227, 153);
}

.accept:hover {
    background-color: rgb(136, 200, 136);
}

.reject {
    background-color: rgb(236, 150, 150);
}

.reject:hover {
    background-color: rgb(212, 135, 135);
}

.copy-emails-btn {
    padding: 1px;
    width: 100px;
    /* align with left of screen */
    display: flex;
    justify-content: center;
}

.tooltip {
    position: relative;
    --bs-tooltip-zindex: 0;
    /* display: inline-block; */
    opacity: 1;
    width: 100px;
}

.tooltip .tooltiptext {
    width: 140px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    /* z-index: 1; */
    opacity: 0;
    transition: opacity 0.3s;

    /* Position the tooltip above the .copy-emails-btn */
    /* margin-left: -150px;
    margin-top: -80px; */
    /* left: 100%;
    top: -6px */
    bottom: 150%;
    left: 50%;
    margin-left: -72px;
}

.tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #555 transparent transparent transparent;
}

/* .tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
} */
.flex {
    display: flex;
    gap: 20px;
    justify-content: center;
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

.no-padding {
    padding: none;
    height: 0;
}
</style>
