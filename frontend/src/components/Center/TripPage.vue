<template>
    <div class="fill">
        <!-- <div class="main-content" :style="{ 'margin-left': sidebarWidth }"> -->
        <div class="bdr">
            <div class="tripinfo">
                <div class="triptitle">
                    <div class="left">
                        <span><h2>{{ props.trip.departure_location }}  &#8594; {{ props.trip.arrival_location }}</h2> </span>
                        <h5>{{ props.trip.departure_time }} &mdash; {{ props.trip.departure_time }}</h5>
                        Luggage: {{ props.trip.num_luggage_bags }}
                    </div>
                    <div>
                        <button>Edit</button>
                        <button>Leave</button>
                    </div> 
                </div>
            </div>
        </div>
 
            <!-- <div class="trip-info">
                <div><strong>To:</strong> {{ props.to }}</div>
                <div><strong>Departure Time:</strong> {{ props.departureTime }}</div>
                <div><strong>Luggage Count:</strong> {{ props.luggageCount }}</div>
                <div><strong>Comments:</strong> {{ props.comments }}</div>
            </div> -->

        <div class="triptitle margin">
            <h4>Group members</h4>
        </div>

        <div class="table-responsive">
            <table class="table bdr">
                <thead>
                    <tr>
                        <th scope="col" class="column">Name</th>
                        <th scope="col" class="column">Min Time</th>
                        <th scope="col" class="column">Max Time</th>
                        <th scope="col" class="column">Departure</th>
                        <th scope="col" class="column">Arrival</th>
                        <th scope="col" class="column">Luggage</th>
                        <!-- <th scope="col" class="column">Email</th>
                        <th scope="col" class="column">Phone Number</th> -->
                        <th scope="col" class="columnend"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="participant in props.trip.participant_list" :key="participant.id">
                    <td>{{ participant.first_name }} {{ participant.last_name }}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <!-- <td>{{ participant.email }}</td>
                    <td>{{ participant.phone }}</td> -->
                    <td></td>
                </tr>
                </tbody>
            </table>
        </div>

        <div class="left">
            <h4>Join requests</h4>
        </div>

        <div class="table-responsive">
            <table class="table bdr">
                <thead>
                    <tr>
                        <th scope="col" class="column">Name</th>
                        <th scope="col" class="column">Min Time</th>
                        <th scope="col" class="column">Max Time</th>
                        <th scope="col" class="column">Departure</th>
                        <th scope="col" class="column">Arrival</th>
                        <th scope="col" class="column">Luggage</th>
                        <!-- <th scope="col" class="column">Email</th>
                        <th scope="col" class="column">Phone Number</th> -->
                        <th scope="col" class="columnend"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="join in props.trip.join_requests" :key="join.id">
                    <td>{{ join.trip_request.user.first_name }} {{ join.trip_request.user.last_name }}</td>
                    <td>{{ join.trip_request.earliest_departure_time }}</td>
                    <td>{{ join.trip_request.latest_departure_time }}</td>
                    <td>{{ join.trip_request.departure_location }}</td>
                    <td>{{ join.trip_request.arrival_location }}</td>
                    <td>{{ join.num_luggage_bags }}</td>
                    <!-- <td>{{ participant.email }}</td>
                    <td>{{ participant.phone }}</td> -->
                    <td>
                        <button @click="acceptJoinRequest(join.id)">Accept</button>
                        <button @click="rejectJoinRequest(join.id)">Reject</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>

        <div class="left">
            <h4>Confirmation requests</h4>
        </div>

        <div class="table-responsive">
            <table class="table table-responsive bdr">
                <thead>
                    <tr>
                        <th scope="col" class="column">Name</th>
                        <th scope="col" class="column">Min Time</th>
                        <th scope="col" class="column">Max Time</th>
                        <th scope="col" class="column">Departure</th>
                        <th scope="col" class="column">Arrival</th>
                        <th scope="col" class="column">Luggage</th>
                        <!-- <th scope="col" class="column">Email</th>
                        <th scope="col" class="column">Phone Number</th> -->
                        <th scope="col" class="column">Status</th>
                        <!-- <th scope="col" class="columnend"></th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="confirmation in props.trip.confirmationRequests" :key="confirmation.id">
                    <td>{{ confirmation.name }}</td>
                    <td>{{ confirmation.minTime }}</td>
                    <td>{{ confirmation.maxTime }}</td>
                    <td>{{ confirmation.departure }}</td>
                    <td>{{ confirmation.arrival }}</td>
                    <td>{{ confirmation.luggage }}</td>
                    <td>
                        {{ confirmation.status }}
                        <button v-if="confirmation.status === 'Sent'">Cancel</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div> 
    <!-- </div> -->
</template>
<script setup>

  import { defineProps, onMounted, reactive } from 'vue';
  import { endpoints } from '../../common/endpoints.js';
    const props = defineProps(['trip'])

    // const from = "Princeton"
    // const to = "EWR"
    // const minTime = "Oct.13, 10:00am"
    // const maxTime = "Oct.13, 11:00pm"
    // const luggage = 3

    // const participants = reactive([])
    // const joinRequests = reactive([])
    // const confirmationRequests = reactive([])

    // const participants = reactive([
    //     {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    //     {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    // ])

    // const joinRequests = reactive([
    //     {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    //     {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    // ])

    // const confirmationRequests = reactive([
    //     {id: 0, status: "Sent", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
    //     {id: 1, status: "Rejected", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    // ])

    onMounted(()=> {
        // participants.value = props.trip.participants
        // joinRequests.value = props.trip.joinRequests

    });

    function acceptJoinRequest(reqid) {
        const endpoint = `${endpoints["joinRequest"]}${reqid}/accept/`;
        try {
          axios.delete(endpoint);
        //   getUserTrips();
        //   getConfirmationRequests();
        } catch (error) {
          alert(formatError(error.response.data.error));
          return;
        }
    }

    function rejectJoinRequest(reqid) {
        const endpoint = `${endpoints["joinRequest"]}${reqid}/reject/`;
        try {
            axios.delete(endpoint);
            // getUserTrips();
            // getConfirmationRequests();
        } catch (error) {
            alert(formatError(error.response.data.error));
            return;
        }
    }

</script>


<style scoped>
.app-container {
  display: flex;
}

.main-content {
  width: 100%;
}
.bdr {
    border-radius: 10px;
    overflow: hidden;
}

.margin {
    margin-top: 8px;
    margin-bottom: 5px;
}

.fill {
    /* height: 100vh;
    box-sizing: border-box; */
    /* position:absolue (or fixed);
    width:100%;
    height:100%;
    top: 0;
    left: 0; */
    /* display: table-cell; */
    align-items: stretch;
}

.column {
    width: 15%
}

.columnend {
    width: 10%;
    margin: 0%;
    padding: 0%;
}

.left {
    text-align: left;
}

.tripinfo {
    width: 100%;
    background-color: white;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 10px;
    outline-offset: 10px;
    /* margin-bottom: 10px; */
    border-radius: 4px;
}

.triptitle {
    display: flex;
    justify-content: space-between;

    /* width: 100px; */
    /* display: inline-block; */
}


textarea {
  resize: vertical;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background: #e74c3c;
  color: #fff;
}

.btn:not(.cancel-btn) {
  background: #2ecc71;
  color: #fff;
}

.btn:not(.cancel-btn):hover {
  background: #27ae60;
}
</style>