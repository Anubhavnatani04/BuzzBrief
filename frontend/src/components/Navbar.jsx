import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Navbar() {
  return (
    <nav className=" relative flex w-full justify-center items-center mx-auto max-w-3xl border-b border-gray-300 p-4 ">
      <div className="flex justify-center items-center">
        <Link to="/">
          <img
            src={logo}
            className="h-18 w-auto sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6 mx-auto"
            alt="Logo"
          />
        </Link>
      </div>
    </nav>
  );
}
