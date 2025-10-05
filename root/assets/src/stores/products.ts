import { defineStore } from 'pinia';
import { OpenAPI, ProductsService } from '@/api/generated/public';

OpenAPI.BASE = import.meta.env.VITE_API_URL;

export const useProductsStore = defineStore('ProductsStore', {
  actions: {
    getProductsInStock() {
      return ProductsService.getProductsInStock();
    },
  },
});
