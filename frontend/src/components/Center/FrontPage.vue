<template>
    <main>
      <div class="main-content" :style="{ 'margin-left': sidebarWidth }">
        <div>
            <h1>Welcome, {{ props.user }}</h1>
            How it works <br>  
            1. Add new trip request
            2. Form your group
            3. Monitor people trying to join your group
        </div>
      </div>
    </main>
</template>
  
  
<script setup>
import { defineProps, onMounted, reactive } from 'vue';


const props = defineProps(['user'])
</script>


<style scoped>

</style>