import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"

export default function SearchBar() {
    return (
        <div className="flex-1 max-w-lg mx-auto">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  type="text"
                  placeholder="Search for products..."
                  className="pl-10 pr-4 py-2 w-full rounded-full text-black border-gray-200 focus:border-green-500 focus:ring-green-500"
                />
              </div>
        </div>
    )
}