<template>
    <transition name="fade">
      <div class="popup modal" tabindex="-1" v-if="isVisible">
        <div
          class="modal-dialog modal-dialog-centered"
          :class="{ 'modal-sm': small, 'modal-lg': large, 'modal-xl': xlarge }"
          :style="style"
        >
          <slot></slot>
        </div>
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    name: "PopupModal",
  
    props: {
      small: {
        type: Boolean,
        default: false,
      },
      medium: {
        type: Boolean,
        default: false,
      },
      large: {
        type: Boolean,
        default: false,
      },
      xlarge: {
        type: Boolean,
        default: false,
      },
      xxlarge: {
        type: Boolean,
        default: false,
      }
    },
  
    data: () => ({
      isVisible: false,
    }),
  
    computed: {
      style() {
        if (this.xxlarge) {
          return {
            "width": "1400px",
            "max-width": "1400px",
          };
        } else if (this.xlarge) {
          return {
            width: "1140px",
            "max-width": "1140px",
          };
        } else if (this.large) {
          return {
            width: "800px",
            "max-width": "800px",
          };
        } else if (this.medium) {
          return {
            width: "500px",
            "max-width": "500px",
          };
        } else {
          return {};
        }
      },
    },
  
    methods: {
      open() {
        this.isVisible = true;
      },
  
      close() {
        this.isVisible = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* css class for the transition */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  
  .popup {
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    z-index: 3;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
  }
  </style>