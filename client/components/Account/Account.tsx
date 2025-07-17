"use client";
import AccountSidebar from './AccountSidebar';
import OrderList from '../Orders/OrderList';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Addresses from '../Address/Addresses';

export default function Account() {
    const selectedSection = useSelector((state: RootState) => state.accountSidebar.selectedSection);

    const renderContent = () => {
        switch (selectedSection) {
          case 'orders':
            return <OrderList />;
          case 'addresses':
            return <Addresses />;
          case 'profile':
            return <></>;
          case 'payment':
            return <></>;
          case 'help':
            return <></>;
          default:
            return <OrderList />;
        }
      };
    
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
            {renderContent()}
          </div>
        </div>
      </div>
    );
  }
