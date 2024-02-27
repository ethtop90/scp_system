import React, { useContext, useState, useRef } from "react";
import { useEffect } from "react";
import { UserInfoContext } from "../../App"; // Update the import path based on your project structure
import axios from "axios";
import { Link, json, useFetcher, useNavigate } from "react-router-dom";
import { BlueButton } from "../../components/BlueButton";
import ScpSettingModal from "../../components/ScpSettingModal";


export default function ScpSetting() {
  // const userInfo = useContext(UserInfoContext);
  const username = localStorage.getItem("user");
  const token = localStorage.getItem("auth_token");
  const navigate = useNavigate();
  const [scpItems, setScpItems] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchAll();
  }, [username]);

  async function fetchAll() {
    await axios
      .get("http://localhost:5000/scp-settings/getall?username=" + username, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setScpItems([...JSON.parse(response.data)]);
        console.log(scpItems.length);
      })
      .catch((err) => {});
  }

  // const handleAddBtn = (e) => {
  //   setShowModal(true)
  // }

  return (
    <>
      <div className="flex justify-end m-5">
        <Link
          class="bg-gray-800 text-white rounded-l-md border-r border-gray-100 py-2 hover:bg-red-700 hover:text-white px-3"
          to={"/"}
        >
          <div class="flex flex-row align-middle">
            <svg
              class="w-5 mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
            <p class="ml-2">Prev</p>
          </div>
        </Link>
      </div>
      <div class="m-2 flex items-center justify-center bg-white px-3 md:px-2 z-0">
        <div class="space-y-6 border-l-2 border-dashed flex flex-col w-full">
          {/* <div>{scpItems.length}</div> */}
          {Array.isArray(scpItems) && scpItems.map((item, index) => (
              <div key={index} className="flex flex-row gap-10">
                <div className="w-1/6 flex justify-center items-center">
                  <BlueButton text={item.type == "site" ? "賃貸" : "売買"} />
                </div>
                <div className="flex flex-col w-1/2 justify-center items-center">
                  <div>{item.mg_title}</div>
                  <div>{item.source}</div>
                </div>
                <div className="w-1/6">
                  <BlueButton
                    text={item.type == "site" ? "設定変更" : "再取込"}
                  />
                </div>
                <div className="w-1/6">
                  <BlueButton text={"削除"} />
                </div>
              </div>
            ))}
          <div className=" flex justify-center">
            <Link
              className="w-1/6 text-center inline-block rounded bg-blue-400 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-blue-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-blue-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-blue-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
              to={"add"}
            >
              新規追加
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
