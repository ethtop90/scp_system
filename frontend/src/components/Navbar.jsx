import React, { useContext } from "react";
import { Link } from "react-router-dom";

const Navbar = ({ isLoggedIn, onLogout }) => {
  //   const userInfo = useContext(UserInfoContext);
  const username = localStorage.getItem("user");
  return (
    <nav className="bg-gray-800 p-4 w-full sticky top-0 z-1000">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-lg font-bold">
          不動産管理
        </Link>

        {isLoggedIn ? (
          <div className="flex items-center space-x-4">
            <span className="text-white">{username}</span>
            <button onClick={onLogout} className="text-white">
              ログアウト
            </button>
          </div>
        ) : (
          <Link to="/login" className="text-white">
            ログイン
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
