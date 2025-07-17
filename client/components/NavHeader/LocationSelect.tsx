"use client";
import { MapPin, ChevronDown } from "lucide-react"
import { useState } from "react";
import LocationModal from "../Location/LocationModal";

export default function LocationSelect() {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const toggleModal = () => {
      setIsModalOpen(!isModalOpen);
    };
    
    return (
        <>
            <div className="flex items-center space-x-2 sm:ml-6 text-gray-600" onClick={toggleModal}>
                <MapPin className="w-4 h-4" />
                <span className="text-sm">Los Angeles, CA</span>
                <ChevronDown className="w-4 h-4" />
            </div>
            {/* Modal */}
            {isModalOpen && <LocationModal onClose={toggleModal} />}
        </>
    )
}