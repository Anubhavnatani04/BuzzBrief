import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function ArticleDetail() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");
  const [showSummary, setShowSummary] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/article/${id}`);
        const data = await response.json();

        if (response.ok) {
          setArticle(data);
        } else {
          setError(data.error || "Failed to fetch article");
        }
      } catch (err) {
        setError("Error fetching article");
        console.error(err);
      }
    };

    if (id) {
      fetchArticle();
    }
  }, [id]);

  const fetchSummary = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/article/${id}/summary`);
      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary);
        setShowSummary(true);
      } else {
        setError(data.error || "Failed to fetch summary");
      }
    } catch (err) {
      setError("Error fetching summary");
      console.error(err);
    }
  };

  if (error) return <div className="text-red-500 p-4">{error}</div>;
  if (!article) return <div className="p-4 text-white">Loading...</div>;

  return (
    <>
      <Navbar />
      <div className="min-h-screen py-10 px-4 text-white">
        <div className="max-w-3xl mx-auto bg-white/30  text-gray-900  backdrop-blur-md border border-white/20 rounded-lg shadow-lg p-6">
          <button
            onClick={() => navigate("/")}
            className="mb-4 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded"
          >
            ← Back

          </button>

          <h1 className="text-3xl font-bold mb-2">{article.headline}</h1>
          <div className="text-sm text-gray-500 mb-4">
            {article.source} ·{" "}
            {new Date(article.created_at).toLocaleDateString(undefined, {
              year: "numeric",
              month: "short",
              day: "numeric",
            })}


          </div>

          {article.image_url && (
            <img
              src={article.image_url}
              alt={article.headline}
              className="mb-4 w-full h-64 object-cover rounded"
            />


)}

          {showSummary ? (
            <>
              <div className="bg-slate-100 p-4 rounded mb-4">
                <h2 className="text-lg font-semibold text-slate-800 mb-2">Summary:</h2>
                <p className="whitespace-pre-wrap break-words text-slate-700">
                  {summary}
                </p>
              </div>
              <button
                onClick={() => setShowSummary(false)}
                className="mb-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded shadow"
              >
                Close Summary
              </button>
            </>
          ) : (
            <button
              onClick={fetchSummary}
              className="mb-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded shadow"
            >
              Get Summary
            </button>


)}

          {!showSummary && (
            <p className="text-gray-800 leading-relaxed mb-6">{article.content}</p>
          )}
        </div>
      </div>

    </>
  );
}
