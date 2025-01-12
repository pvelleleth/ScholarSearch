import React, { useState } from 'react';

const CitationModal = ({ paper, isOpen, onClose }) => {
  const [selectedFormat, setSelectedFormat] = useState('MLA');

  const generateCitation = (format) => {
    const authors = paper.authors;
    const year = new Date(paper.publication_date).getFullYear();
    const title = paper.title;

    switch (format) {
      case 'MLA':
        const mlaAuthors = authors.length > 0 
          ? authors.length === 1 
            ? `${authors[0]}.` 
            : authors.length === 2 
              ? `${authors[0]}, and ${authors[1]}.`
              : `${authors[0]}, et al.`
          : '';
        return `${mlaAuthors} "${title}." PubMed, National Library of Medicine, ${year}, pubmed.ncbi.nlm.nih.gov/${paper.pmid}.`;

      case 'APA':
        const apaAuthors = authors.length > 0 
          ? authors.length === 1 
            ? `${authors[0]}.` 
            : authors.length === 2 
              ? `${authors[0]} & ${authors[1]}.`
              : `${authors[0]} et al.`
          : '';
        return `${apaAuthors} (${year}). ${title}. PubMed. https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}`;

      case 'Chicago':
        const chicagoAuthors = authors.length > 0 
          ? authors.length === 1 
            ? `${authors[0]}.` 
            : authors.length === 2 
              ? `${authors[0]}, and ${authors[1]}.`
              : `${authors[0]}, et al.`
          : '';
        return `${chicagoAuthors} "${title}." PubMed (${year}). https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}.`;

      default:
        return '';
    }
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      alert('Citation copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy citation:', err);
      alert('Failed to copy citation');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 max-w-2xl w-full mx-4 relative">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <h3 className="text-xl font-semibold mb-4">Citation</h3>

        {/* Citation format selector */}
        <div className="flex space-x-2 mb-4">
          {['MLA', 'APA', 'Chicago'].map((format) => (
            <button
              key={format}
              onClick={() => setSelectedFormat(format)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 ${
                selectedFormat === format
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {format}
            </button>
          ))}
        </div>

        {/* Citation text */}
        <div className="bg-gray-50 p-4 rounded-lg mb-4">
          <p className="text-gray-700 text-sm whitespace-pre-wrap">
            {generateCitation(selectedFormat)}
          </p>
        </div>

        {/* Copy button */}
        <button
          onClick={() => copyToClipboard(generateCitation(selectedFormat))}
          className="w-full bg-blue-500 text-white py-2 rounded-full hover:bg-blue-600 transition-colors duration-200"
        >
          Copy Citation
        </button>
      </div>
    </div>
  );
};

export default CitationModal; 