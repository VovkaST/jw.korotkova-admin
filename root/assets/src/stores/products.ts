import { defineStore } from 'pinia';
import { OpenAPI, ProductsService } from '@/api/generated/public';

if (import.meta.env.DEV) {
  OpenAPI.BASE = 'http://127.0.0.1:8001';
}

export const useProductsStore = defineStore('ProductsStore', {
  actions: {
    getProductsInStock() {
      return ProductsService.getProductsInStock();
    },
  },
});
