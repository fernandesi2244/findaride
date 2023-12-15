<template>
    <header>
        <h1>How to use findaride!</h1>
    </header>

    <section>
        <h2>Getting Started</h2>
        <p>Before you start booking your next ride, here's a quick guide on how to use findaride.<br><br>
            Please note that findaride bookings are independent of public transport schedules, i.e.,
            we only provide a scheduling and group formation mechanism based on user preferences
            and don't handle the process of actually acquiring the Uber/Lyft. As the actual availability
            of rides may vary, be sure to cross-reference the trip information under the 'Manage my trips' tab
            with availability for the preferred ride-sharing service.</p>
    </section>
    <section>
        <p>Filter trip data by typing your trip details. Once you find a trip that meets your criteria, mark the checkbox next to it
          and click the 'Request to join' button to send a request to join that group. You can then view these requests under the
          'Manage my trips' tab.</p>
        <div class="profile-image">
            <img class="img-fluid" src="/assets/filter_trips.jpeg" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>
    <section>
    <p>If you don't find a suitable trip, or if there aren't trips available, feel free to create a new one.</p>
        <div class="profile-image">
            <img class="img-fluid" src="/assets/create_trip.png" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>
        <section>
        <!---TO DO: Create an image for manage my trip tab with join requests functionality-->
        <p>Review your trip details in the 'Manage my trips' tab once you're done.</p>
        <div class="profile-image">
            <img class="img-fluid" src="/assets/manage_trips.jpeg" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
        <p>It's simple! You'll receive email notifications for trip updates, which can also be viewed in the 'Manage my trips' tab.
        </p>
    </section>
    <section>
            <p>View statistics about your past trips on your profile page.</p>
        <div class="profile-image">
            <img class="img-fluid" src="/assets/profile.png" alt="Profile" style="max-width:600pt; height:300pt;">
        </div>
    </section>

    
</template>

<style scoped>
/* Base Styles */
header h1 {
  text-align: center;
  /* color: #007bff; */
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
