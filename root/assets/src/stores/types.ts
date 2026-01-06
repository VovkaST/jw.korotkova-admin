import { type ProductDTO } from '@/api/generated/public/models/ProductDTO';
import { type ProductFileDTO } from '@/api/generated/public/models/ProductFileDTO';

export type IProduct = ProductDTO;
export type IProductFile = ProductFileDTO;

export enum ImageSizes {
  ORIGINAL = 'ORIGINAL',
  XL = 'XL',
  L = 'L',
  M = 'M',
  S = 'S',
};
