<template>
    <popup-modal ref="popup" medium>
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Help</h4>
        </div>
        <div class="modal-body">
          <!--make the text a bit shorter-->
          
          
          <p class="text-start">
            <h5>User Instructions for Ride-Sharing Trip Requests and Group Management</h5>
            <ol>
                <li> Begin by clicking on 'Create a new trip request'. This action will open
                    a form where you can input all the necessary details for your trip.</li>
                <li>Once you have filled in the form, submit it. The system will then start
                    searching for groups that match your specified departure times, locations,
                    and other preferences.</li>
                <li>Groups that are compatible with your trip request will receive
                    notifications. These groups will review your request and either
                    accept or reject it.</li>
                <li>Groups will receive continuous reminders to make a decision regarding
                    your request.</li>
                <li> If all members of a group agree to accept you, you will receive a
                    notification for final confirmation.</li>
                <li> In case of rejection, don't worry. You will have the option to either be
                    placed in a new group or select another existing group.</li>
                <li> As a group member, you will receive email notifications when
                    someone requests to join your group.</li>
                <li>Review the requesting member's trip details and personal information.
                    Based on this information, you can either accept or reject their request.</li>
                <li>Once all current group members accept a new member, that individual
                    must confirm their placement in the group.</li>
                <li>After this confirmation, all members of the group will be notified,
                    and the trip details will be updated accordingly. </li>
                <li>If the group you have joined does not meet your needs, you have the
                    option to request reassignment to a different group.</li>
                <li> Should you need to cancel your trip, this action will update the
                    group's travel statistics and notify other group members of the change.</li>
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