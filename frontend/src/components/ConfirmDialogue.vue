<template>
    <popup-modal ref="popup" small>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
        </div>
        <div class="modal-body">
          <p>
            {{ message }}
          </p>
        </div>
        <div class="modal-footer">
          <button :class="cancelClass" @click="_cancel">
            {{ cancelButton }}
          </button>
          <button v-if="okButton" type="button" :class="okClass" @click="_confirm">
            {{ okButton }}
          </button>
        </div>
      </div>
    </popup-modal>
  </template>
  
  <script>
  import PopupModal from "./PopupModal.vue";
  
  export default {
    name: "ConfirmDialogue",
  
    components: { PopupModal },

    data: () => ({
      // Parameters that change depending on the type of dialogue
      title: undefined,
      message: undefined, // Main text content
      okButton: undefined, // Text for confirm button; leave it empty because we don't know what we're using it for
      cancelButton: "Cancel", // text for cancel button
      cancelClass: "btn btn-secondary",
      okClass: "btn btn-primary",
  
      // Private variables
      resolvePromise: undefined,
      rejectPromise: undefined,
    }),
  
    methods: {
      async show(opts = {}) {
        this.title = opts.title;
        this.message = opts.message;
        this.okButton = opts.okButton;
        if (opts.cancelButton) {
          this.cancelButton = opts.cancelButton;
        }
        if(opts.cancelClass) {
            this.cancelClass = opts.cancelClass;
        }
        if(opts.okClass) {
            this.okClass = opts.okClass
        }

        // Once we set our config, we tell the popup modal to open
        this.$refs.popup.open();
        // Return promise so the caller can get results
        return new Promise((resolve, reject) => {
          this.resolvePromise = resolve;
          this.rejectPromise = reject;
        });
      },
  
      _confirm() {
        this.$refs.popup.close();
        this.resolvePromise(true);
      },
  
      _cancel() {
        this.$refs.popup.close();
        this.resolvePromise(false);
      },
    },
  };
  </script>