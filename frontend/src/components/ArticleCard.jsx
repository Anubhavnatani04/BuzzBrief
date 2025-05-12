import React from "react";
import { Link } from "react-router-dom";

export default function ArticleCard({ article }) {
  return (
    <Link to={`/article/${article.id}`} className="block mb-4">
      <div className="flex flex-row-reverse bg-white">
        
        {article.image_url && (
          <img
            src={article.image_url}
            alt={article.headline}
            className="w-36 h-24 object-cover rounded-lg flex-shrink-0"
          />
        )}
        
        <div className="p-4 flex flex-col justify-between text-gray-900 w-full">
          <h2 className="text-md font-bold font-s ">
            {article.headline} 
          </h2>
          <h3 className="text-md text-gray-700 font-semibold">
            {article.description}
          </h3>

          
          
          <div className="text-xs text-gray-600 mt-2">
            {article.source} &middot;{" "}
            {new Date(article.created_at).toLocaleDateString()}
          </div>
        </div>
      </div>
    </Link>
  );
}
