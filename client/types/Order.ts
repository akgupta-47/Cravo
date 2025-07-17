import { Product } from "./Product";

export interface Order {
    id: number;
    products: Product[]; // Array of product image URLs
    status: string;
    date: string;
    total: string;
  }