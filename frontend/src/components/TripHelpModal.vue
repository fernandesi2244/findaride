<template>
    <popup-modal ref="popup" medium>
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Help</h4>
        </div>
        <div class="modal-body">
          <!--make the text a bit shorter-->
          
          
          <p class="text-start">
            <h5>Confirmed trips and pending trips</h5>
            <p>The following assumes you have already planned a new trip. If not, please do so and come back!</p>
            <h6>Confirmed trips</h6>
            <ol>
              <li>These represent trips that you're definitely a part of. Scroll through the list of trips and
                select any one to view more details like the other members of the group (as well as their contact
                info), the total number of luggage bags, and join requests.
              </li>
              <li> Join requests are requests from other users to join your trip. You can accept or reject these
                requests here. For a new member to be accepted into your trip, all members of the trip must
                accept them. <em>To maximize the chance of that person joining your group, we recommend that all members
                accept the new person as soon as possible.</em></li>
              <li> Sometimes, shit happens. If you at any point need to drop the trip, we recommend you do so as soon as
                possible by clicking the 'Leave' button in the trip details. This will automatically notify all other members
                of the group for you.</li>
              <li> <strong>When the time comes, use the 'Copy emails' button to get the contact information for everyone in your
                group. Set up an email chat to discuss the specifics of the Uber/Lyft ride as well as the precise time that
                everyone wants to leave at.
              </strong></li>
            </ol>
            <br>
            <h6>Pending trips</h6>
            <ol>
                <li>These represent trips that are indeterminate. In other words, when your trip is in this phase, we're 
                  actively looking for existing trips that you could join.
                </li>
                <li>When you plan a new trip using our automatic matching algorithm, we'll send requests to at most 5 individual
                  trips that match the parameters of your requested trip. These are the 'Trip matches' that you see under each
                  pending trip. If no such trips exist, we'll create a new trip for you that others can then join (which will be
                  located under the confirmed trips tab).
                </li>
                <li>The members of the trips that are compatible with your trip request will receive notifications and can either
                  accept or reject your request (as described above).</li>
                <li> If all members of a group agree to accept you, you will receive a
                    notification for final confirmation. If you get a confirmation notification, go to the pending trips tab, select
                    the trip for which you have received a confirmation request, and either accept or deny the invitation. <em>We recommend
                      that you don't take too much time in making this decision, as the trip may fill up by the time you accept their invitation,
                      in which case you've missed that opportunity.</em> After you accept a confirmation request, all other members will be notified,
                    and the trip details will be updated accordingly.</li>
                <li>Note that confirmation requests simply give you the ability to decide between multiple groups that you've
                  been accepted into for the same trip request. You can choose the trip that best suits you based on time,
                  number of members, number of luggage bags, etc. If you'd like to automatically accept the first confirmation
                  request you get, you can enable this setting in your profile.</li>
                <li> In case of rejection, don't worry. It may be that your requested departure time span is too extreme in
                  either direction. In any case, you will have the option to either be placed in a new group or select another existing group.</li>
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