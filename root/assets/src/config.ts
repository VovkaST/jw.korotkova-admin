interface ImportMetaEnv {
  readonly siteTitle: string
  readonly siteDescription: string
  readonly siteDescriptionOG: string
  readonly siteUrl: string
}

export const Config: ImportMetaEnv = {
  siteTitle: import.meta.env.VITE_SITE_TITLE,
  siteDescription: import.meta.env.VITE_SITE_DESCRIPTION,
  siteDescriptionOG: import.meta.env.VITE_SITE_DESCRIPTION_OG,
  siteUrl: import.meta.env.VITE_SITE_URL,
} as const;
