import React from 'react';

interface ConfidenceBadgeProps {
  level: 'HIGH' | 'MEDIUM' | 'LOW';
  score?: number;
}

const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ level, score }) => {
  const config = {
    HIGH: { color: 'bg-green-100 text-green-800 border-green-200', dot: 'bg-green-500', text: 'High Confidence' },
    MEDIUM: { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', dot: 'bg-yellow-500', text: 'Medium Confidence' },
    LOW: { color: 'bg-red-100 text-red-800 border-red-200', dot: 'bg-red-500', text: 'Low Confidence' }
  };

  const current = config[level] || config.MEDIUM;

  return (
    <div 
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${current.color}`}
      title={score ? `Confidence score: ${(score * 100).toFixed(1)}%` : undefined}
    >
      <span className={`w-2 h-2 mr-1.5 rounded-full ${current.dot}`}></span>
      {current.text}
    </div>
  );
};

export default ConfidenceBadge;
