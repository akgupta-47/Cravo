'use client';
import { ChevronRight } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function CartModal({ onClose }: { onClose: () => void }) {
  const [isVisible, setIsVisible] = useState(false);

  // Dummy items for the cart
  const cartItems = [
    {
      id: 1,
      name: 'Fresh Bananas',
      image: '/placeholder.svg',
      description: 'Fresh organic bananas',
      unit: '1 kg',
      quantity: 2,
      price: '$2.99',
    },
    {
      id: 2,
      name: 'Organic Apples',
      image: '/placeholder.svg',
      description: 'Fresh organic bananas',
      unit: '1 pc',
      quantity: 1,
      price: '$4.99',
    },
    {
      id: 3,
      name: 'Fresh Bread',
      image: '/placeholder.svg',
      description: 'Fresh organic bananas',
      unit: '400 gm',
      quantity: 3,
      price: '$3.49',
    },
  ];

  useEffect(() => {
    // Trigger the slide-in animation when the modal is mounted
    setIsVisible(true);
    return () => {
      // Trigger the slide-out animation when the modal is unmounted
      setIsVisible(false);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-end z-50">
      <div
        className={`bg-white rounded-lg shadow-lg h-full p-6 relative transform transition-transform duration-300 ${
          isVisible ? 'translate-x-0' : 'translate-x-full'
        } lg:w-[40%] md:w-[50%] sm:w-[80%] w-full`}
      >
        {/* Modal Header */}
        <div className="flex items-center mb-4">
          <ChevronRight
            onClick={() => {
              setIsVisible(false); // Trigger slide-out animation
              setTimeout(onClose, 300); // Wait for animation to finish before closing
            }}
            className="w-5 h-5 text-gray-600 mr-2"
          />
          <h2 className="text-lg font-semibold text-gray-800">
            Your Shopping Cart
          </h2>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          {/* Items Header */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-800">
              Items ({cartItems.length})
            </h3>
          </div>

          {/* Items List */}
          <div className="space-y-4">
            {cartItems.map((item) => (
              <div
                key={item.id}
                className="flex items-center space-x-4 rounded-lg p-4"
              >
                {/* Item Image */}
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-16 h-16 object-cover rounded-lg"
                />

                {/* Item Details */}
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-gray-800">
                    {item.name}
                  </h4>
                  <h4 className="text-sm text-gray-800">{item.description}</h4>
                  <h4 className="text-sm font-semibold text-gray-400">
                    {item.unit}
                  </h4>
                </div>

                <div className="flex items-center space-x-2 mt-2">
                  {/* Quantity Updater */}
                  <button className="px-2 py-1 bg-green-600 rounded text-sm">
                    -
                  </button>
                  <span className="text-sm text-gray-950">{item.quantity}</span>
                  <button className="px-2 py-1 bg-green-600 rounded text-sm">
                    +
                  </button>
                </div>

                {/* Item Price */}
                <div>
                  <div className="text-sm font-semibold text-gray-800">
                    {item.price}
                  </div>
                  <div className="text-sm text-gray-400 line-through">
                    {'$8000'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
