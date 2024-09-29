declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

interface ImportMetaEnv {
  VITE_HTTP_URL: string;
  VITE_WEBSOCKET_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
