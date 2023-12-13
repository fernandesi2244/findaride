<template>
  <div class="about">
    <header class="header">
      <h1>About findaride</h1>
    </header>

    <section class="concept">
      <p>
        findaride is an innovative platform designed to take
        the hassle out of student ride-sharing. Recognizing the
        struggles with costly fares and the endless search
        through email threads and spreadsheets, we offer
        a streamlined solution for your journey's needs.
      </p>
    </section>

    <section class="mission">
      <p>
        Our mission is to revolutionize the way students find
        and book their rides. When peak travel season rolls around,
        findaride steps in to provide a service that’s not only
        easy to use but also kind to your wallet. We’ve crafted
        a tool that does away with the complexities of planning
        your trips, whether it’s a ride back home or to an event.
      </p>
      <p>
        At the core of findaride is a commitment to simplicity
        and affordability. We understand that manual searches
        for the right travel option can be time-consuming
        and frustrating, often leading to overpriced choices
        or last-minute scrambles. findaride eliminates this
        stress by consolidating travel options in one accessible
        place, enabling students to book their ride in
        just a few clicks.
      </p>
      <p>
        Our platform is more than just a booking service; it’s a
        community where students can find companions for their
        journeys, share costs, and make travel during the busiest
        times of the year as smooth as possible. Our vision is for
        findaride to become an indispensable travel companion for
        students, ensuring that you can focus more on your studies
        and less on how you’ll get to your next destination.
      </p>
    </section>
    <section class="team">
      <h2>The team behind findaride</h2>
      <ul>
        <li>Ian Fernandes - ianfernandes@princeton.edu (<a target="_blank"
            href="https://www.linkedin.com/in/ian-fernandes/">LinkedIn</a>)</li>
        <li>Dylan Li - dl2223@princeton.edu (<a target="_blank"
            href="https://www.linkedin.com/in/dylan-li-0b7772222/">LinkedIn</a>)</li>
        <li>Kohei Sanno - ks1495@princeton.edu (<a target="_blank"
            href="https://www.linkedin.com/in/koheisanno/">LinkedIn</a>)</li>
        <li>Darren Alexis - da2476@princeton.edu (<a target="_blank"
            href="https://www.linkedin.com/in/darren-alexis-210078256/">LinkedIn</a>)</li>
      </ul>
    </section>
    <section class="acknowledgments">
      <h2>Special thanks to</h2>
      <ul>
        <li>Tolulope Oshinowo COS 333 - Fall 2023 Advisor</li>
        <li>Robert Dondero - COS 333 Fall 2023 Professor</li>
      </ul>
    </section>
  </div>
</template>
  
<style scoped>
.about {
  font-family: 'Roboto', Arial, sans-serif;
  color: #4A4A4A;
  background-color: #F4F4F8;
  /* padding: 20px; */
  line-height: 1.6;
}

.header h1 {
  text-align: center;
  color: #333;
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

.team h2, .acknowledgments h2 {
  font-size: 2rem;
  color: #0056b3;
  margin-bottom: 15px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

ul li {
  margin-bottom: 10px;
}

ul li a {
  color: #007bff;
  text-decoration: none;
}

ul li a:hover {
  text-decoration: underline;
}

.footer nav p {
  margin: 0;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }

  section {
    padding: 15px;
  }

  .team h2, .acknowledgments h2 {
    font-size: 1.8rem;
  }
}

</style>
  