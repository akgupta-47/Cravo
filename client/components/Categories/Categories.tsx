export default function Categories() {
    const categories = [
        { name: "All", icon: "⏰", color: "text-green-600", active: true },
        { name: "Cafe", icon: "☕", color: "text-orange-600" },
        { name: "Home", icon: "🏠", color: "text-blue-600" },
        { name: "Toys", icon: "🧸", color: "text-green-600" },
        { name: "Fresh", icon: "🥬", color: "text-green-600" },
        { name: "Electronics", icon: "📱", color: "text-gray-600" },
        { name: "Beauty", icon: "✨", color: "text-pink-600" },
        { name: "Fashion", icon: "👕", color: "text-green-600" },
        { name: "Deal Zone", icon: "🏷️", color: "text-red-600" },
        { name: "Baby Store", icon: "👶", color: "text-purple-600" },
    ]

    return (
        <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-4 sm:grid-cols-4 lg:grid-cols-10 gap-4 py-4">
            {categories.map((category, index) => (
              <div
                key={index}
                className={`flex flex-col items-center space-y-2 min-w-0 cursor-pointer group ${
                  category.active ? "text-yellow-600" : "text-gray-600 hover:text-green-600"
                }`}
              >
                <div
                  className={`text-2xl ${category.active ? "bg-green-100" : "group-hover:bg-gray-100"} w-12 h-12 rounded-full flex items-center justify-center`}
                >
                  {category.icon}
                </div>
                <span className="text-sm font-medium whitespace-nowrap">{category.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
}