export interface Product {
    id: number;
    category: string;
    name: string;
    description: string;
    price: string;
    image: string;
    quantity?: number; // Optional for products in cart
    unit?: string; // Optional for products in orders
}