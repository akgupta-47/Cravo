import { MapPin, ChevronDown } from "lucide-react"

export default function LocationSelect() {
    return (
        <div className="flex items-center space-x-2 sm:ml-6 text-gray-600">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">Los Angeles, CA</span>
              <ChevronDown className="w-4 h-4" />
        </div>
    )
}