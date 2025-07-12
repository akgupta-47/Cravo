import { createSlice } from '@reduxjs/toolkit';

const sidebarSlice = createSlice({
  name: 'sidebar',
  initialState: {
    selectedSection: 'orders', // Default section
  },
  reducers: {
    setSelectedSection(state, action) {
      state.selectedSection = action.payload;
    },
  },
});

export const { setSelectedSection } = sidebarSlice.actions;
export default sidebarSlice.reducer;