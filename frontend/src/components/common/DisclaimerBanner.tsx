import React from 'react';
import { AlertCircle } from 'lucide-react';

const DisclaimerBanner: React.FC = () => {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 bg-[#fffbeb] border-t border-[#fde68a] p-2 text-center text-xs text-[#92400e] flex justify-center items-center shadow-[0_-2px_10px_rgba(0,0,0,0.05)]">
      <AlertCircle className="w-4 h-4 mr-2 inline-block shrink-0" />
      <span className="font-medium">Disclaimer:</span>
      <span className="ml-1">This information is for informational purposes only and does not constitute legal advice. Always consult a qualified legal professional.</span>
    </div>
  );
};

export default DisclaimerBanner;
