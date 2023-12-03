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
                            <div class="flex">
                                <h5 class="text-start margin-right header-border">Members<br></h5>
                                <div class="text-start">Luggage bags: <span>{{ trip.num_luggage_bags }}</span></div>
                                <div class="tooltip">
                                    <button type="button" 
                                            class="btn-text"
                                            @click="copyEmailsOf(trip.participant_list, trip.id)">Copy emails</button>
                                    <span class="tooltiptext" :id="'copyTooltip' + trip.id">Copied to clipboard</span>
                                </div>
                            </div>
                            <!-- put each member on a separate line -->
                            <h6 v-for="participant in trip.participant_list" class="text-start">
                                {{ nameEmail(participant) }}
                            </h6>
                        </div>
                        <div class="hug-right">
                            <button class="btn btn-danger" @click="leaveTrip(trip.id)">Leave</button>
                        </div>
                    </div>
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
                                        <div class="flex" v-else>
                                            <button class="btn-text accept" role="button" @click="acceptJoinRequest(join.id)">Accept</button>
                                            <button class="btn-text reject" role="button" @click="rejectJoinRequest(join.id)">Reject</button>
                                        </div>
                                    </td>
                                    
                                </tr>
                                <tr v-if="join.trip_request.comment">
                                    <td colspan="30" class="no-border">
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
import {ref, defineProps, onMounted, reactive, computed } from 'vue';
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

function leaveTrip(tripID) {
    if (confirm('Are you sure you want to leave this trip?')) {
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
            alert(error);
            return;
        }
    }
}


function setTooltip(tooltip) {
  tooltip('hide')
    // .attr('data-original-title', message)
    .tooltip('show');
}

function hideTooltip(btn) {
  setTimeout(function() {
    btn.tooltip('hide');
  }, 1000);
}

function showTooltip(id) {
    var tooltip = document.getElementById(id);
    tooltip.style.opacity = 1
    
    setTimeout(function() {
        tooltip.style.opacity = 0
    }, 1000)
}

function copyEmailsOf(participants, id) {
    const emails = participants.map(p => p.email).join(",")
    navigator.clipboard.writeText(emails)
    console.log("copyTooltip" + id)
    showTooltip("copyTooltip" + id)
}

</script>

<style>
.header-border {
    border-right: 1px;
    border-bottom: 1px;
}

.margin-right {
    margin-right: 50px;
}

.btn-text {
    border:none;
    margin:0;
    padding: 0px 1px 0px 1px;
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

.button-39 {
  background-color: #FFFFFF;
  border: 1px solid rgb(209,213,219);
  /* border: 1px solid green; */

  border-radius: .5rem;
  box-sizing: border-box;
  color: #111827;
  font-family: "Inter var",ui-sans-serif,system-ui,-apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
  font-size: .875rem;
  font-weight: 600;
  line-height: 1.25rem;
  padding: .75rem 1rem;
  text-align: center;
  text-decoration: none #D1D5DB solid;
  text-decoration-thickness: auto;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button-39:hover {
  background-color: rgb(249,250,251);
}

.button-39:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

.button-39:focus-visible {
  box-shadow: none;
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

.tooltip {
    position: relative;
    display: inline-block;
    opacity: 1;
}

.tooltip .tooltiptext {
    /* visibility: hidden; */
    width: 140px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 150%;
    left: 50%;
    margin-left: -75px;
    opacity: 0;
    transition: opacity 0.3s;
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
</style>
