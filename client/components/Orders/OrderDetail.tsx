import { Order } from '@/types/Order';
import {
  Check,
  ChevronLeft,
  Copy,
  HelpCircle,
  MessageCircle,
  ReceiptIcon,
  Star,
} from 'lucide-react';
import OrderProduct from './OrderProduct';

export default function OrderDetail(props: {
  selectedOrder: Order;
  goBackToOrders: () => void;
}) {
  return (
    <div className="space-y-4 overflow-scroll">
      <div className="flex items-center text-gray-800">
        <ChevronLeft
          onClick={props.goBackToOrders}
          className="w-6 h-6 text-gray-600 mr-2"
        />
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-gray-800">
            Order #{props.selectedOrder.id}
          </span>
          <span>{props.selectedOrder.products.length} items</span>
        </div>
        {/* Buttons */}
        <div className="ml-auto flex space-x-4 mr-2">
          <button className="px-4 py-2 items-center bg-green-200 text-sm hover:bg-green-400 text-green-900 rounded">
            <Star className="inline mr-1 w-4 h-4" />
            Rate
          </button>
          <button className="px-4 py-2 items-center bg-green-200 text-sm hover:bg-green-400 text-green-900 rounded">
            <MessageCircle className="inline mr-1 w-4 h-4" />
            Help
          </button>
        </div>
      </div>
      <div className="p-4 flex flex-col space-y-4">
        {/* Order Status */}
        <h1 className="font-semibold text-gray-800 flex items-center">
          {props.selectedOrder.status} <Check className="ml-2 text-green-600" />
        </h1>
        <hr></hr>

        <span className="font-semibold text-gray-950">
          {props.selectedOrder.products.length} items in Shipment
        </span>
        {/* Product Images */}
        <div className="flex flex-col">
          {props.selectedOrder.products.map((product, index) => (
            <OrderProduct key={index} product={product} />
          ))}
        </div>
      </div>
      <div className="p-4 flex flex-col space-y-4">
        {/* Order Summary */}
        <h1 className="font-semibold text-gray-800 flex items-center">
          <ReceiptIcon className="mr-2 text-green-600" />
          Bill Summary
        </h1>
        <hr></hr>
        <div className="flex flex-col space-y-2">
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Item Total</span>
            <span className="text-sm font-semibold text-gray-800">$49.99</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Delivery Fee</span>
            <span className="text-sm font-semibold text-gray-800">$5.00</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Platform Fee</span>
            <span className="text-sm font-semibold text-gray-800">$2.50</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Discount</span>
            <span className="text-sm font-semibold text-green-600">
              -$10.00
            </span>
          </div>
          <hr />
          <div className="flex justify-between">
            <span className="text-md font-semibold text-gray-800">
              Total Bill
            </span>
            <span className="text-md font-bold text-gray-800">$47.49</span>
          </div>
        </div>
        <button className="px-4 py-2 w-[50%] bg-green-200 hover:bg-green-400 text-green-900 rounded">
            Download Invoice / Credit Note
        </button>
      </div>
      <div className="p-4 flex flex-col space-y-4">
        <h1 className="font-semibold text-gray-800 flex items-center">
          Order Details
        </h1>
        <hr />

        {/* Order ID */}
        <div className="flex flex-col space-y-2">
          <span className="text-sm text-gray-600">Order ID:</span>
          <span className="text-sm font-semibold text-gray-800">
            {props.selectedOrder.id}
            <Copy className="inline ml-2 w-4 h-4 text-gray-600 cursor-pointer" />
          </span>
        </div>

        {/* Delivery Address */}
        <div className="flex flex-col space-y-2">
          <span className="text-sm text-gray-600">Delivery Address:</span>
          <span className="text-sm font-semibold text-gray-800">
            123 Main Street, Los Angeles, CA
          </span>
        </div>

        {/* Order Placed */}
        <div className="flex flex-col space-y-2">
          <span className="text-sm text-gray-600">Order Placed:</span>
          <span className="text-sm font-semibold text-gray-800">
            July 10, 2025, 10:30 AM
          </span>
        </div>

        {/* Order Arrived */}
        <div className="flex flex-col space-y-2">
          <span className="text-sm text-gray-600">Order Arrived:</span>
          <span className="text-sm font-semibold text-gray-800">
            July 12, 2025, 2:00 PM
          </span>
        </div>

        {/* Shop Name */}
        <div className="flex flex-col space-y-2">
          <span className="text-sm text-gray-600">Shop Name:</span>
          <span className="text-sm font-semibold text-gray-800">
            Green Grocers
          </span>
        </div>
      </div>
    </div>
  );
}
