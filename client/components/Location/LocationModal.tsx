"use client";
import { useState } from "react";
import { X, MapPin, Search } from "lucide-react";
import { Input } from "@/components/ui/input";

export default function LocationModal({ onClose }: { onClose: () => void }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");

    // Dummy addresses
    const addresses = [
        "123 Main Street, Los Angeles, CA",
        "456 Elm Street, San Francisco, CA",
        "789 Oak Avenue, San Diego, CA",
        "101 Pine Lane, Sacramento, CA",
    ];

  // Debounce logic
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);

    clearTimeout((window as any).debounceTimeout);
    (window as any).debounceTimeout = setTimeout(() => {
      setDebouncedSearchTerm(value);
    }, 300); // 300ms debounce delay
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
        {/* Close Button */}
        <button
          className="absolute top-4 right-4 text-gray-600 hover:text-gray-800"
          onClick={onClose}
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Content */}
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Select Your Location
        </h2>

        {/* Search Bar */}
        <div className="relative mb-4">
          <Input
            type="text"
            placeholder="Search for a location..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="pl-10 pr-4 py-2 w-full rounded-lg text-gray-950 border-gray-300 focus:border-green-500 focus:ring-green-500"
          />
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        </div>

        {/* Address List */}
        {addresses.length > 0 && (
          <div className="overflow-y-auto max-h-40 mb-4 border rounded-lg p-2">
            {addresses.map((address, index) => (
              <div
                key={index}
                className="flex items-center text-sm text-gray-700 py-2 px-3 hover:bg-gray-100 rounded cursor-pointer"
              >
                <MapPin className="w-4 h-4 text-gray-400 mr-2" />
                <span>{address}</span>
              </div>
            ))}
          </div>
        )}

        {/* Current Location */}
        <button
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg w-full"
          onClick={() => alert("Current location selected")}
        >
          Use Current Location
        </button>
      </div>
    </div>
  );
}