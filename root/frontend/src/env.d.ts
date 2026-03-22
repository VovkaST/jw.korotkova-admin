/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_URL?: string;
  readonly VITE_AUTHOR_SITE_URL?: string;
  readonly VITE_CONTACT_EMAIL?: string;
  readonly VITE_CONTACT_PHONE_TEL?: string;
  readonly VITE_CONTACT_PHONE_LABEL?: string;
  readonly VITE_CONTACT_INN?: string;
  readonly VITE_CONSULTATION_TITLE?: string;
  readonly VITE_CONSULTATION_DURATION?: string;
  readonly VITE_CONSULTATION_PRICE?: string;
  readonly VITE_CONSULTATION_SPECIAL_OFFER?: string;
  readonly VITE_CONSULTATION_DESC?: string;
  readonly VITE_SOCIAL_TELEGRAM_DM?: string;
  readonly VITE_SOCIAL_VK_DM?: string;
  readonly VITE_SOCIAL_MAX_DM?: string;
  readonly VITE_CHANNEL_TELEGRAM_URL?: string;
  readonly VITE_CHANNEL_VK_URL?: string;
  readonly VITE_CHANNEL_MAX_URL?: string;
}

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
