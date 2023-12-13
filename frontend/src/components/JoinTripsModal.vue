<template>
    <popup-modal ref="popup" medium>
      <div class="modal-content" style="text-align: left;">
        <div class="modal-body">
          <form @submit.prevent="submit" class="form-container">
            <h5 class="nickname">
                <label class="label" for="nickname">Nickname:</label>
                <input class="input" id="nickname" v-model="myData.nickname" type="text" placeholder="e.g. Spring break" maxlength="255" required>
            </h5>
            <div class="luggage">
                    <label class="text-start" for="luggage-count">Number of luggage bags:</label>
                    <input id="luggage-count" v-model.number="myData.luggageCount" type="number" min="0" required />
                </div>
            <div class="form-group">
              <label class="text-start" for="comments">Additional comments:</label>
              <textarea id="comments" v-model="myData.comment" placeholder="Any special accommodations, considerations, etc."
                maxlength="255"></textarea>
            </div>
              Request to join <b>{{ trips.length }}</b> trip(s)
            <hr>
            <div class="create-trip-footer">
                <button style="color: white" type="button" @click="_close" class="btn btn-secondary">Close</button>
              <button type="submit" class="btn primary">Send requests</button>
            </div>
          </form>
        </div>
      </div>
    </popup-modal>
  </template>
  
  <script>
  import PopupModal from "./PopupModal.vue";
  
  export default {
    name: "AddTripModal",
    components: {
      PopupModal,
    },
    props: ['trips'],

    data() {
      return {
        myData: {
            nickname: '',
            luggageCount: 0,
            comment: '',
        },
      }
    },
    methods: {
      show() {
        this.$refs.popup.open();
      },
      _close() {
        this.$refs.popup.close();
      },
      resetForm() {
        this.myData.nickname = ''
        this.myData.luggageCount = 0;
        this.myData.comment = '';
      },
      submit() {
        this.$emit('joinSelectedTrips', this.myData );
        this.$emit('refreshTrips');
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