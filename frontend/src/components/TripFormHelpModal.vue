<template>
  <popup-modal ref="popup" medium>
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title">Help</h4>
      </div>
      <div class="modal-body">
        <!--make the text a bit shorter-->
        <p class="text-start">
        <h5>Creating a trip request</h5>
        To start, click 'Create a new trip request'. This opens the form to input your trip details.<br>
        <ol>
          <li>Pickup location: Enter your start location in the 'Pickup location' field, using suggestions
            that appear as you type.</li>
          <li>Dropoff location: Similarly, input your end location in the 'Dropoff location' field.</li>
          <li>Departure times: Choose your 'Earliest departure time' and 'Latest departure time' using
            the datetime pickers.</li>
          <li>Walking distance: Specify your maximum walking distance to and from pickup and dropoff
            points in minutes.</li>
          <li>Luggage: Indicate the number of luggage bags.</li>
          <li>Additional comments: Use the 'Additional comments' section for special requests or
            considerations.
            This could include preferences like a child seat, assistance for differently-abled passengers, etc.
            There's a character limit to ensure concise communication.</li>
        </ol>
        Click 'Create trip request' to submit.<br><br>

        <h5>After submitting the form</h5>
        <ol>
          <li>After successfully creating a trip request, either we will send requests to join specific existing groups
            on your behalf, or if no such groups exist, we will create a new trip for you. Check the 'My confirmed trips' and
            'My pending trips' tabs to determine which outcome was the case.</li>
          <li>If we've made requests to join specific groups on your behalf, then you'll receive an email notification if one of
            those groups accepts you. You can then proceed to confirm the acceptance. However, if no group accepts you, then
            a trip will automatically be created for you.</li>
          <li>If a trip was automatically created for you upon entering your trip details, then you're all set! You'll automatically
            receive requests to join your group (as emails) from other students with similar trip profiles.
          </li>
        </ol>
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

<style scoped>
.modal-body {
  max-height: 593px;
  overflow-y: auto;
}
</style>