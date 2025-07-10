import AccountSidebar from './AccountSidebar';
import OrderList from '../Orders/OrderList';

export default function Account() {
    return (
      <div className="h-screen w-full flex bg-gray-100">
        {/* Card Container */}
        <div className="bg-white shadow-lg rounded-lg w-full max-w-5xl mx-auto flex h-full flex-row">
          {/* Left Section (30%) */}
          <div className="w-1/3 bg-gray-50 border-r flex flex-col">
            <AccountSidebar />
          </div>
  
          {/* Right Section (70%) */}
          <div className="w-2/3 p-6 flex flex-col space-y-6">
            <OrderList />
          </div>
        </div>
      </div>
    );
  }
