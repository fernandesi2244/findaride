<template>
      <TripFormHelpModal ref="tripFormHelpModal"></TripFormHelpModal>
      <div class="modal-content">
        <div class="modal-body">
          <form @submit.prevent="submit" class="form-container">
            <div class="form-row">
            <div class="form-group">
              <label class="text-start" for="from">Pickup location:</label>
              <input id="from" ref="fromRef" v-model="trip.from" placeholder="Start typing to see results..." required />
            </div>
            <div class="form-group">
              <label class="text-start" for="to">Dropoff location:</label>
              <input id="to" ref="toRef" v-model="trip.to" placeholder="Start typing to see results..." required />
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
              <label class="text-start" for="pickup-time">Earliest departure time:</label>
              <input id="pickup-time" v-model="trip.earliestDepartureTime" type="datetime-local" required />
            </div>
            <div class="form-group">
              <label class="text-start" for="dropoff-time">Latest departure time:</label>
              <input id="dropoff-time" v-model="trip.latestDepartureTime" type="datetime-local" required />
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
              <label class="text-start" for="luggage-count">Number of luggage bags:</label>
              <input id="luggage-count" v-model.number="trip.luggageCount" type="number" min="0" required />
            </div>
        </div>
        <button v-tooltip="'Would you like to create a trip?'" id="add-trip-btn" @click="addManualTripRequest" class="btn btn-primary">Create a new trip</button>
          
            <!-- <div class="form-actions">
              <button type="submit" class="btn primary">Find Matching Trips</button>
            </div> -->
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
  
  let fromLocationWasSelected = false;
  let toLocationWasSelected = false;
  
  export default {
    name: "AddTripModal",
    components: {
      TripFormHelpModal,
      
    },
    data() {
      return {
        showInvalidLocationModal: false,
        invalidLocationType: '',
        fromLocationWasSelected: false,
        toLocationWasSelected: false,
        from: '',
        to: '',
        trip: {
          fromLat: '',
          fromLong: '',
          toLat: '',
          toLong: '',
          departureDate: '',
          earliestDepartureTime: '',
          latestDepartureTime: '',
          luggageCount: 0,
          comment: '',
        },
      }
    },
    computed: {
        allFieldsFilled() {
        return this.trip.from && this.trip.to && this.trip.earliestDepartureTime && this.trip.latestDepartureTime && this.trip.luggageCount > 0;
        },
    },
    watch: {
        'trip.from': 'checkAndCreateTripRequest',
        'trip.to': 'checkAndCreateTripRequest',
        'trip.earliestDepartureTime': 'checkAndCreateTripRequest',
        'trip.latestDepartureTime': 'checkAndCreateTripRequest',
        'trip.luggageCount': 'checkAndCreateTripRequest',
    },
    mounted() {
    this.initializeAutocomplete();
    },
    methods: {
        checkAndCreateTripRequest() {
          this.autoSearchForTrips();
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
        this.from = this.$refs.fromRef.value;
        this.$emit('getTrips', { ...this.trip });
        fromLocationWasSelected = true;
      });

      acTo.addListener("place_changed", () => {
        let place = acTo.getPlace().geometry.location;
        this.trip.toLat = place.lat();
        this.trip.toLong = place.lng();
        this.to = this.$refs.toRef.value;
        this.$emit('getTrips', { ...this.trip });
        toLocationWasSelected = true;
      });
    },
      _close() {
        this.$refs.popup.close();
      },
      toggleHelp() {
        console.log(this.$refs.tripFormHelpModal)
        this.$refs.tripFormHelpModal.show();
      },
      async addManualTripRequest() {
        if(!validateFormData(tripData)) return;
        showCommentsAndLuggagePopup();
        let data = {
            "earliest_departure_time": trip.earliestDepartureTime,
            "latest_departure_time": trip.latestDepartureTime,
            "num_luggage_bags": trip.luggageCount,
            "user": user.id,
            "departure_location": trip.departure_location,
            "arrival_location": trip.arrival_location,
        };
        
        const endpoint = await endpoints["tripRequest"];
        try {
            const response = axios.post(endpoint, data);    
            if (response.status === 200) {
              alert("Trip created successfully!");
            } else {
              alert("Trip creation failed. Please try again.");
            } 
          }
        catch (error) {
            alert("Error creating trip: " + error.message);
        }
        },
      resetForm() {
        this.from = '';
        this.trip.fromLat = '';
        this.trip.fromLong = '';
        this.to = '';
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
        this.$emit('refreshTrips');
        this.resetForm();
        this._close();
      },
      autoSearchForTrips() {
        console.log("TEST")
        this.$emit('getTrips', { ...this.trip });
      },
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
  flex: 1;
  margin-right: 10px;
}
  .form-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
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