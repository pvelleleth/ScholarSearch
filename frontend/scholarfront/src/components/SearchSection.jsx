import React, { useState } from "react";
import { FiSearch } from "react-icons/fi";

const SearchSection = ({ onSearch }) => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (query.trim() === "") return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/search?query=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error('Search failed. Please try again.');
      }
      
      const results = await response.json();
      onSearch(results);
    } catch (err) {
      setError(err.message);
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Title */}
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Search PubMed</h1>
      
      {/* Search Bar */}
      <div className="flex items-center w-full bg-white shadow-lg rounded-full px-6 py-3">
        <FiSearch className="text-gray-500 text-xl mr-3" />
        <input
          type="text"
          placeholder="Search for research papers..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          className="flex-1 text-gray-700 focus:outline-none text-lg"
          disabled={isLoading}
        />
        <button
          onClick={handleSearch}
          disabled={isLoading}
          className={`${
            isLoading ? 'bg-blue-400' : 'bg-blue-500 hover:bg-blue-600'
          } text-white px-6 py-2 rounded-full transition font-medium`}
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <p className="text-red-500 text-sm mt-4 text-center">
          {error}
        </p>
      )}

      {/* Helper Text */}
      <p className="text-sm text-gray-500 mt-4 text-center">
        Use keywords or phrases to find relevant research papers.
      </p>
    </div>
  );
};

export default SearchSection;