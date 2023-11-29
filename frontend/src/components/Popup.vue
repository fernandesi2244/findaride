<template>
    <div class="popup" @click="TogglePopup">
        <div class="popup-inner" @click.stop>
            <slot />
            <button class="popup-close" @click="TogglePopup">
                Close
            </button>
        </div>
    </div>
</template>


<script>
export default {
	props: ['TogglePopup']
}
</script>

<style lang="scss" scoped>
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