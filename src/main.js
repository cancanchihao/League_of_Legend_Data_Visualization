import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App)

// 添加 favicon
const link = document.createElement('link');
link.rel = 'icon';
link.href = 'title.ico'; // 确保这个路径与您的 favicon 文件位置相匹配
document.head.appendChild(link);

app.use(router)
app.use(vuetify)
app.mount('#app')
