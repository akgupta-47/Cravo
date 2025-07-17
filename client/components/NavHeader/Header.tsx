'use client';
import { ShoppingCart, User } from 'lucide-react';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import LocationSelect from './LocationSelect';
import SearchBar from './SearchBar';
import { useState } from 'react';
import CartModal from '../Cart/CartModel';

export default function Header() {
  const [isCartModalOpen, setIsCartModalOpen] = useState(false);

  const toggleCartModal = () => {
    setIsCartModalOpen(!isCartModalOpen);
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* First Row */}
          <div className="flex items-center w-full h-16">
            {/* Logo (hidden on small screens) */}
            <Link href="/" passHref legacyBehavior>
              <div className="flex items-center space-x-3 hidden sm:flex">
                <div className="w-10 h-10 bg-green-600 rounded-xl flex items-center justify-center">
                  <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                    <ShoppingCart className="w-6 h-6 text-white" />
                  </div>
                </div>
                <span className="text-xl font-bold text-green-600">Cravo</span>
              </div>
            </Link>

            {/* Location */}
            <LocationSelect />

            <div className="hidden sm:hidden lg:flex w-80 mx-auto">
              <SearchBar />
            </div>

            {/* Right side icons */}
            <div className="flex items-center ml-auto space-x-4">
              <div className="relative">
                <ShoppingCart
                  className="w-6 h-6 text-gray-600"
                  onClick={toggleCartModal}
                />
                <Badge className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center p-0">
                  0
                </Badge>
              </div>
              <Link href="/account" passHref legacyBehavior>
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center cursor-pointer">
                  <User className="w-5 h-5 text-gray-200" />
                </div>
              </Link>
            </div>
          </div>

          {/* Second Row (Search Bar for phone mode) */}
          <div className="mt-2 mb-4 sm:hidden">
            <SearchBar />
          </div>
        </div>
      </header>

      {isCartModalOpen && <CartModal onClose={toggleCartModal} />}
    </>
  );
}
