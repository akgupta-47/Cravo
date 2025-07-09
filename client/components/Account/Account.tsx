export default function Account() {
  return (
    <div className="h-screen w-full flex bg-gray-100">
      {/* Card Container */}
      <div className="bg-white shadow-lg rounded-lg w-full max-w-5xl mx-auto flex flex-col h-full">
        <div className="flex-1 bg-gray-50 w-[30%] border-b">
          <div className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              User Info
            </h2>
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
              Dashboard
            </button>
            <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
              Orders
            </button>
            <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
              Settings
            </button>
            <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
              Help
            </button>
            <button className="hover:bg-gray-200 text-black px-8 py-4 w-full text-left">
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
