import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/js/all'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App).use(vuetify).use(router);

app.directive('tooltip', {
  mounted(el, binding) {
    el.style.position = 'relative';
    const span = document.createElement('span');
    span.textContent = binding.value;
    span.style.visibility = 'hidden';
    span.style.position = 'absolute';
    span.style.bottom = '100%';
    span.style.left = '50%';
    span.style.transform = 'translateX(-50%)';
    span.style.backgroundColor = 'black';
    span.style.color = 'white';
    span.style.padding = '5px 10px';
    span.style.borderRadius = '4px';
    span.style.fontSize = '14px';
    span.style.whiteSpace = 'nowrap';
    el.appendChild(span);

    el.onmouseenter = () => span.style.visibility = 'visible';
    el.onmouseleave = () => span.style.visibility = 'hidden';
  }
});

app.mount('#app');
