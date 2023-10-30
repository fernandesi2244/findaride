<template>
    <div class="modal-overlay">
      <div class="modal">
        <h3>Add a new trip</h3>
        
        <form @submit.prevent="submit">
          <!-- Form fields for trip details -->
          <div class="form-group">
            <input v-model="trip.from" placeholder="From" required />
          </div>
          <div class="form-group">
            <input v-model="trip.to" placeholder="To" required />
          </div>
          <div class="form-group">
            <input v-model="trip.departureTime" type="time" required />
          </div>
          <div class="form-group">
            <input v-model.number="trip.luggageCount" type="number" min="0" required />
          </div>
          <div class="form-group">
            <textarea v-model="trip.comments" placeholder="Other comments"></textarea>
          </div>
          
          <button type="submit" class="btn">Add Trip</button>
        </form>
        
        <button @click="closeModal" class="btn cancel-btn">Cancel</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, defineEmits } from 'vue';
  const emit = defineEmits(['addTrip', 'close']);
  const trip = reactive({
    id: Date.now(),
    from: '',
    to: '',
    departureTime: '',
    luggageCount: 0,
    comments: '',
    status: 'Pending',
  });
  
  function submit() {
    console.log("Submitting trip:", trip);
    emit('addTrip', { ...trip });
    resetForm();
  }
  
  function closeModal() {
    emit('close');
    resetForm();
    router.push('/dashboard');
  }
  
  function resetForm() {
    trip.from = '';
    trip.to = '';
    trip.departureTime = '';
    trip.luggageCount = 0;
    trip.comments = '';
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal {
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    width: 90%;
    max-width: 400px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  input, textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  textarea {
    resize: vertical;
  }
  
  .btn {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .cancel-btn {
    background: #e74c3c;
    color: #fff;
  }
  
  .btn:not(.cancel-btn) {
    background: #2ecc71;
    color: #fff;
  }
  
  .btn:not(.cancel-btn):hover {
    background: #27ae60;
  }
  </style>
  