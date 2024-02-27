import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios, {isCancel, AxiosError} from 'axios'
import {toast} from "react-toastify"

export default function Login(props) {

  const[loginForm, setLoginForm] = useState({
    username: "",
    password: "",
  })

  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setLoginForm({
          ...loginForm, username: event.target.value
        })
        break;
      case "password":
        setLoginForm({
          ...loginForm, password: event.target.value
        })
        break;
      default:
        break;
    }
  }
  // console.log(loginForm)

  const onSubmitHandler = async(event) => {
    event.preventDefault()
    console.log(loginForm)

    await axios.post('http://127.0.0.1:5000/login', {
      username: loginForm.username,
      password: loginForm.password
    })    
    .then(function (response) {
      // console.log(response);
      // console.log(response.data.result.access_token);

      // save access_token and token_type in localStorage
      localStorage.setItem("auth_token", response.data.access_token)
      localStorage.setItem("auth_token_type", response.data.token_type)
      localStorage.setItem("user", response.data.username )


      // add success notify
      toast.success(response.data.message)

      // reload after success login
      setTimeout(() => {
        window.location.reload()
      }, 1000);

    })
    .catch(function (error) {
      console.log(error);
      // add error notify
      toast.error(error.response.data.detail)
    });

  }

  return (
    <React.Fragment>
        <h1 className="text-3xl font-bold text-center mb-4 cursor-pointer">
            いらっしゃいませ
        </h1>
        <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 -tracking-wide cursor-pointer mx-auto">
アカウントにログインしてください。        </p>
        <form onSubmit={onSubmitHandler}>
          <div className="space-y-4">
            <input 
                type="text" name="" id="" placeholder="ユーザー名"
                onChange={ (event) => {
                  onChangeForm("username", event)
                }}
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            />
            <input 
                type="password" name="" id="" placeholder="パスワード"
                onChange={ (event) => {
                  onChangeForm("password", event)
                } }
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-yellow-400"
            />
          </div>
          <div className="text-center mt-6">
            <button
                type="submit" 
                className="py-3 w-64 text-xl text-white bg-yellow-400 rounded-2xl hover:bg-yellow-300 active:bg-yellow-500 outline-none"
                >
                サインイン
            </button>
            <p>
              アカウントをお持ちではありませんか?{" "}
              <Link 
                to={"/?register"}
                onClick={() => {props.setPage("register")}}
              >
                <span className="underline cursor-pointer">登録する</span> または {" "}
              </Link>
              <Link
                to={"/forgot"}
                onClick={() => {props.setPage("forgot")}}
              >
                <span className="underline cursor-pointer">パスワードをお忘れですか？</span>   
              </Link>
            </p>
          </div>
        </form>
    </React.Fragment>
  )
}
