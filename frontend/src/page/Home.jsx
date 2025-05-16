import React, { useEffect, useState } from 'react';
import ArticleCard from '../components/ArticleCard';
import { fetchArticles, fetchArticlesByDate } from '../lib/api';
import Navbar from '../components/Navbar';

function Home() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasMore, setHasMore] = useState(false);
  const [offset, setOffset] = useState(0);
  const [sortByDate, setSortByDate] = useState(null);

  // Convert Date object to UTC date string (YYYY-MM-DD) for API
  const formatDateToAPI = (date) => {
    if (!date) return null;
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
    const day = String(date.getUTCDate()).padStart(2, '0');
    return { year, month, day };
  };

  // Parse timestamp string to Date object (treat as UTC)
  const parseTimestamp = (timestamp) => {
    if (!timestamp) return null;
    return new Date(timestamp + 'Z');
  };

  // Format date for display in ArticleCard
  const formatDisplayDate = (date) => {
    if (!date) return '';
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: 'UTC'
    });
  };

  // Load articles based on state
  const loadArticles = async () => {
    try {
      setLoading(true);
      setError(null);
      let data;

      if (sortByDate) {
        const { year, month, day } = formatDateToAPI(sortByDate);
        data = await fetchArticlesByDate(year, month, day);
        
        // Filter articles to ensure they match the selected date (UTC)
        const filteredArticles = data.articles?.filter(article => {
          const articleDate = parseTimestamp(article.created_at);
          return (
            articleDate.getUTCFullYear() === year &&
            String(articleDate.getUTCMonth() + 1).padStart(2, '0') === month &&
            String(articleDate.getUTCDate()).padStart(2, '0') === day
          );
        }) || [];
        
        setArticles(filteredArticles);
        setHasMore(false);
      } else {
        data = await fetchArticles(offset, 10);
        // Add parsed date to each article for display
        const articlesWithDates = data.articles?.map(article => ({
          ...article,
          displayDate: formatDisplayDate(parseTimestamp(article.created_at))
        })) || [];
        setArticles((prev) =>
          offset === 0 ? articlesWithDates : [...prev, ...articlesWithDates]
        );
        setHasMore(data.hasMore || false);
      }
    } catch (err) {
      setError(err.message);
      console.error('Error loading articles:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles();
  }, [offset, sortByDate]);

  // When date changes from Navbar
  const handleDateChange = (e) => {
    if (!e.target.value) {
      setSortByDate(null);
      setOffset(0);
      return;
    }
    // Create Date object from input (local time) but treat as UTC date
    const [year, month, day] = e.target.value.split('-').map(Number);
    // Create a Date object in UTC
    const date = new Date(Date.UTC(year, month - 1, day));
    setSortByDate(date);
    setOffset(0);
  };

  return (
    <div className="min-h-screen bg-[rgb(218,200,170)]">
      <Navbar onDateChange={handleDateChange} selectedDate={sortByDate} />
      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10 ">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 pb-4 border-b border-gray-200">
          <h1 className="text-3xl font-bold tracking-tight text-[rgba(11,15,30,0.9)] font-jakarta">
            Trending News
          </h1>
          <div className="mt-4 sm:mt-0 text-sm text-gray-500">
            {sortByDate ? (
              <span>
                Showing articles for {formatDisplayDate(sortByDate)}
              </span>
            ) : (
              <span>Showing latest articles</span>
            )}
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
            <p>Error loading articles: {error}</p>
            <button
              onClick={loadArticles}
              className="mt-2 text-sm text-red-600 hover:text-red-800 font-medium"
            >
              Retry
            </button>
          </div>
        )}

        {articles.length === 0 && !loading ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              {sortByDate
                ? 'No articles found for this date'
                : 'No articles available'}
            </p>
          </div>
        ) : (
          <div className="space-y-6 mb-10">
            {articles.map((article) => (
              <ArticleCard 
                key={article.id || article.url} 
                article={article}
                displayDate={article.displayDate}
              />
            ))}
          </div>
        )}

        {loading && (
          <div className="flex justify-center my-8">
            <div className="animate-spin h-10 w-10 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          </div>
        )}

        {hasMore && !loading && !sortByDate && (
          <div className="text-center mt-8">
            <button
              onClick={() => setOffset((prev) => prev + 6)}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-black bg-[#e4d3bf]  focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50"
            >
              Load More
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;