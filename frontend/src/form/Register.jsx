import axios from "axios";
import React, { useEffect } from "react";
import { useState } from "react";
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Register(props) {
  const navigate = useNavigate();
  const [formRegister, setFormRegister] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: ""
  });


  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setFormRegister({ ...formRegister, username: event.target.value });
        break;
      case "email":
        // email validation
        const email_validation = /\S+@\S+\.\S+/;
        if (email_validation.test(event.target.value)) {
          setFormRegister({ ...formRegister, email: event.target.value });
        }
        break;
      case "password":
        setFormRegister({ ...formRegister, password: event.target.value });
        break;
      case "confirm_password":
        setFormRegister({ ...formRegister, confirm_password: event.target.value });
        break;
    }
  };

  // submit handler
  const onSubmitHandler = async (event) => {
    event.preventDefault();
    // console.log("formData", formRegister);

    // call POST API for submit register form data
    
    if (formRegister['password'] !== formRegister['confirm_password']) {
      toast.error("パスワードが確認用パスワードと等しくない");
    } else {

      await axios
        .post("http://49.212.185.58:8080/register", formRegister)
        .then((response) => {
          // redirect to sign page
          navigate("/login");
          console.log("response: ", response);
          // add susscess toast notify
          toast.success(response.data.detail);

          setTimeout(() => {
            window.location.reload();
          }, 1000);
        })
        .catch((error) => {
          console.log("error: ", error);
          // add error toast notify
          toast.error(error.response.data.detail);
        });
    }
  };
  return (
    <React.Fragment>
      <h1 className="text-3xl font-bold text-center mb-4 cursor-pointer">
        新 規 登 録
      </h1>
      {/* <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 -tracking-wide cursor-pointer mx-auto">
            Welcome
        </p> */}
      <form onSubmit={onSubmitHandler}>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="ユーザー名"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("username", event);
            }}
          />
          <input
            type="email"
            placeholder="Eメール"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("email", event);
            }}
          />
          <input
            type="password"
            placeholder="パスワード"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("password", event);
            }}
          />
          <input
            type="password"
            placeholder="パスワードを認証する"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            onChange={(event) => {
              onChangeForm("confirm_password", event);
            }}
          />
        </div>
        <div className="text-center mt-6">
          <button
            type="submit"
            className="py-3 w-64 text-xl text-white bg-blue-400 rounded-2xl hover:bg-blue-300 active:bg-blue-500 outline-none"
          >
            サインアップ
          </button>
          <p>
            すでにアカウントをお持ちですか?{" "}
            <Link
              to={"/login"}
              onClick={() => {
                props.setPage("login");
              }}
            >
              <span className="underline cursor-pointer">サインイン</span>
            </Link>
          </p>
        </div>
      </form>
    </React.Fragment>
  );
}
