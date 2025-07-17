import Header from "@/components/NavHeader/Header"
import Account from "@/components/Account/Account"


export default function Page() {

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      <main className="py-8">
        <Account />
      </main>
    </div>
  )
}
