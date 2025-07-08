import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Image from 'next/image';
import { Product as ProductType } from '@/types/Product';

export default function Product(props: { product: ProductType }) {
  return (
    <div
      key={props.product.id}
      className="bg-white rounded-xl shadow-sm border hover:shadow-md transition-shadow"
    >
      <div className="aspect-square relative overflow-hidden rounded-t-xl">
        <Image
          src={props.product.image || '/placeholder.svg'}
          alt={props.product.name}
          fill
          className="object-cover"
        />
        <Button className="absolute bottom-2 right-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
          <span className="hidden sm:inline">Add to Cart</span>
          <span className="inline sm:hidden">Add +</span>
        </Button>
      </div>
      <div className="p-4">
        <Badge className={`text-xs font-medium mb-2`}>
          {props.product.category}
        </Badge>
        <h3 className="font-semibold text-gray-900 mb-1">
          {props.product.name}
        </h3>
        <p className="text-sm text-gray-600 mb-3">
          {props.product.description}
        </p>
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-gray-900">
            {props.product.price}
          </span>
        </div>
      </div>
    </div>
  );
}
