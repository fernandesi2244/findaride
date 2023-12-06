<template>
  <popup-modal ref="popup" medium>
    <TripFormHelpModal ref="tripFormHelpModal"></TripFormHelpModal>
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title">New trip</h4>
        <button @click="toggleHelp" class="btn btn-primary" style="background-color: #95a1ac; border-radius: 50%; font-size:small;">?</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submit" class="form-container">
          <div class="form-group">
            <label class="text-start" for="from">Pickup location:</label>
            <input id="from" ref="fromRef" v-model="trip.from" placeholder="Start typing to see results..." required />
          </div>
          <div class="form-group">
            <label class="text-start" for="to">Dropoff location:</label>
            <input id="to" ref="toRef" v-model="trip.to" placeholder="Start typing to see results..." required />
          </div>
          <div class="form-group">
            <label class="text-start" for="pickup-time">Earliest departure time:</label>
            <input id="pickup-time" v-model="trip.earliestDepartureTime" type="datetime-local" required />
          </div>
          <div class="form-group">
            <label class="text-start" for="dropoff-time">Latest departure time:</label>
            <input id="dropoff-time" v-model="trip.latestDepartureTime" type="datetime-local" required />
          </div>
          <div class="form-group">
            <label class="text-start" for="luggage-count">Number of luggage bags:</label>
            <input id="luggage-count" v-model.number="trip.luggageCount" type="number" min="0" required />
          </div>
          <div class="form-group">
            <label class="text-start" for="comments">Additional comments:</label>
            <textarea id="comments" v-model="trip.comment" placeholder="Any special accommodations, considerations, etc."
              maxlength="255"></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn primary">Create trip request</button>
            <button type="button" @click="_close" class="btn cancel-btn">Close</button>
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
  </popup-modal>
</template>

<script>
import TripFormHelpModal from '../components/TripFormHelpModal.vue';
import PopupModal from "./PopupModal.vue";

let fromLocationWasSelected = false;
let toLocationWasSelected = false;

export default {
  name: "AddTripModal",
  components: {
    PopupModal,
    TripFormHelpModal,
  },
  data() {
    return {
      showInvalidLocationModal: false,
      invalidLocationType: '',
      trip: {
        from: '',
        fromLat: '',
        fromLong: '',
        to: '',
        toLat: '',
        toLong: '',
        departureDate: '',
        earliestDepartureTime: '',
        latestDepartureTime: '',
        luggageCount: 0,
        comment: '',
        status: 'Pending',
      },
    }
  },
  methods: {
    show() {
      this.$refs.popup.open();

      this.$nextTick(() => {
        const acFrom = new google.maps.places.Autocomplete(this.$refs.fromRef, {
          types: ["transit_station"],
          fields: ["geometry"]
        });

        const acTo = new google.maps.places.Autocomplete(this.$refs.toRef, {
          types: ["transit_station"],
          fields: ["geometry"]
        });

        google.maps.event.addListener(acFrom, "place_changed", () => {
          let place = acFrom.getPlace().geometry.location;
          this.trip.fromLat = place.lat();
          this.trip.fromLong = place.lng();
          this.trip.from = document.getElementById('from').value;
          fromLocationWasSelected = true;
        });

        google.maps.event.addListener(acTo, "place_changed", () => {
          let place = acTo.getPlace().geometry.location;
          this.trip.toLat = place.lat();
          this.trip.toLong = place.lng();
          this.trip.to = document.getElementById('to').value;
          toLocationWasSelected = true;
        });

        document.getElementById('from').addEventListener('input', () => {
          fromLocationWasSelected = false;
        });

        document.getElementById('to').addEventListener('input', () => {
          toLocationWasSelected = false;
        });

        this.listenersMounted = true;
      });
    },
    _close() {
      this.$refs.popup.close();
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
    },
    showInvalidLocationAlert(locationType) {
      this.invalidLocationType = locationType;
      this.showInvalidLocationModal = true;
    },

    closeInvalidLocationModal() {
      this.showInvalidLocationModal = false;
    },
    submit() {
      if (!fromLocationWasSelected) {
        this.showInvalidLocationAlert('pickup');
        return;
      }
      if (!toLocationWasSelected) {
        this.showInvalidLocationAlert('dropoff');
        return;
      }
      console.log("Submitting trip:", { ...this.trip });
      this.$emit('addTripRequest', { ...this.trip });
      this.resetForm();
      this._close();
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


.trip-request-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
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
  margin-bottom: 15px;
  text-align:left;
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
  text-align: right;
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


.btn.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
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