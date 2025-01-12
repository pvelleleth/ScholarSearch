import React, { useState } from 'react';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';
import CitationModal from './CitationModal';

const SearchResults = ({ results }) => {
  const [selectedPaper, setSelectedPaper] = useState(null);
  const navigate = useNavigate();

  if (!results || results.length === 0) return null;

  const handleChatClick = (pmid) => {
    navigate(`/chat/${pmid}`);
  };

  return (
    <div className="w-full mt-8">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-2">
        {results.map((paper) => (
          <div
            key={paper.pmid}
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden border border-gray-100"
          >
            <div className="p-6">
              {/* Title */}
              <h2 className="text-xl font-semibold text-gray-800 mb-2 line-clamp-2 hover:line-clamp-none">
                {paper.title}
              </h2>

              {/* Authors */}
              <div className="mb-3">
                <p className="text-sm text-gray-600 line-clamp-1">
                  {paper.authors.join(', ')}
                </p>
              </div>

              {/* Abstract */}
              <p className="text-gray-600 mb-4 line-clamp-3 hover:line-clamp-none text-sm">
                {paper.abstract}
              </p>

              {/* Footer */}
              <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                <div className="text-sm text-gray-500">
                  {format(new Date(paper.publication_date), 'MMM d, yyyy')}
                </div>
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-blue-600 font-medium">
                    Score: {paper.relevance_score.toFixed(2)}
                  </span>
                  <button
                    onClick={() => setSelectedPaper(paper)}
                    className="text-sm text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-full transition-colors duration-300"
                  >
                    Cite
                  </button>
                  <button
                    onClick={() => handleChatClick(paper.pmid)}
                    className="text-sm text-purple-600 hover:text-purple-700 bg-purple-100 hover:bg-purple-200 px-3 py-2 rounded-full transition-colors duration-300"
                  >
                    Chat
                  </button>
                  <a
                    href={`https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-white bg-blue-500 hover:bg-blue-600 px-3 py-2 rounded-full transition-colors duration-300"
                  >
                    View
                  </a>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Citation Modal */}
      <CitationModal
        paper={selectedPaper}
        isOpen={selectedPaper !== null}
        onClose={() => setSelectedPaper(null)}
      />
    </div>
  );
};

export default SearchResults; 