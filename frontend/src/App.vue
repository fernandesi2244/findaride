<template>
<div id="app" class="box">
    <nav>
        <div class="nav-content">
            <span class = text-size><router-link to="/">findaride</router-link></span>

            <div class="right">
                <router-link to="/">Home</router-link> |
                <router-link to="/about">About</router-link> |
                <!----<a href="/accounts/login/">Login</a> |
                <a href="/accounts/logout/">Logout</a> |
                <router-link to="/login">Login</router-link> |
                <router-link to="/signup">Sign Up</router-link>| ---->
                <router-link to="/dashboard">Dashboard</router-link>
            </div>
        </div>
    </nav>

    <router-view class="full-height"/>
</div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.modal.show {
  z-index: 10000;
}

.box {
  display: flex;
  flex-flow: column;
  height: 100vh;
}

.full-height {
    height: 100%;
}

nav {
  background: #aed8ab;
  box-shadow: 0 2px 4px rgba(182, 166, 166, 0.1);
  padding: 0.5rem 2rem;
  
}
.nav-content {
  max-width: none;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  padding: 0 10px;
}

.text-size {
  font-size:22px;
}

.right {
  display: flex;
  align-items: center;
}
</style>
