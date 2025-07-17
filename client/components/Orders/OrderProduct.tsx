import Image from 'next/image';
import { Product as ProductType } from '@/types/Product';

export default function OrderProduct(props: { product: ProductType }) {
  return (
    <div
      key={props.product.id}
      className="flex items-center space-x-4 rounded-lg p-4"
    >
      {/* props.product Image */}
      <img
        src={props.product.image || '/placeholder.svg'}
        alt={props.product.name}
        className="w-5 h-4"
      />

      {/* props.product Details */}
      <div className="flex-1">
        <h4 className="text-sm font-semibold flex text-gray-800">
          {props.product.name}
        </h4>
        <h4 className="text-sm text-gray-800">
          {props.product.unit} | {props.product.quantity}
        </h4>
      </div>

      {/* props.product Price */}
      <div>
        <div className="text-sm font-semibold text-gray-800">
          {props.product.price}
        </div>
        <div className="text-sm text-gray-400 line-through">{'$8000'}</div>
      </div>
    </div>
  );
}
