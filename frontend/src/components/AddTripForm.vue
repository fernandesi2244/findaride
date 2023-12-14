<template>
  <popup-modal ref="popup" medium>
    <div class="modal-content">
    <form @submit.prevent="submitNewTrip" class="create-trip-modal">
      <h5 class="nickname">
        <label class="label" for="nickname">Nickname:</label>
        <input class="input" id="nickname" v-model="trip.nickname" type="text" placeholder="e.g. Spring break departure"
          maxlength="255" required>
      </h5>

      <div class="luggage">
        <label class="text-start" for="luggage-count">Number of luggage bags:</label>
        <input id="luggage-count" v-model.number="trip.luggageCount" type="number" min="0" required />
      </div>

      <div>Create a trip by yourself and wait for others to join you.</div>
      <hr>

      <div>
        <div class="create-trip-row">
          <b> Pickup location:</b> <br>
          <div class="">{{ cleanLocation(trip.from) }}</div>
        </div>
        <div class="create-trip-row">
          <b> Dropoff location:</b><br>
          <div class="">{{ cleanLocation(trip.to) }}</div>
        </div>
        <div class="create-trip-row">
          <b> Earliest departure time:</b>
          <div class="">{{ getDate(trip.earliestDepartureTime) + ", " + getTime(trip.earliestDepartureTime) }}</div>
        </div>
        <div class="create-trip-row">
          <b> Latest departure time:</b>
          <div class="">{{ getDate(trip.latestDepartureTime) + ", " + getTime(trip.latestDepartureTime) }}</div>
        </div>
      </div>

      <div class="create-trip-footer">
        <button type="button" @click="closeCreateTripModal" class="btn btn-secondary">Close</button>
        <button type="submit" class="btn primary">Create trip</button>
      </div>
    </form>
    </div>
  </popup-modal>
  <div class="modal-content mb-3">
    <div class="modal-body">
      <form @submit.prevent="submitFirst" class="form-container">
        <div class="form-row mb-1">
          <div class="form-group">
            <label class="text-start" for="from">Pickup location:</label>
            <input class="form-control" :class="{ 'is-valid': fromLocationWasSelected }" @keydown="pickupLocationChanged()" id="from" ref="fromRef" v-model="trip.from" placeholder="Start typing to see results..." required />
          </div>
          <div class="form-group">
            <label class="text-start" for="to">Dropoff location:</label>
            <input class="form-control" :class="{ 'is-valid': toLocationWasSelected }" id="to" ref="toRef" @keydown="dropoffLocationChanged()" v-model="trip.to" placeholder="Start typing to see results..." required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="text-start" for="pickup-time">Earliest departure time:</label>
            <input class="form-control" :class="{ 'is-valid': trip.earliestDepartureTime != '' }" id="pickup-time" v-model="trip.earliestDepartureTime" type="datetime-local" required />
          </div>
          <div class="form-group">
            <label class="text-start" for="dropoff-time">Latest departure time:</label>
            <input class="form-control" :class="{ 'is-valid': trip.latestDepartureTime != '' }" id="dropoff-time" v-model="trip.latestDepartureTime" type="datetime-local" required />
          </div>
        </div>
        <div class="mb-1">
          Can't find a trip you like?
          <button id="add-trip-btn" class="btn-link">Create your own trip</button>
          that others can join.
        </div>
        
        <div v-if="showInvalidLocationModal" class="overlay"></div>
        <div v-if="showInvalidLocationModal" class="invalid-location-modal">
          <div class="modal-header">
            <h4 class="modal-title">Invalid Location</h4>
            <button @click="closeInvalidLocationModal" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <p>Please select a valid {{ invalidLocationType }} location from the suggestions.</p>
          </div>
          <div class="modal-footer">
            <button @click="closeInvalidLocationModal" class="btn primary">OK</button>
          </div>
        </div>

        <div v-if="showInvalidLocationModal" class="overlay"></div>
        <div v-if="showInvalidLocationModal" class="invalid-location-modal">
          <div class="modal-header">
            <h4 class="modal-title">Invalid Location</h4>
            <button @click="closeInvalidLocationModal" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <p>Please select a valid {{ invalidLocationType }} location from the suggestions.</p>
          </div>
          <div class="modal-footer">
            <button @click="closeInvalidLocationModal" class="btn primary">OK</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
  
<script>
import TripFormHelpModal from '../components/TripFormHelpModal.vue';
import PopupModal from './PopupModal.vue';
import { getTime, getDate, cleanLocation } from './common.js';

export default {
  name: "AddTripModal",
  components: {
    TripFormHelpModal, PopupModal
  },
  emits: ['getFilteredTrips', 'createTrip', 'refreshTrips', 'getTrips'],
  data() {
    return {
      showCreateTripModal: false,
      showInvalidLocationModal: false,
      invalidLocationType: '',
      fromLocationWasSelected: false,
      toLocationWasSelected: false,
      trip: {
        from: '',
        to: '',
        fromLat: '',
        fromLong: '',
        toLat: '',
        toLong: '',
        departureDate: '',
        earliestDepartureTime: '',
        latestDepartureTime: '',
        luggageCount: 0,
        nickname: '',
        comment: '',
      },
    }
  },
  computed: {
    noFieldsFilled() {
        return !this.trip.from && !this.trip.to && !this.trip.earliestDepartureTime && !this.trip.latestDepartureTime && this.trip.luggageCount == 0;
    },
    allFieldsFilled() {
      return this.trip.from && this.trip.to && this.trip.earliestDepartureTime && this.trip.latestDepartureTime && this.trip.luggageCount > 0;
    },
  },
  watch: {
    'trip.from': 'checkAndCreateTripRequest',
    'trip.to': 'checkAndCreateTripRequest',
    'trip.earliestDepartureTime': 'checkAndCreateTripRequest',
    'trip.latestDepartureTime': 'checkAndCreateTripRequest',
  },
  mounted() {
    this.initializeAutocomplete();
  },
  methods: {
    getTime, getDate, cleanLocation,
    checkAndCreateTripRequest() {
        if(!this.toLocationWasSelected) {
            this.trip.toLat = '';
            this.trip.toLong = ''
        }
        if(!this.fromLocationWasSelected) {
            this.trip.fromLat = '';
            this.trip.fromLong = '';
        }
        if(this.noFieldsFilled) {
            this.$emit('getFilteredTrips', {})
        } else {
            this.$emit('getFilteredTrips', { ...this.trip })
        }
    },
    initializeAutocomplete() {
      const acFrom = new google.maps.places.Autocomplete(this.$refs.fromRef, {
        types: ["transit_station"],
        fields: ["geometry"]
      });

      const acTo = new google.maps.places.Autocomplete(this.$refs.toRef, {
        types: ["transit_station"],
        fields: ["geometry"]
      });

      acFrom.addListener("place_changed", () => {
        let place = acFrom.getPlace().geometry.location;
        this.trip.fromLat = place.lat();
        this.trip.fromLong = place.lng();
        this.trip.from = this.$refs.fromRef.value;
        this.$emit('getTrips', { ...this.trip });
        this.fromLocationWasSelected = true;
      });

      acTo.addListener("place_changed", () => {
        let place = acTo.getPlace().geometry.location;
        this.trip.toLat = place.lat();
        this.trip.toLong = place.lng();
        this.trip.to = this.$refs.toRef.value;
        this.$emit('getTrips', { ...this.trip });
        this.toLocationWasSelected = true;
      });
    },
    toggleHelp() {
      console.log(this.$refs.tripFormHelpModal)
      this.$refs.tripFormHelpModal.show();
    },
    resetForm() {
      this.trip.from = '';
      this.trip.fromLat = '';
      this.trip.fromLong = '';
      this.trip.to = '';
      this.trip.toLat = '';
      this.trip.toLong = '';
      this.trip.departureDate = '';
      this.trip.earliestDepartureTime = '';
      this.trip.latestDepartureTime = '';
      this.trip.luggageCount = 0;
      this.trip.comment = '';
      this.trip.nickname = '';

      this.fromLocationWasSelected = false;
      this.toLocationWasSelected = false
    },
    showInvalidLocationAlert(locationType) {
      this.invalidLocationType = locationType;
      this.showInvalidLocationModal = true;
    },

    pickupLocationChanged() {
      this.fromLocationWasSelected = false;
    },
    dropoffLocationChanged() {
      this.toLocationWasSelected = false;
    },

    closeInvalidLocationModal() {
      this.showInvalidLocationModal = false;
    },
    closeCreateTripModal() {
      this.$refs.popup.close()
    },
    submitFirst() {
      if (!this.fromLocationWasSelected) {
        this.showInvalidLocationAlert('pickup');
        return;
      }
      if (!this.toLocationWasSelected) {
        this.showInvalidLocationAlert('dropoff');
        return;
      }
      this.$refs.popup.open()
      this.toggleCreateTripModal()
    },
    async submitNewTrip() {
      // if(!validateFormData(tripData)) return;
      console.log("Submitting trip:", { ...this.trip });
      this.$emit('createTrip', { ...this.trip });
      this.$emit('refreshTrips');
      this.resetForm();
      this.$refs.popup.close()
    },
    autoSearchForTrips() {
      this.$emit('getTrips', { ...this.trip });
    },
    toggleCreateTripModal() {
      this.showCreateTripModal = !this.showCreateTripModal
    }
  }
}
</script>
<style>
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --input-border-color: #ccc;
  --hover-opacity: 0.9;
}

.btn-link {
  background: none !important;
  border: none;
  padding: 0 !important;
  /*optional*/
  font-family: arial, sans-serif;
  /*input has OS specific font-family*/
  color: rgb(13, 110, 253);
  text-decoration: underline;
  cursor: pointer;
}

.create-trip-footer {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  margin-top: 10px;
  gap: 10px
}

.create-trip-row {
  display: flex;
  gap: 5px;
}


.luggage {
  flex: 2;
}

.luggage label {
  font-weight: bold;
  width: 200px;
  margin-bottom: 10px;
}

.luggage input {
  width: 55px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.nickname {
  white-space: nowrap;
}

.nickname label {
  float: left;
  margin-right: 10px;
  width: 100px;
  padding: 5px 5px 5px 0px;
  font-weight: bold;
}

.nickname input {
  width: calc(100% - 110px);
  padding: 5px;
  background-color: rgba(0, 0, 0, 0.05);
}

.trip-request-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #0e0b0b;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* left-align all elements */
  text-align: left;
}


.trip-request-form h3 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

/* Style for form groups */
.form-group {
  flex: 1;
  margin-right: 10px;
}

.form-row {
  display: flex;
  justify-content: space-between;
  /* margin-bottom: 15px; */
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}


.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}


.form-group textarea {
  height: 100px;
  resize: vertical;
}


/* Style for buttons */
.form-actions {
  display: flex;
  justify-content: center;
  padding-top: 10px;
}


.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}


.btn.primary {
  background-color: #007bff;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}


/* Additional styles for responsiveness and interactivity */
@media (max-width: 768px) {
  .trip-request-form {
    padding: 10px;
  }
}


input:focus,
textarea:focus {
  border-color: #007bff;
  outline: none;
}

.btn {
  border-radius: 30px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.create-trip-modal {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: 80%;
  max-width: 500px;
  text-align: left;
}

.create-trip-modal .modal-header {
  /* margin-bottom: 10px; */
}

.invalid-location-modal {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: 80%;
  max-width: 400px;
}

.invalid-location-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.invalid-location-modal .modal-header .close-btn {
  border: none;
  background: none;
  font-size: 1.5em;
  cursor: pointer;
}

.invalid-location-modal .modal-body p {
  color: #333;
}

.invalid-location-modal .modal-footer {
  text-align: right;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
</style>