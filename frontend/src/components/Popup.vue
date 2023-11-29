<template>
    <transition name="fade">
        <div class="popup" v-if="isVisible">
            <div class="popup-inner" @click.stop>
                <slot />
                <button class="popup-close">
                    Close
                </button>
            </div>
        </div>
    </transition>
</template>


<script>
export default {
	props: ['TogglePopup'],
    data: () => ({
        isVisible: false,
    }),
  
    methods: {
        open() {
            this.isVisible = true;
        },

        close() {
            this.isVisible = false;
        },
    }
}
</script>

<style lang="scss" scoped>
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
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 99;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.popup-inner {
    background: white;
    padding: 32px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}


.popup-close {
    background: var(--primary-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    margin-top: 20px;
}

.popup-close:hover {
    background-color: #0056b3;
}

</style>