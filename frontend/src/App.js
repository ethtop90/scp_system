import React, { useContext, useEffect, useState } from "react";
import { Route, Routes, useNavigate, BrowserRouter } from "react-router-dom";

import "./App.css";
import Forgot from "./form/Forgot";
import Home from "./form/Home";
import Login from "./form/Login";
import Register from "./form/Register";
import ScpSetting from "./form/scpSetting/ScpSetting";
import { createContext } from "react";
import Navbar from "./components/Navbar";
import { toast } from "react-toastify";
import Main from "./form/Main";
import PrintSetting from "./form/print/PrintSetting";
import ScpSettingModal from "./components/ScpSettingModal";
import AutoSetting from "./form/print/AutoSetting";

const UserInfoContext = createContext();

export { UserInfoContext };

function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState();
  const [userInfo, setUserInfo] = useState({}); // Initialize with an empty object
  const navigate = useNavigate();

  // set auth token from localStorage if available
  useEffect(() => {
    const auth = localStorage.getItem("auth_token");

    setToken(auth);
    console.log(localStorage);
    const storedUserInfo = JSON.parse(localStorage.getItem("username")) || {};
    setUserInfo(storedUserInfo);
  }, [token]);

  const choosePage = () => {
    if (page === "login") {
      return <Login setPage={setPage} />;
    }
    if (page === "forgot") {
      return <Forgot setPage={setPage} />;
    }
    if (page === "register") {
      return <Register setPage={setPage} />;
    }
  };

  const onClickHandler = (event) => {
    event.preventDefault();
    // remove token from local storage
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_token_type");

    // tostify
    toast("Logged Out.", {
      position: "top-right",
      autoClose: 8080,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

    // reload page
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  };

  // render page wrt token home/login page
  const pages = () => {
    if (token == null) {
      return (
        <>
          <Navbar isLoggedIn={false} onLogout={onClickHandler} />
          <div className="min-h-screen bg-blue-400 flex justify-center items-center">
            <div className="py-12 px-12 bg-white rounded-2xl shadow-xl z-20">
              {/* <Login/> */}
              {/* <Register/> */}
              {/* <Forgot/> */}
              {choosePage()}
            </div>
          </div>
        </>
      );
    } else {
      return (
        <>
          <Navbar isLoggedIn={true} onLogout={onClickHandler} />
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/login" element={<Main />} />
            <Route path="/register" element={<Main />} />
            <Route path="/scp-settings" element={<ScpSetting />} />
            <Route path="/print-setting" element={<PrintSetting />} />
            <Route path="/scp-settings/add" element={<ScpSettingModal  method={'add'}/>} />
            <Route path="/scp-settings/update" element={<ScpSettingModal method={'update'} />}  />
            <Route path="/print-setting/auto-setting" element={<AutoSetting />} />

          </Routes>
        </>
      );
    }
  };
  return (
    <UserInfoContext.Provider value={userInfo}>
      <React.Fragment>{pages()}</React.Fragment>
    </UserInfoContext.Provider>
  );
}

export default App;
