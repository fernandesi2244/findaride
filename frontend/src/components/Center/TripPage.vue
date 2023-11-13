<template>
    
        <div class="fill">
            <Sidebar />
        <div :style="{ 'margin-left': sidebarWidth }">
            <router-view />
        </div>
        <div class="main-content" :style="{ 'margin-left': sidebarWidth }">
        <div class="bdr">
            <div class="tripinfo">
                <div class="triptitle">
                    <div class="left">
                        <span><h2>{{ from }}  &#8594; {{ to }}</h2> </span>
                        <h5>{{ minTime }} &mdash; {{ maxTime }}</h5>
                    </div>
                    <div>
                        <button>Edit</button>
                        <button>Delete</button>
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
            <button>Leave</button>
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
                    <tr v-for="participant in participants" :key="participant.id">
                    <td>{{ participant.name }}</td>
                    <td>{{ participant.minTime }}</td>
                    <td>{{ participant.maxTime }}</td>
                    <td>{{ participant.departure }}</td>
                    <td>{{ participant.arrival }}</td>
                    <td>{{ participant.luggage }}</td>
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
                    <tr v-for="join in joinRequests" :key="join.id">
                    <td>{{ join.name }}</td>
                    <td>{{ join.minTime }}</td>
                    <td>{{ join.maxTime }}</td>
                    <td>{{ join.departure }}</td>
                    <td>{{ join.arrival }}</td>
                    <td>{{ join.luggage }}</td>
                    <!-- <td>{{ participant.email }}</td>
                    <td>{{ participant.phone }}</td> -->
                    <td>
                        <button @click="acceptJoinRequest(req.id)">Accept</button>
                        <button @click="rejectJoinRequest(req.id)">Reject</button>
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
                    <tr v-for="confirmation in confirmationRequests" :key="confirmation.id">
                    <td>{{ confirmation.name }}</td>
                    <td>{{ confirmation.minTime }}</td>
                    <td>{{ confirmation.maxTime }}</td>
                    <td>{{ confirmation.departure }}</td>
                    <td>{{ confirmation.arrival }}</td>
                    <td>{{ confirmation.luggage }}</td>
                    <td>
                        {{ confirmation.status }}
                        <button>Cancel</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div> </div>
</template>
<script setup>

  import { defineProps, onMounted, reactive } from 'vue';
  import Sidebar from './../Sidebar/Sidebar.vue'
  import { sidebarWidth } from './../Sidebar/state.js'
    const props = defineProps({
        tripid: Number
    })

    const from = "Princeton"
    const to = "EWR"
    const minTime = "Oct.13, 10:00am"
    const maxTime = "Oct.13, 11:00pm"

    const participants = reactive([
        {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    const joinRequests = reactive([
        {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    const confirmationRequests = reactive([
        {id: 0, status: "Pending", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, status: "Rejected", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    onMounted(()=> {
        // participants.values = props.participants
        participants.values = fetchTrip(props.id)
    });

    function fetchTrip(id) {

    }


    function acceptJoinRequest(reqid) {
        print(props.tripid, reqid);
    }

    function rejectJoinRequest(reqid) {
        print(props.tripid, reqid);
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