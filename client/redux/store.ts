import { configureStore } from '@reduxjs/toolkit';
import accountSidebarSlice from '../slice/accountSidebarSlice';

const store = configureStore({
  reducer: {
    accountSidebar: accountSidebarSlice,
  },
});

// Infer the `RootState` type from the store itself
export type RootState = ReturnType<typeof store.getState>;

export default store;