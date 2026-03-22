import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: 'src/api/v1/schema.yaml',
  output: 'src/api/v1/client',
  plugins: ['@hey-api/client-next'],
  logs: 'info',
});
