import Header from "@/components/NavHeader/Header"
import Categories from "@/components/Categories/Categories"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"

export default function Page() {

  const products = [
    {
      id: 1,
      category: "FRESH",
      name: "Fresh Bananas",
      description: "Fresh organic bananas",
      price: "$2.99",
      image: "/placeholder.svg?height=200&width=300",
      categoryColor: "bg-blue-100 text-blue-600",
    },
    {
      id: 2,
      category: "FRESH",
      name: "Organic Apples",
      description: "Crisp organic red apples",
      price: "$4.99",
      image: "/placeholder.svg?height=200&width=300",
      categoryColor: "bg-blue-100 text-blue-600",
    },
    {
      id: 3,
      category: "HOME",
      name: "Fresh Bread",
      description: "Freshly baked artisan bread",
      price: "$3.49",
      image: "/placeholder.svg?height=200&width=300",
      categoryColor: "bg-purple-100 text-purple-600",
    },
    {
      id: 4,
      category: "FRESH",
      name: "Organic Milk",
      description: "Fresh organic whole milk",
      price: "$5.99",
      image: "/placeholder.svg?height=200&width=300",
      categoryColor: "bg-blue-100 text-blue-600",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Categories */}
      <Categories />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <p className="text-gray-600 text-lg">Favourite items from your hometown vendors</p>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <div key={product.id} className="bg-white rounded-xl shadow-sm border hover:shadow-md transition-shadow">
              <div className="aspect-square relative overflow-hidden rounded-t-xl">
                <Image src={product.image || "/placeholder.svg"} alt={product.name} fill className="object-cover" />
              </div>
              <div className="p-4">
                <Badge className={`${product.categoryColor} text-xs font-medium mb-2`}>{product.category}</Badge>
                <h3 className="font-semibold text-gray-900 mb-1">{product.name}</h3>
                <p className="text-sm text-gray-600 mb-3">{product.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-gray-900">{product.price}</span>
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">Add to Cart</Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
