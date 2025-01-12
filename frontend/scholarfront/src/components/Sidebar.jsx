import React from 'react';
import { FiSearch, FiMessageSquare } from 'react-icons/fi';

const Sidebar = ({ activeTab = 'search', onTabChange }) => {
  const tabs = [
    {
      id: 'search',
      label: 'Search',
      icon: FiSearch
    },
    {
      id: 'chat',
      label: 'Chat Doc',
      icon: FiMessageSquare
    }
  ];

  return (
    <div className="fixed left-0 top-0 h-screen w-[250px] bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-800">PubMed AI</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${
                activeTab === tab.id
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Icon className="text-xl" />
              <span className="font-medium">{tab.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-sm text-gray-500">© 2024 PubMed AI</p>
      </div>
    </div>
  );
};

export default Sidebar;