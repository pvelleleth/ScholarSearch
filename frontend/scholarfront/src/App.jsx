import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import SearchSection from './components/SearchSection';
import SearchResults from './components/SearchResults';
import ChatInterface from './components/ChatInterface';

function App({ initialTab = 'search' }) {
    const [searchResults, setSearchResults] = useState([]);
    const [activeTab, setActiveTab] = useState(initialTab);
    const { pmid, title } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        setActiveTab(initialTab);
    }, [initialTab]);

    const handleSearch = (results) => {
        setSearchResults(results);
        // Scroll to results smoothly
        setTimeout(() => {
            window.scrollTo({
                top: window.innerHeight * 0.4,
                behavior: 'smooth'
            });
        }, 100);
    };

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        if (tab === 'search') {
            navigate('/');
        }
    };

    return (
        <div className="flex w-full min-h-screen bg-gray-50">
            <Sidebar activeTab={activeTab} onTabChange={handleTabChange} />
            <main className="flex-1 ml-[250px] p-8">
                <div className="max-w-7xl mx-auto">
                    {activeTab === 'search' ? (
                        <>
                            <div className="min-h-[60vh] flex items-center justify-center">
                                <SearchSection onSearch={handleSearch} />
                            </div>
                            <SearchResults results={searchResults} />
                        </>
                    ) : (
                        <div className="min-h-screen">
                            <h2 className="text-2xl font-bold mb-6">Chat with Paper</h2>
                            <p className="text-gray-600 mb-6">
                                PMID: {pmid} • Ask questions about this paper and I'll help you understand it better.
                            </p>
                            <ChatInterface pmid={pmid} title={title} />
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;