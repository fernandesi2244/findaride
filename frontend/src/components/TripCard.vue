<template>
    <h2 class="accordion-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            :data-bs-target="'#' + trip.college + trip.id">
            <span class="nickname-card">
                {{ trip.trip_nickname }}
            </span>
            <span class="status">
                {{ numRidersText }}
            </span>
        </button>
    </h2>
    <div :id="trip.college + trip.id" class="accordion-collapse collapse">
        <div class="accordion-body">
            <div class='mb-2'>
                <div class="row">
                    <div class="col-8 text-start">
                        <h5 :title="`${trip.departure_location} -> ${trip.arrival_location}`"> {{ cleanLocation(trip.departure_location) }} &#8594; {{ cleanLocation(trip.arrival_location) }}
                        </h5>
                        <p class="text-muted" style="font-size: 14px;">
                            <span class="me-4">
                                {{ getDateOrRange(trip.earliest_departure_time, trip.latest_departure_time) }}
                            </span>

                            {{ getTimeRange(trip.earliest_departure_time, trip.latest_departure_time) }}
                            <sup>
                                {{ getDateDiff(trip.earliest_departure_time, trip.latest_departure_time) }}
                            </sup>
                        </p>
                    </div>
                    <div class="col-4">
                        <button class="float-end btn btn-danger btn-sm" style="max-width: 80px;"
                            @click="emit('leaveTrip', trip.id)">Leave</button>
                    </div>
                </div>
                <div class="row mt-2 mb-5">
                    <div class="col-3 text-start">Luggage bags: <span>{{ trip.num_luggage_bags }}</span></div>
                    <div class="col-4 text-start">
                        <div class="flex mark-trip-div">
                            <label class="form-check-label me-2">
                                Mark trip as full
                            </label>
                            <div class="form-check form-switch">
                                <input @click="emit('toggleTripIsFull', trip.id)" v-model="trip.is_full"
                                    class="form-check-input" type="checkbox" role="switch" value="" :id="'check' + trip.id">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mt-5 pt-5">
                    <div class="col text-start">
                        <div class="flex" style="justify-content: start;">
                            <h5 class="text-start header-border">Members<br></h5>
                            <div class="tooltip">
                                <button class="btn-text copy-emails-btn"
                                    @click="copyEmailsOf(trip.participant_list.filter(participant => participant.id !== userID), trip.id)">
                                    Copy emails
                                </button>
                                <span class="tooltiptext" :id="'copyTooltip' + trip.id">Copied to
                                    clipboard</span>
                            </div>
                        </div>
                        <!-- put each member on a separate line -->
                        <!-- print all trip participants except current user -->
                        <p class="text-start text-muted" style="margin-bottom: 0.4em;">- You</p>
                        <p style="margin-bottom: 0.4em;"
                            v-for="participant in trip.participant_list.filter(participant => participant.id !== userID)"
                            :key="participant.id" class="text-start text-muted">
                            - {{ nameEmail(participant) }}
                        </p>
                    </div>
                    <div class="col ps-5" style="border-left: solid rgb(187, 187, 187) 1px;">
                        <h5 class="text-start">Join requests</h5>
                        <div v-if="trip.join_requests.length == 0">
                            <p class="text-start text-muted fst-italic">No requests to join yet.</p>
                        </div>
                        <div v-else class="table-responsive">
                            <table class="table bdr">
                                <thead>
                                    <tr>
                                        <th scope="col" class="column">Name</th>
                                        <th scope="col" class="column">Bags</th>
                                        <th scope="col" class="column"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template v-for="join in trip.join_requests" :key="join.id">
                                        <tr>
                                            <td v-bind:class="join.trip_request.comment ? 'no-border' : ''">{{
                                                join.trip_request.user.first_name }} {{
        join.trip_request.user.last_name }}</td>
                                            <td v-bind:class="join.trip_request.comment ? 'no-border' : ''">{{
                                                join.trip_request.num_luggage_bags }}</td>
                                            <td v-bind:class="join.trip_request.comment ? 'no-border' : ''">
                                                <div v-if="join.participants_that_accepted.includes(userID)">
                                                    <!-- check if there are other members of the trip that need to approve the reqeust -->
                                                    <div
                                                        v-if="join.participants_that_accepted.length < trip.num_participants">
                                                        Waiting for other members...
                                                    </div>
                                                    <div v-else>
                                                        They're in!
                                                    </div>
                                                </div>
                                                <div v-else>
                                                    <button class="btn-text accept" role="button"
                                                        style="width:60px; margin-right:5px"
                                                        @click="emit('acceptJoinRequest', join.id)">Accept</button>
                                                    <button class="btn-text reject" role="button" style="width:60px"
                                                        @click="emit('rejectJoinRequest', join.id)">Reject</button>
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
</template>

<script setup>
import { toRefs, defineProps, defineEmits, computed } from 'vue';
import { getDatePart, getDate, getTime, getDateOrRange, cleanLocation, nameEmail, getTimeRange, getDateDiff } from '../components/common.js'


const props = defineProps(['trip', 'userID'])
const { trip, userID } = toRefs(props)

const emit = defineEmits(['acceptJoinRequest', 'rejectJoinRequest', 'leaveTrip', 'toggleTripIsFull'])

const numRidersText = computed(() => {
    const numOthers = trip.value.participant_list.length - 1
    if (numOthers == 1) {
        return "You + 1 other"
    }
    return "You + " + String(numOthers) + " others"
})

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

.reject {
    background-color: rgb(236, 150, 150);
}

.copy-emails-btn {
    padding: 1px;
    width: 100px;
    /* align with left of screen */
    display: flex;
    justify-content: center;
    background-color: rgb(221, 221, 221);
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

button.btn.btn-danger {
    color: white;
}

.mark-trip-div {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 0.2em;
}
</style>