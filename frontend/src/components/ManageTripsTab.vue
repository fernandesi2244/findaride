<template>
    <ConfirmDialogue ref="confirmDialogue" cancel-color="red"></ConfirmDialogue>
    <div v-if="trips.length == 0 && tripRequests.length == 0">
        <h4 class="my-8">No trips yet.</h4>
    </div>

    <div v-else>
        <div class="accordion" id="accordion">
            <div v-for="trip in sortedTrips" :key="trip.type + trip.id" class="accordion-item">
                <div v-if="trip.type === 't'">
                    <TripCard :trip="trip" :userID="userID" @acceptJoinRequest="acceptJoinRequest"
                        @rejectJoinRequest="rejectJoinRequest" @leaveTrip="leaveTrip" @toggleTripIsFull="toggleTripIsFull">
                    </TripCard>
                </div>
                <div v-else>
                    <TripRequestCard :tripRequest="trip" @withdrawJoinRequest="rejectJoinRequest"
                        @removeTripRequest="removeTripRequest"></TripRequestCard>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import ConfirmDialogue from "./ConfirmDialogue.vue"
import TripCard from "./TripCard.vue"
import TripRequestCard from "./TripRequestCard.vue"
import { ref, defineProps, defineEmits, computed, onMounted, toRefs } from 'vue';
import { endpoints } from '../common/endpoints.js';
import { axios } from '../common/axios_service.js'
import { formatError } from '../components/common.js'

const emit = defineEmits(['refreshTrips']);
const props = defineProps(['trips', 'tripRequests', 'userID']);
const { trips, tripRequests, userID } = toRefs(props);
const confirmDialogue = ref(null);
const sortedTrips = computed(() => {
    const myTrips = trips.value.map(obj => ({ ...obj, type: 't' }))
    const myRequests = tripRequests.value.map(obj => ({ ...obj, type: 'r' }))
    let allTrips = myTrips.concat(myRequests);
    return allTrips.sort((a, b) => {
        // sort by nickname string if comparing pending trips with possibly many trip requests
        if (a.type === 'r' && b.type === 'r') {
            return a.trip_nickname.localeCompare(b.trip_nickname)
        } else if (a.type === 't' && b.type === 't') {
            return new Date(a.earliest_departure_time) - new Date(b.earliest_departure_time)
        } else if (a.type === 'r' && b.type === 't') {
            return 1;
        } else {
            return -1;
        }
    });
});

function toggleTripIsFull(tripID) {
    const endpoint = `${endpoints["trip"]}${tripID}/`;
    try {
        axios.patch(endpoint, null, {
            params: {
                action: 'toggleIsFullSetting'
            }
        });
        // note that we don't refresh trips because the patch might not have finished
    } catch (error) {
        alert(error);
        emit('refreshTrips', null, true);
        return;
    }
}

async function acceptJoinRequest(joinID) {
    const endpoint = `${endpoints["joinRequests"]}${joinID}/?action=accept`;
    try {
        await axios.post(endpoint);
        emit('refreshTrips', null, true);
    } catch (error) {
        alert(error);
        return;
    }
}

async function rejectJoinRequest(joinID) {
    const confirm = await confirmDialogue.value.show({
        title: "Confirm",
        message: "Are you sure you want to withdraw this request?",
        cancelButton: "Cancel",
        okButton: "Confirm",
        okClass: "btn btn-danger",
    });

    if (confirm) {
        const endpoint = `${endpoints["joinRequests"]}${joinID}/?action=reject`;
        try {
            await axios.post(endpoint);
            emit('refreshTrips', null, true);
        } catch (error) {
            alert(error);
            return;
        }
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
            emit('refreshTrips', tripID, true);
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

async function removeTripRequest(tripRequestID) {
    const confirm = await confirmDialogue.value.show({
        title: "Confirm",
        message: "Are you sure you want to remove this trip?",
        cancelButton: "Cancel",
        okButton: "Remove",
        okClass: "btn btn-danger",
    });
    if (confirm) {
        const endpoint = `${endpoints["deleteTripRequest"]}${tripRequestID}/`;
        try {
            await axios.delete(endpoint);
            emit('refreshTrips', null, true);
        } catch (error) {
            confirmDialogue.value.show({
                title: "Error",
                message: "Error removing trip:\n" + (error.response.data.error !== undefined ? formatError(error.response.data.error) : error.response.statusText),
                cancelButton: "Close",
                okClass: "btn btn-danger",
            });
            return;
        }
    }
}

</script>