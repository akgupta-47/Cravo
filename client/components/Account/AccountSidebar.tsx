import {
    CreditCard,
    HelpCircle,
    Home,
    LogOut,
    ShoppingBag,
    User,
  } from 'lucide-react';
  
  export default function AccountSidebar() {
    return (
          <>
            <div className="p-6">
              <div className="flex items-center space-x-6">
                {/* User Photo */}
                <div className="w-20 h-20 bg-gray-300 rounded-full"></div>
  
                {/* User Details */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">
                    John Doe
                  </h3>
                  <p className="text-sm text-gray-600">john.doe@example.com</p>
                  <p className="text-sm text-gray-600">+1 234 567 890</p>
                </div>
              </div>
            </div>
  
            <div className="flex-2 flex flex-col space-y-4 py-4">
              {/* Sidebar Buttons */}
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <ShoppingBag className="inline mr-2" />
                Orders
              </button>
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <Home className="inline mr-2" />
                Addresses
              </button>
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <User className="inline mr-2" />
                Profile
              </button>
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <CreditCard className="inline mr-2" />
                Payment
              </button>
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <HelpCircle className="inline mr-2" />
                Help
              </button>
              <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
                <LogOut className="inline mr-2" />
                Logout
              </button>
            </div>
          </>
    );
  }
  