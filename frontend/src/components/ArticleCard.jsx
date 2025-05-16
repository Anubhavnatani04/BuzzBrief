import React from "react";
import { Link } from "react-router-dom";

export default function ArticleCard({ article }) {
  return (
<Link to={`/article/${article.id}`} className="block mb-4 ">
  <div className="flex justify-between  bg-[#e4d3bf]  border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
    <div className="p-4 flex flex-col justify-between text-[#7b78cf] w-full">
      <h2 className="text-lg font-bold text-gray-900 text-justify">{article.headline}</h2>
      <h3 className="text-md text-gray-700 font-semibold">
        {article.description}
      </h3>
      <div className="text-xs text-gray-600 mt-2">
        {article.source} &middot;{" "}
        {new Date(article.created_at).toLocaleDateString()}
      </div>
    </div>

    {article.image_url && (
      <img
        src={article.image_url}
        alt={article.headline}
        className="w-36 h-24 object-cover rounded-lg m-4"
      />
    )}
  </div>
</Link>


  );
}
