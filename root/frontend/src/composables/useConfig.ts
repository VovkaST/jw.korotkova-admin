export type SocialIcon = "telegram" | "vk" | "max";

export interface MessengerLink {
  label: string;
  description: string;
  href: string;
  icon: SocialIcon;
}

export interface ChannelLink {
  label: string;
  href: string;
  icon: SocialIcon;
  cta: string;
}

export interface PhoneConfig {
  /** Полный href для `<a href="...">`, например `tel:+79991234567` */
  telHref: string;
  /** Текст для отображения */
  label: string;
}

export interface ConsultationConfig {
  title: string;
  duration: string;
  price: string;
  description: string;
  specialOffer: string;
}

export interface AppConfig {
  /** Публичный URL этого сайта (лендинга) */
  siteUrl: string;
  /** Сайт автора вёрстки / разработки */
  authorSiteUrl: string;
  email: string;
  phone: PhoneConfig;
  inn: string;
  consultation: ConsultationConfig;
  messengerLinks: MessengerLink[];
  compassChannelLinks: ChannelLink[];
}

function envString(
  key: keyof ImportMetaEnv & string,
  fallback: string,
): string {
  const v = import.meta.env[key];
  return typeof v === "string" && v.length > 0 ? v : fallback;
}

/**
 * Конфигурация лендинга из переменных окружения (`VITE_*`).
 * Значения по умолчанию совпадают с прежними захардкоженными строками.
 */
export function useConfig(): AppConfig {
  return {
    siteUrl: envString("VITE_APP_URL", "https://jw-korotkova.ru"),
    authorSiteUrl: envString(
      "VITE_AUTHOR_SITE_URL",
      "https://korotkovladimir.ru/",
    ),
    email: envString("VITE_CONTACT_EMAIL", "hello@soultherapy.ru"),
    phone: {
      telHref: envString("VITE_CONTACT_PHONE_TEL", "tel:+79991234567"),
      label: envString("VITE_CONTACT_PHONE_LABEL", "+7 (999) 123-45-67"),
    },
    inn: envString("VITE_CONTACT_INN", "772775846428"),
    consultation: {
      title: envString(
        "VITE_CONSULTATION_TITLE",
        "Консультация «Терапия Души»",
      ),
      duration: envString("VITE_CONSULTATION_DURATION", "60 мин"),
      price: envString("VITE_CONSULTATION_PRICE", "3 000 ₽"),
      description: envString(
        "VITE_CONSULTATION_DESC",
        "Единичная сессия по вашему запросу",
      ),
      specialOffer: envString("VITE_CONSULTATION_SPECIAL_OFFER", ""),
    },
    messengerLinks: [
      {
        label: "Telegram",
        description: "Удобно с телефона и десктопа",
        href: envString("VITE_SOCIAL_TELEGRAM_DM", "https://t.me/"),
        icon: "telegram",
      },
      {
        label: "ВКонтакте",
        description: "Личные сообщения ВКонтакте",
        href: envString("VITE_SOCIAL_VK_DM", "https://vk.me/"),
        icon: "vk",
      },
      {
        label: "Max",
        description: "Написать в Max",
        href: envString("VITE_SOCIAL_MAX_DM", "#"),
        icon: "max",
      },
    ],
    compassChannelLinks: [
      {
        label: "Telegram",
        href: envString("VITE_CHANNEL_TELEGRAM_URL", "https://t.me/"),
        icon: "telegram",
        cta: "Перейти в канал",
      },
      {
        label: "ВКонтакте",
        href: envString("VITE_CHANNEL_VK_URL", "https://vk.com/"),
        icon: "vk",
        cta: "Перейти в сообщество",
      },
      {
        label: "Max",
        href: envString("VITE_CHANNEL_MAX_URL", "#"),
        icon: "max",
        cta: "Перейти в канал",
      },
    ],
  };
}
