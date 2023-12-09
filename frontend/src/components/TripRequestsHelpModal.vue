<template>
    <popup-modal ref="popup" medium>
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Help</h4>
        </div>
        <div class="modal-body">
            <p class="text-start">
              Welcome to your trip request management tab! Here's a quick guide on how to navigate<br>
                through trip matches and confirmation requests:<br><br>
                Trip Matches: These are potential trips that match your preferences. You'll see details<br>
                like departure and arrival locations, times, luggage totals, and number of riders. Please<br>
                note, these details represent the trip status before your addition.<br><br>
                To remove yourself from a trip match, simply click the "Withdraw" button next to the <br>
                respective trip.<br><br>
                Confirmation Requests: These are trips where your addition has been proposed, and you <br>
                need to confirm your participation. Details here represent the trip status after your <br>
                potential addition.<br><br>
                To join a trip, click the "Accept" button. This will confirm your participation and <br>
                update the trip details. If the trip no longer suits you, click the "Reject" button <br>
                to decline the offer.<br>
                <br>
                Remember, your decisions affect the trip dynamics, so please choose carefully!
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
    name: "TripRequestsHelpModal",
  
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