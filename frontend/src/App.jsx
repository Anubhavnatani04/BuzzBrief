import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./page/Home" // <-- Make sure this matches your actual file path
import ArticleDetails from "./page/ArticleDetails" // <-- Make sure this matches your actual file path
import "./index.css"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/article/:id" element={<ArticleDetails />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
