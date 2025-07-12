'use client';

import { MapPin, Search, X } from 'lucide-react';
import React, { useState, useEffect } from 'react';
import { Input } from '../ui/input';

export default function AddressModal({
  onClose,
  onSave,
  address,
  editMode,
}: {
  onClose: () => void;
  onSave: (address: any) => void;
  address?: any; // Optional address prop for editing
  editMode: boolean; // Determines whether we are editing or creating
}) {
  const [formData, setFormData] = useState({
    name: '',
    houseNumber: '',
    buildingName: '',
    area: '',
    city: '',
    pinCode: '',
    label: '',
    isDefault: false,
    receiverName: '',
    address: '',
    phone: '',
    email: '',
  });
  const [addressSearched, setAddressSearched] = useState(false);
  const [viewForm, setViewForm] = useState(false);

  // Initialize formData based on the address prop if editMode is true
  useEffect(() => {
    if (editMode && address) {
      setFormData(address);
    }
  }, [editMode, address]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]:
        type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    });
  };

  const handleSubmit = () => {
    onSave(formData);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow-lg p-6 w-full max-w-md h-[80%] text-gray-800 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xl font-semibold text-gray-800">
            {!viewForm ? 'Location Information' : 'Add Address Details'}
          </h2>
          <div className="flex items-center justify-center">
            <X onClick={() => onClose()} />
          </div>
        </div>

        <hr className="mb-4" />

        {/* Scrollable content area */}
        <div className="flex-1 overflow-y-auto mb-4">
          {!viewForm && (
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search for products..."
                className="pl-10 pr-4 py-2 w-full rounded text-black border-gray-200 focus:border-green-500 focus:ring-green-500"
              />
            </div>
          )}
          {viewForm && (
            <>
              <h3 className="flex justify-between font-semibold mb-2">
                Saved Location
                <button
                  className="text-sm text-green-600 hover:underline"
                  onClick={() => setViewForm(false)}
                >
                  Change
                </button>
              </h3>
              <div className="flex my-4 bg-green-700 p-4 rounded items-center">
                <MapPin className="w-5 h-5 text-white inline-block mr-2" />
                <div>
                  <h3 className="text-white font-semibold">Sraddha Splendor</h3>
                  <p className="text-white text-sm">
                    1234 Elm Street, Springfield, IL 62704
                  </p>
                </div>
              </div>
              <form className="space-y-4 mt-2 overflow-scroll h-[70%]">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter name"
                  />
                </div>

                {/* House Number */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    House Number
                  </label>
                  <input
                    type="text"
                    name="houseNumber"
                    value={formData.houseNumber}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter house number"
                  />
                </div>

                {/* Building Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Building Name
                  </label>
                  <input
                    type="text"
                    name="buildingName"
                    value={formData.buildingName}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter building name"
                  />
                </div>

                {/* Area */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Area
                  </label>
                  <input
                    type="text"
                    name="area"
                    value={formData.area}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter area"
                  />
                </div>

                {/* City */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    City
                  </label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter city"
                  />
                </div>

                {/* Pin Code */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Pin Code
                  </label>
                  <input
                    type="text"
                    name="pinCode"
                    value={formData.pinCode}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter pin code"
                  />
                </div>

                {/* Label */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Label
                  </label>
                  <select
                    name="label"
                    value={formData.label}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                  >
                    <option value="">Select label</option>
                    <option value="Home">Home</option>
                    <option value="Work">Work</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                {/* Is Default */}
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="isDefault"
                    checked={formData.isDefault}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <label className="text-sm font-medium text-gray-700">
                    Set as Default
                  </label>
                </div>

                {/* Receiver Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Receiver Name
                  </label>
                  <input
                    type="text"
                    name="receiverName"
                    value={formData.receiverName}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter receiver name"
                  />
                </div>

                {/* Phone */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Phone
                  </label>
                  <input
                    type="text"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter phone number"
                  />
                </div>

                {/* Email */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Enter email"
                  />
                </div>

                {/* Buttons */}
                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={handleSubmit}
                    className="px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded w-full"
                  >
                    Save & Continue
                  </button>
                </div>
              </form>
            </>
          )}
        </div>

        {/* Footer with buttons (stays at bottom) */}
        {!viewForm && (
          <div className="mt-auto pt-4 border-t border-gray-200">
            {addressSearched === false ? (
              <>
                <h3 className="text-center font-semibold mb-2">
                  Select a delivery location
                </h3>
                <div className="flex justify-center space-x-4">
                  <button className="px-4 py-2 text-green-900 border border-green-400 rounded hover:bg-green-50 transition-colors">
                    Search Location
                  </button>
                  <button
                    className="px-4 py-2 bg-green-200 hover:bg-green-400 text-green-900 rounded transition-colors"
                    onClick={() => setAddressSearched(true)}
                  >
                    Current Location
                  </button>
                </div>
              </>
            ) : (
              <>
                <h3 className="font-semibold mb-2">Sraddha Splendor</h3>
                <p className="text-sm text-gray-600">
                  1234 Elm Street, Springfield, IL 62704
                </p>
                <button
                  className="w-full mt-3 text-lg py-2 bg-green-200 hover:bg-green-400 text-green-900 rounded"
                  onClick={() => setViewForm(true)}
                >
                  Confirm & Continue
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
    // <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    //   <div className="bg-white rounded shadow-lg p-6 w-full max-w-md h-[80%] text-gray-800">
    //     <div className="flex items-center justify-between mb-3">
    //       <h2 className="text-xl font-semibold text-gray-800">
    //         Location Information
    //       </h2>
    //       <div className="flex items-center justify-center">
    //         <X /> {/* Ensure X is properly centered */}
    //       </div>
    //     </div>
    //     <hr></hr>
    //     <div className="m-2 relative bottom-0">
    //       <h3 className="flex justify-center font-semibold">
    //         Select a delivery location
    //       </h3>
    //       <div className="flex justify-center space-x-4 mt-2">
    //         <button className="px-4 py-2 text-green-900 border border-green-400 rounded">
    //           Search Location
    //         </button>
    //         <button className="px-4 py-2 bg-green-200 hover:bg-green-400 text-green-900 rounded">
    //           Current Location
    //         </button>
    //       </div>
    //     </div>
    //
    //   </div>
    // </div>
  );
}
