<template>
    <div class="fill">
        <div class="bdr">
            <div class="tripinfo">
                <div class="triptitle">
                    <div class="left">
                        <span><h2>{{ props.tripRequest.departure_location }}  &#8594; {{ props.tripRequest.arrival_location }}</h2> </span>
                        <h5>{{ props.tripRequest.earliest_departure_time }} &mdash; {{ props.tripRequest.latest_departure_time }}</h5>
                        Luggage: {{ props.tripRequest.num_luggage_bags }}
                    </div>
                    <div>
                        <button>Edit</button>
                        <button>Delete</button>
                    </div> 
                </div>
            </div>
        </div>

        <div class="left">
            <h4>Join requests</h4>
            <div>{{ props.tripRequest.join_requests.length }}</div>
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
                        <th scope="col" class="columnend"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="join in props.tripRequest.join_requests" :key="join.id" :id="join.id">
                    <td></td>
                    <td>{{ join.trip.earliest_departure_time }}</td>
                    <td></td>
                    <td>{{ join.trip.departure_location }}</td>
                    <td>{{ join.trip.arrival_location }}</td>
                    <td>{{ join.trip.num_luggage_bags }}</td>
                    <td>
                        <button @click="acceptJoinRequest(req.id)">Accept</button>
                        <button @click="rejectJoinRequest(req.id)">Deny</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>

        <div class="left">
            <h4>Matching Trips</h4>
        </div>

        <div class="table-responsive">
            <table class="table table-responsive bdr">
                <thead>
                    <tr>
                        <th scope="col" class="column">Group size</th>
                        <th scope="col" class="column">Min Time</th>
                        <th scope="col" class="column">Max Time</th>
                        <th scope="col" class="column">Departure</th>
                        <th scope="col" class="column">Arrival</th>
                        <th scope="col" class="column">Luggage</th>
                        <th scope="col" class="column">Status</th>
                        <!-- <th scope="col" class="columnend"></th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="match in matches" :key="match.id">
                    <td>{{ match.name }}</td>
                    <td>{{ match.minTime }}</td>
                    <td>{{ match.maxTime }}</td>
                    <td>{{ match.departure }}</td>
                    <td>{{ match.arrival }}</td>
                    <td>{{ match.luggage }}</td>
                    <td>
                        <button v-if="match.status === 'None'">Request</button>
                        <div v-else>{{ match.status }}</div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script setup>
  import { defineProps, onMounted, reactive } from 'vue';
  import { getTime, getDate, getDateTime, cleanLocation } from './common.js'

  const props = defineProps(['tripRequest'])

  /*
    const from = "Princeton"
    const to = "EWR"
    const minTime = "Oct.13, 10:00am"
    const maxTime = "Oct.13, 11:00pm"
    const luggage = 3

    
    const participants = reactive([
        {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    const joinRequests = reactive([
        {id: 0, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    const matches = reactive([
        {id: 0, status: "Pending", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Friend Center", arrival: "EWR", name: "a", email:"a@princeton.edu", phone:"666-666-6666", luggage: 1},
        {id: 1, status: "Denied", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2},
        {id: 1, status: "None", minTime: "Oct. 13, 10:00am", maxTime: "Oct. 13, 1:00pm", departure: "Admissions Center", arrival: "EWR", name: "b", email:"bbbbb@princeton.edu", phone:"666-666-6667", luggage: 2}
    ])

    */
    onMounted(()=> {
        // participants.values = props.participants
        //participants.values = fetchTrip(props.id)
    });

    function fetchTrip() {
        props.tripid
    }

    function editTripRequest() {

    }


    function acceptJoinRequest(reqid) {
        print(props.tripid, reqid);
    }

    function rejectJoinRequest(reqid) {
        print(props.tripid, reqid);
    }
</script>


<style scoped>

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