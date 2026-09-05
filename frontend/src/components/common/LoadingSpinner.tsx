import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex justify-center items-center py-4">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2c7a7b]"></div>
    </div>
  );
};

export default LoadingSpinner;
