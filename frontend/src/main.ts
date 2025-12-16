import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './ui/router'

const app = createApp(App)

app.use(router)

app.config.errorHandler = (err, instance, info) => {
    console.error('Global Error:', err);
    console.error('Info:', info);
    // Show on screen for user
    const div = document.createElement('div');
    div.style.position = 'fixed';
    div.style.top = '0';
    div.style.left = '0';
    div.style.width = '100%';
    div.style.backgroundColor = 'red';
    div.style.color = 'white';
    div.style.zIndex = '99999';
    div.style.padding = '20px';
    div.textContent = `Global Error: ${err}`;
    document.body.appendChild(div);
};

app.mount('#app')

