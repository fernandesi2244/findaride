<script>
import { toRef } from 'vue'
import SidebarLink from './SidebarLink.vue'
import { collapsed, toggleSidebar, sidebarWidth } from './state.js'
import { getDate, getDateTime, getTime, cleanLocation } from '../Center/common.js'

export default {
    props: ['trips', 'tripRequests'],
    emits: ['selectTrip', 'selectTripRequest', 'showTripForm'],
    methods: {
        clickTrip(id) {
            console.log('selected trip' + id)
            this.$emit('selectTrip', id)
        },
        clickTripRequest(id) {
            console.log('selected trip request ' + id)
            this.$emit('selectTripRequest', id)
        },
        clickAddTrip() {
            console.log('clicked form')
            this.$emit('showTripForm')
        }
    },
    components: { SidebarLink },

    setup(props) {
        const tripsArray = toRef(props, 'trips')
        const tripRequestsArray = toRef(props, 'tripRequests')

        return { 
            collapsed, toggleSidebar, sidebarWidth, 
            tripsArray, tripRequestsArray,
            getDate, getDateTime, getTime, cleanLocation 
        }
    }
}


</script>

<template>
    <div class="sidebar" :style="{ width: sidebarWidth }">
        <h1>
        <span v-if="collapsed">
            <div>V</div>
            <div>S</div>
        </span>
        
        <span class="text-size" v-else>
            <router-link to="/" style="text-decoration: none; color: inherit; cursor: pointer;">FindARide</router-link>
        </span>
        </h1>

        <!-- <SidebarLink to="/frontpage" icon="fas fa-home">Home</SidebarLink>
        <SidebarLink to="/dashboard" icon="fas fa-columns">Dashboard</SidebarLink>
        <SidebarLink to="/trips" icon="fas fa-chart-bar">Your Trips</SidebarLink>
        <SidebarLink to="/triprequest" icon="fas fa-users">Trip Requests</SidebarLink>
        <SidebarLink to="/confirmationrequest" icon="fas fa-image">Confirmation Requests</SidebarLink> -->
        
        <div class="section-header">
            <button @click="clickAddTrip" class="btn add-trip-btn">+ Create New Request</button>
        </div>

        <h4 class="left">Trips</h4>
        <div v-for="trip in tripsArray" :key="trip.id">
            <button @click="clickTrip(trip.id)">
                <div class="card">
                    <div><strong>From:</strong> {{ cleanLocation(trip.departure_location) }}</div>
                    <div><strong>To:</strong> {{ cleanLocation(trip.arrival_location) }}</div>
                    <div><strong>Departure Date:</strong> {{ getDate(trip.departure_time) }}</div>
                    <div><strong>Departure Time:</strong> {{ getTime(trip.departure_time) }}</div>
                    <div><strong>Luggage Count:</strong> {{ trip.num_luggage_bags }}</div>
                </div>
            </button>
        </div>

        <h4 class="left">Requests</h4>
        <div v-for="tripReq in tripRequestsArray" :key="tripReq.id">
            <button @click="clickTripRequest(tripReq.id)">
                <div class="card">
                    <div><strong>From:</strong> {{ cleanLocation(tripReq.departure_location) }}</div>
                    <div><strong>To:</strong> {{ cleanLocation(tripReq.arrival_location) }}</div>
                    <div><strong>Departure Date:</strong> {{ getDate(tripReq.earliest_departure_time) }}</div>
                    <div><strong>Departure Time:</strong>{{ getTime(tripReq.earliest_departure_time) }} &#8594; {{ getTime(tripReq.latest_departure_time) }}</div>
                    <div><strong>Luggage Count:</strong> {{ tripReq.num_luggage_bags }}</div>
                </div>
            </button>
        </div>

        <span
        class="collapse-icon"
        :class="{ 'rotate-180': collapsed }"
        @click="toggleSidebar"
        >
        <i class="fas fa-angle-double-left" />
        </span>
    </div>
</template>

<style>
:root {
  --sidebar-bg-color: #2f855a;
  --sidebar-item-hover: #38a169;
  --sidebar-item-active: #276749;
}
</style>

<style scoped>
.sidebar {
  
  color: white;
  background-color: var(--sidebar-bg-color);

  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}
.left {
    text-align: left;
}
.text-size {
  font-size:30px;
}
.sidebar h1 {
  height: 2.5em;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 0.75em;

  color: rgba(255, 255, 255, 0.7);

  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}

.add-trip-btn {
    background-color: #008CBA;
    color: #fff;
}
</style>