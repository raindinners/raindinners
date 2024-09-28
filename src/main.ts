import { registerPlugins } from "./plugins";

import "@/styles/styles.css";
import App from "@/App.vue";
import { createApp } from "vue";

const app = createApp(App);
app.config.compilerOptions.isCustomElement = (_) => {
  return true;
};
registerPlugins(app);
app.mount("#app");
