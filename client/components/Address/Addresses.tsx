'use client';

import React, { useState } from 'react';
import { Home, MapPin, Edit2Icon, TrashIcon } from 'lucide-react';
import AddressModal from './AddressModal';

export default function Addresses() {
  const [addresses, setAddresses] = useState([
    {
      name: "John Doe",
      houseNumber: "123",
      buildingName: "Springfield Plaza",
      area: "Downtown",
      city: "Springfield",
      pinCode: "62701",
      label: "Home",
      isDefault: true,
      receiverName: "John Doe",
      address: "BLOCK-2, SRADDHA SPLENDOR, R Narayanapura, 11/1, Ramagondanahalli Borewell Rd, Palm Meado",
      phone: "+1 234 567 890",
      email: "",
    },
    {
      name: "Jane Smith",
      houseNumber: "456",
      buildingName: "Maple Apartments",
      area: "Uptown",
      city: "Chicago",
      pinCode: "60601",
      label: "Work",
      isDefault: false,
      receiverName: "Jane Smith",
      address: "456 Maple St, Chicago, IL 60601",
      phone: "+1 987 654 321",
      email: "jane.smith@example.com",
    },
    {
      name: "Michael Johnson",
      houseNumber: "789",
      buildingName: "Oakwood Villas",
      area: "Suburbs",
      city: "Los Angeles",
      pinCode: "90001",
      label: "Vacation Home",
      isDefault: false,
      receiverName: "Michael Johnson",
      address: "789 Oakwood Dr, Los Angeles, CA 90001",
      phone: "+1 555 123 456",
      email: "michael.johnson@example.com",
    },
    {
      name: "Emily Davis",
      houseNumber: "321",
      buildingName: "Pinewood Estates",
      area: "Midtown",
      city: "New York",
      pinCode: "10001",
      label: "Other",
      isDefault: false,
      receiverName: "Emily Davis",
      address: "321 Pinewood Ave, New York, NY 10001",
      phone: "+1 444 567 890",
      email: "emily.davis@example.com",
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentAddress, setCurrentAddress] = useState(null);

  const handleAddAddress = () => {
    setEditMode(false);
    setCurrentAddress(null);
    setIsModalOpen(true);
  };

  const handleEditAddress = (address: any) => {
    setEditMode(true);
    setCurrentAddress(address);
    setIsModalOpen(true);
  };

  const handleSaveAddress = (newAddress: any) => {
    if (editMode) {
      // Update existing address
      setAddresses((prevAddresses) =>
        prevAddresses.map((addr) =>
          addr === currentAddress ? newAddress : addr
        )
      );
    } else {
      // Add new address
      setAddresses((prevAddresses) => [...prevAddresses, newAddress]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className='space-y-0'>
    
    <div className="space-y-4 overflow-scroll">
      <div className="p-2 flex items-center text-gray-800 justify-between">
        <h1 className="font-semibold text-gray-800 flex items-center">
          All Addresses <Home className="ml-2 text-green-600" />
        </h1>
        <button
          onClick={handleAddAddress}
          className="px-4 py-2 w-[30%] bg-green-200 hover:bg-green-400 text-green-900 rounded"
        >
          Add Address
        </button>
      </div>
      <hr />
      <div className="p-3 flex flex-col space-y-4 text-gray-900">
        {addresses.map((address, index) => (
          <div key={index}>
            <div className="flex items-center justify-between cursor-pointer">
              <MapPin className="w-4 h-4" />
              <div className="flex-1 ml-2 p-2">
                <h3>{address.name}</h3>
                <p>
                  {address.houseNumber + " " + address.address + " " + address.area}
                </p>
              </div>
              <Edit2Icon
                className="w-4 h-4 mx-3 cursor-pointer"
                onClick={() => handleEditAddress(address)}
              />
              <TrashIcon className="w-4 h-4 mx-3 cursor-pointer" />
            </div>
            <hr />
          </div>
        ))}
      </div>

    </div>
      {/* Address Modal */}
      {isModalOpen && (
        <AddressModal
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveAddress}
          address={currentAddress}
          editMode={editMode}
        />
      )}
    </div>
  );
}
