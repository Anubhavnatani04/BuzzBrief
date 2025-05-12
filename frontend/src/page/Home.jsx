import React, { useEffect, useState } from 'react';
import ArticleCard from '../components/ArticleCard';
import { fetchArticles ,fetchArticlesByDate} from '../lib/api';
import Navbar from '../components/Navbar';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';



function Home() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasMore, setHasMore] = useState(false);
  const [offset, setOffset] = useState(0);
const [sortByDate, setSortByDate] = useState(false);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        setLoading(true);
        setError(null);
        const { articles, hasMore } = await fetchArticles(offset, 10);
        setArticles(prev => offset === 0 ? articles : [...prev, ...articles]);
        setHasMore(hasMore);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadArticles();
  }, [offset]);
  const handleSortByDate = async (date) => {
    setSortByDate(date);
    setOffset(0);
    try {
      setLoading(true);
      setError(null);
  
      // Extract year, month, and day properly
      const year = date.getUTCFullYear();
      const month = String(date.getUTCMonth() + 1).padStart(2, '0');
      const day = String(date.getUTCDate()).padStart(2, '0');
  
      const articles = await fetchArticlesByDate(year, month, day);
      setArticles(articles);
      setHasMore(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-white ">
      <Navbar className="max-w-3xl" />
      <div className="max-w-3xl mx-auto px-6 py-10 ">
        <div className="flex justify-between items-center mb-10 ">
          <h1 className="text-4xl font-extrabold tracking-tight font-serif  ">
            🗞️ Trending News
          </h1>
           
          <DatePicker
  selected={sortByDate}
  onChange={handleSortByDate}
  dateFormat="yyyy-MM-dd"
  className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
  maxDate={new Date()}
  placeholderText="Select a date"
/>


          
        </div>

        {error && (
          <div className="bg-red-500/20 text-red-200 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="flex flex-col gap-1 mb-10">
          {articles.map(article => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>

        {loading && (
          <div className="flex justify-center my-8">
            <div className="animate-spin h-10 w-10 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          </div>
        )}

        {hasMore && !loading && (
          <div className="text-center mt-10">
            <button
              onClick={() => setOffset(prev => prev + 6)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg shadow-md transition transform hover:scale-105"
            >
              Load More Articles
            </button>
          </div>
        )}
      </div>
     
    </div>
    
  );
}

export default Home;