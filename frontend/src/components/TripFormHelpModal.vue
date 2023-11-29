<template>
    <popup-modal ref="popup" medium>
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Help</h4>
        </div>
        <div class="modal-body">
            <!--make the text a bit shorter-->
            <p class="text-start">
                Creating a Trip Request<br>
                - To start, click 'Create a new trip request'. This opens the form to input your trip details.<br>
                Filling Out the Form<br>
                - Pickup Location: Enter your start location in the 'Pickup Location' field, using suggestions<br> 
                that appear as you type.<br>
                - Dropoff Location: Similarly, input your end location in the 'Dropoff Location' field.<br>
                - Departure Times: Choose your 'Earliest Departure Time' and 'Latest Departure Time' using <br>
                the datetime pickers.<br>
                - Walking Distance: Specify your maximum walking distance to and from pickup and dropoff <br>
                points in minutes.<br>
                - Luggage: Indicate the number of luggage bags.<br>
                - Additional Comments: Use the 'Additional comments' section for special requests or <br>
                considerations.<br>
                This could include preferences like a child seat, assistance for <br>
                differently-abled passengers, etc. There's a character limit to ensure concise <br>
                communication.<br>
                Submitting the Form<br>
                - Click 'Create trip request' to submit. Use the 'Reset' button to clear all fields if needed.<br>
                - After Submission - You'll receive an email notification about the status of your trip request <br>
                after submission.<br>
                - Accessing Trip Requests: Navigate to the 'Trip Requests' tab to view your submitted requests.<br>
                - Trip Request Details: Each request is listed with details like departure and arrival locations, <br>
                and departure times.<br>
                Status and Actions:<br>
                - Each request shows its current status (e.g., pending, confirmed).<br>
                - You can withdraw a request or accept/reject join requests for your trip.<br>
                - After Submission - You'll receive an email notification about the status of your trip request 
                <br>after submission.
            </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="_close">
            Close
          </button>
        </div>
      </div>
    </popup-modal>
  </template>
  
  <script>
  import PopupModal from "./PopupModal.vue";
  
  export default {
    name: "TripFormHelpModal",
  
    components: { PopupModal },
  
    methods: {
      show() {
        this.$refs.popup.open();
      },
      _close() {
        this.$refs.popup.close();
      },
    },
  };
  </script>