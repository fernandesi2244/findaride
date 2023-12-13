<template>
    <header>
        <h1>Welcome to FindARide!</h1>
    </header>

    <section>
        <h2>Getting Started</h2>
        <p>Before you start booking your next ride, here's a quick guide on how to use findaride.
            Please note, findaride bookings are independent of traditional taxi or public transport
            services. Availability may vary, so always check the 'Manage My Trips' tab for specific
            information about each ride, including current group members and pending join requests.</p>
    </section>
    <section>
        <p>Filter trip data by typing your trip details. Once you find a trip that meets your criteria, send a join request.</p>
        <!---TO DO: Add comments to each picutre explaining features-->
        <!-- TO DO: Create an image showing filtering data with a created trip showing join feature -->
        <div class="profile-image">
            <img class="img-fluid" src="static/filter_trips.jpeg" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>
    <section>
    <p>If you don't find a suitable trip, or there are no trips available, feel free to create a new one.</p>
        <div class="profile-image">
            <img class="img-fluid" src="static/create_trip.png" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>
        <section>
        <!---TO DO: Create an image for manage my trip tab with join requests functionality-->
        <p>Review your trip details in the 'Manage My Trips' tab once you're done.</p>
        <div class="profile-image">
            <img class="img-fluid" src="static/manage_trips.jpeg" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
        <p>It's simple! You'll receive email notifications for trip updates, which can also be viewed in the 'Manage My Trips' tab.
            
        </p>
    </section>
    <section>
            <p>View statistics about your past trips on your profile page.</p>
        <div class="profile-image">
            <img class="img-fluid" src="static/profile.png" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>

    
</template>

<style scoped>
/* Base Styles */
header h1 {
  text-align: center;
  color: #007bff;
  font-size: 2.5rem;
  margin-bottom: 30px;
}

section {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: justify;
}

h2 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 15px;
}

p {
  font-size: 1rem;
  color: #4A4A4A;
  line-height: 1.6;
  margin-bottom: 15px;
}

.profile-image {
  text-align: center;
  margin: 20px 0; 
}

.img-fluid {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

@media (max-width: 768px) {
  header h1 {
    font-size: 2rem;
  }

  section {
    padding: 15px;
  }

  h2 {
    font-size: 1.8rem;
  }
}

</style>

<script>
</script>
