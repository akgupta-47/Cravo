"use client";
import { Order } from "@/types/Order";
import { ArrowDownIcon, CheckCircle } from "lucide-react";
import { useState } from "react";
import OrderDetail from "./OrderDetail";

const initialOrders: Order[] = [
  {
    id: 1,
    products: [    {
      id: 1,
      category: 'FRESH',
      name: 'Fresh Bananas',
      description: 'Fresh organic bananas',
      price: '$2.99',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    },
    {
      id: 2,
      category: 'FRESH',
      name: 'Organic Apples',
      description: 'Crisp organic red apples',
      price: '$4.99',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    },
    {
      id: 3,
      category: 'HOME',
      name: 'Fresh Bread',
      description: 'Freshly baked artisan bread',
      price: '$3.49',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    }],
    status: "Order Delivered",
    date: "July 10, 2025, 10:30 AM",
    total: "$49.99",
  },
  {
    id: 2,
    products: [    {
      id: 1,
      category: 'FRESH',
      name: 'Fresh Bananas',
      description: 'Fresh organic bananas',
      price: '$2.99',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    },
    {
      id: 2,
      category: 'FRESH',
      name: 'Organic Apples',
      description: 'Crisp organic red apples',
      price: '$4.99',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    }],
    status: "Order Pending",
    date: "July 9, 2025, 2:15 PM",
    total: "$29.99",
  },
  {
    id: 3,
    products: [    {
      id: 1,
      category: 'FRESH',
      name: 'Fresh Bananas',
      description: 'Fresh organic bananas',
      price: '$2.99',
      image: '/placeholder.svg?height=200&width=300',
      unit: '1 kg',
      quantity: 2,
    }],
    status: "Order Cancelled",
    date: "July 8, 2025, 5:45 PM",
    total: "$19.99",
  },
];

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>(initialOrders);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  const loadMoreOrders = () => {
    const additionalOrders: Order[] = [
      {
        id: 4,
        products: [    {
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
        }],
        status: "Order Cancelled",
        date: "July 8, 2025, 5:45 PM",
        total: "$19.99",
      }
    ];
    setOrders((prevOrders) => [...prevOrders, ...additionalOrders]);
  };

  const viewOrderDetails = (order: Order) => {
    setSelectedOrder(order);
  };

  const goBackToOrders = () => {
    setSelectedOrder(null);
  };

  return (
    <>
      {/* Conditionally Render Content */}
      {selectedOrder ? (
        <OrderDetail
          selectedOrder={selectedOrder}
          goBackToOrders={goBackToOrders}
        />
      ) : (
        <>
          {/* Orders Heading */}
          <h2 className="text-xl font-semibold text-gray-800">Orders</h2>

          {/* Order Cards */}
          <div className="space-y-4 overflow-scroll">
            {orders.map((order) => (
              <div
                key={order.id}
                className="bg-gray-50 shadow rounded-lg p-4 flex flex-col space-y-4"
              >
                {/* Product Images */}
                <div className="flex space-x-4">
                  {order.products.map((product, index) => (
                    <img
                      key={index}
                      src={product.image}
                      alt={`Product ${index + 1}`}
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                  ))}
                </div>

                {/* Order Status */}
                <div className="text-sm text-gray-600 flex items-center">
                  {order.status}{" "}
                  <CheckCircle className="ml-2 text-green-600" />
                </div>

                {/* Order Date and Time */}
                <div className="text-sm text-gray-600">
                  Placed at {order.date}
                </div>

                {/* Bottom Section */}
                <div className="flex justify-between items-center">
                  {/* Amount */}
                  <div className="text-lg font-semibold text-gray-800">
                    Total: {order.total}
                  </div>

                  {/* Buttons */}
                  <div className="flex space-x-4">
                    <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm">
                      Rate Order
                    </button>
                    <button
                      onClick={() => viewOrderDetails(order)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm"
                    >
                      View Order
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Load More Button */}
          <div className="mt-4 flex justify-center">
            <button
              onClick={loadMoreOrders}
              className="bg-gray-800 hover:bg-gray-900 text-white px-6 py-2 rounded text-sm"
            >
              Load More
              <ArrowDownIcon className="inline ml-2 w-4 h-4" />
            </button>
          </div>
        </>
      )}
    </>
  );
}
