import Header from "@/components/NavHeader/Header"
import Categories from "@/components/Categories/Categories"
import ProductList from "@/components/ProductList/ProductList"


export default function Page() {

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Categories */}
      <Categories />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ProductList />
      </main>
    </div>
  )
}
