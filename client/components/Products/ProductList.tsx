import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Image from 'next/image';
import Product from './Product';

export default function ProductList() {
  const products = [
    {
      id: 1,
      category: 'FRESH',
      name: 'Fresh Bananas',
      description: 'Fresh organic bananas',
      price: '$2.99',
      image: '/placeholder.svg?height=200&width=300',
    },
    {
      id: 2,
      category: 'FRESH',
      name: 'Organic Apples',
      description: 'Crisp organic red apples',
      price: '$4.99',
      image: '/placeholder.svg?height=200&width=300',
    },
    {
      id: 3,
      category: 'HOME',
      name: 'Fresh Bread',
      description: 'Freshly baked artisan bread',
      price: '$3.49',
      image: '/placeholder.svg?height=200&width=300',
    },
    {
      id: 4,
      category: 'FRESH',
      name: 'Organic Milk',
      description: 'Fresh organic whole milk',
      price: '$5.99',
      image: '/placeholder.svg?height=200&width=300',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <p className="text-gray-600 text-lg">
          Favourite items from your hometown vendors
        </p>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <Product key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
