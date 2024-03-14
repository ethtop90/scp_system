import React, { useEffect, useRef, useState } from "react";
import { toast } from "react-toastify";
import {
  TERipple,
  TEModal,
  TEModalDialog,
  TEModalContent,
  TEModalHeader,
  TEModalBody,
  TEModalFooter,
  TEDropdown,
  TEDropdownItem,
  TEDropdownMenu,
  TEDropdownToggle,
  TEInput,
  TEButton,
  TELabel,
} from "tw-elements-react";

import { Table, Pagination } from 'antd';
import AllDataTable from "./AllDataTable";

import { Dropdown, Ripple, initTE } from "tw-elements";
import axios from "axios";
import _, { first } from "lodash";

import originKeys from "../settings/origin_keys.json";
import { useNavigate, useNavigationType } from "react-router";
import '../settings/origin_keys.json'
// import fs from "fs";

initTE({ Dropdown, Ripple });

export default function ScpSettingModal({ method }) {
  const navigator = useNavigate();
  const username = localStorage.getItem("user");
  const token = localStorage.getItem("token");
  const fileInput = useRef();
  const [selectedFile, setSelectedFile] = useState(null);
  const [showModal, setShowModal] = useState(method == "update" ? true : false);
  const [id, setId] = useState(null);
  const [sourceType, setSourceType] = useState("site");
  const [datatype, setDataType] = useState("rental");
  const [settingName, setSettingName] = useState();
  const [mgTitle, setMgTitle] = useState("");
  const [ptName, setPtName] = useState("");
  const [source, setSource] = useState("");
  const [dataKeys, setDataKeys] = useState([]);
  let mapping = {};
  let firstData = {};
  const [matchingData, setMatchingData] = useState({});
  const [loading, setLoading] = useState(false);
  const [allDataPageVisible, setAllDataPageVisible] = useState(false);
  let tableColumns = [];
  const [allTabledata, setAllTableData] = useState([{}]);

  const handleTypeBtn = (type) => {
    setSourceType(type);
    setShowModal(true);
  };

  useEffect(() => {
    console.log("sourceType:", sourceType);
  }, [sourceType]);

  const handleMgTitle = (newValue) => {
    console.log(newValue);
    setMgTitle(newValue);
  };

  const handlePtName = (e) => {
    console.log(e.target.value);
    setPtName(e.target.value);
  };

  const handleSource = (e, t) => {
    if (t == "file") {
      const file = e.target.files[0];
      setSelectedFile(file);
    }
    setSource(e.target.value);
  };

  const handleRun = async () => {

    console.log(loading);
    let formData = new FormData();
    formData.append("file", selectedFile);
    console.log(formData);
    if (sourceType == "file") {
      await setLoading(true);
      axios
        .post(
          `http://localhost:8080/scp-running/get-data/file?username=${username}&type=${datatype}&get_type=one`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          console.log("File uploaded successfully:", response.data.message);
          processData(response.data);
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
      await setLoading(false);
    } else {
      await setLoading(true);
      await axios
        .post(
          `http://localhost:8080/scp-running/get-data/site?username=${username}&type=${datatype}&get_type=one`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            source: source,
          }
        )
        .then((response) => {
          console.log("File uploaded successfully:", response.data.message);
          if (response.data.valid == true) {
            processData(response.data);
          } else {
            toast.error("url or type is invalid");
          }
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
      await setLoading(false);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();

    if (method == "add") {
      await axios
        .post(
          `http://localhost:8080/scp-settings/add-item?username=${username}&type=${datatype}&source=${source}`,
          {
            type: sourceType,
            data_type: datatype,
            mg_title: mgTitle,
            pt_name: ptName,
            source: source,
          }
        )
        .then((response) => {
          toast.success(response.data.message);
          setId(response.data.id);
        })
        .catch((error) => {
          console.log(error);
        });
      fetchData();
    } else {
      await axios
        .put(
          `http://localhost:8080/scp-settings/update-item?username=${username}&id=${id}`,
          {
            type: sourceType,
            data_type: datatype,
            mg_title: mgTitle,
            pt_name: ptName,
            source: source,
          }
        )
        .then((response) => {
          toast.success(response.data.message);
        })
        .catch((error) => {
          console.log(error);
        });
      fetchData();
    }
  };

  const handleMatchingData = (key, val) => {
    console.log(key, val);
    setMatchingData({
      ...matchingData,
      mapping: { ...matchingData.mapping, [key]: val },
    });
  };

  function swapKeysAndValues(obj) {
    var swappedObject = {};
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        swappedObject[obj[key]] = key;
      }
    }
    return swappedObject;
  }

  const addNewItem = (item) => {
    setAllTableData(prevArray => [...prevArray, item]);

  }

  const getAllScpData = async () => {
    setLoading(true);

    if (sourceType == 'site') {
      await axios
        .post(
          `http://localhost:8080/scp-running/get-data/site?username=${username}&type=${datatype}&get_type=all`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            source: source,
          }
        )
        .then((response) => {
          if (response.data.valid == true) {
            const tempTabledata = response.data['all_data'];
            const tempData = matchingData.mapping;
            const replacedData = swapKeysAndValues(tempData);
            console.log("tempTabledata:", tempTabledata);
            tempTabledata.map((item) => {
              console.log("item:", item);
              let itemData = {}
              originKeys[datatype].map((val) => {
                if (replacedData.hasOwnProperty(val)) {
                  itemData[val] = item[replacedData[val]];
                }
                else {
                  itemData[val] = null;
                }

              })
              console.log(itemData)
              // allTabledata.push(itemData)
              addNewItem(itemData);

            })
            console.log('allTabledata:', allTabledata);
          } else {
            toast.error("url or type is invalid");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
    else {
      let formData = new FormData();
      formData.append("file", selectedFile);
      console.log("get-data file request sent!", formData['file']);
      await axios
        .post(
          `http://localhost:8080/scp-running/get-data/file?username=${username}&type=${datatype}&get_type=all`,

          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${token}`,
            },
          }

        )
        .then((response) => {
          if (response.data.valid == true) {
            const tempTabledata = response.data['all_data'];
            const tempData = matchingData.mapping;
            const replacedData = swapKeysAndValues(tempData);
            console.log("tempTabledata:", tempTabledata);
            tempTabledata.map((item) => {
              console.log("item:", item);
              let itemData = {}
              originKeys[datatype].map((val) => {
                if (replacedData.hasOwnProperty(val)) {
                  itemData[val] = item[replacedData[val]];
                }
                else {
                  itemData[val] = null;
                }

              })
              console.log(itemData)
              // allTabledata.push(itemData)
              addNewItem(itemData);

            })
            console.log('allTabledata:', allTabledata);
          } else {
            toast.error("url or type is invalid");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }

    setLoading(false);
  }

  const handleMatchingDataSave = async (e) => {
    e.preventDefault();
    if (id) {
      await axios
        .post(
          `http://localhost:8080/scp-running/matching-data/add?username=${username}&id=${id}`,
          {
            ...matchingData,
          }
        )
        .then((response) => {

        })
        .catch((error) => {
          console.log(error);
        });
      await getAllScpData();
      setAllDataPageVisible(true);
      console.log(allDataPageVisible);
      // mapping.map
    } else {
      toast.error("Save the setting!");
    }
  };

  const fetchData = async () => {
    const username = localStorage.getItem("user");
    const url = window.location.href;
    const searchParams = new URLSearchParams(new URL(url).search);
    const id = searchParams.get("id");
    if (username && id) {
      console.log(username, id);
      await axios
        .get(
          `http://localhost:8080/scp-settings/get-item?username=${username}&id=${id}`
        )
        .then((response) => {
          toast.success(response.data.message);
          let data = response.data;
          console.log(data);
          console.log(data.data_type);
          setSourceType(data.type);
          setSource(data.source);
          console.log(data.source);
          setDataType(data.data_type);
          setMgTitle(data.mg_title);
          setPtName(data.pt_name);
          setId(data.id);
        })
        .catch((error) => {
          console.log(error);
        });
      method == "update" &&
        (await axios
          .get(
            `http://localhost:8080/scp-running/matching-data/get?username=${username}&id=${id}&type=${datatype}`,
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          )
          .then((response) => {
            console.log(response.data);
            setMatchingData({ ...response.data });
          })
          .catch((error) => {
            console.log(error);
          }));
    }
  };

  const processData = (data) => {
    setDataKeys([...data["item_keys"]]);
    mapping = JSON.stringify(data["mapping"]);
    firstData = JSON.stringify(data["first_data"]);
    setMatchingData({ ...data });
  };

  useEffect(() => {
    console.log("method:", method);
    if (method == "update") {
      const username = localStorage.getItem("user");
      const url = window.location.href;
      const searchParams = new URLSearchParams(new URL(url).search);
      setId(searchParams.get("id"));
      fetchData();
    }
    setLoading(false);
    console.log('originKeys:', originKeys[datatype]);
    // originKeys.map((value, index) => {
    //   tableColumns.push({ title: value, dataIndex: value, key: value })
    // })
    // console.log("tableColumns:", tableColumns);
  }, []);

  const handleChangePage = () => {

  }

  useEffect(() => {
    // fetchData();
    console.log(showModal);
    if (showModal == false && method == "update") navigator(-1);
  }, [showModal]);

  useEffect(() => {
    console.log(id);
  }, [id]);




  return (
    <>
      {
        allDataPageVisible ?
          <div className="">
            {allTabledata && <AllDataTable allData={allTabledata} scpSettingId={id} dataType={datatype} />}
            <div className="flex justify-center w-1/2 mx-auto px-10">
              <button
                type="button"
                className="inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                onClick={(e) => { setAllDataPageVisible(false) }}
              >
                Go back
              </button>
            </div>
          </div> :
          <div>
            {/* <!-- Button trigger modal --> */}
            <TERipple rippleColor="white" className="flex justify-center m-10 gap-5">
              <button
                type="button"
                className="inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                onClick={() => handleTypeBtn("site")}
              >
                サイトから取込
              </button>
              <button
                type="button"
                className="inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                onClick={() => handleTypeBtn("file")}
              >
                エクセルから取込
              </button>
            </TERipple>

            {/* <!-- Modal --> */}
            <TEModal show={showModal} setShow={setShowModal} scrollable onc>
              <TEModalDialog size="lg" centered>
                <TEModalContent>
                  <TEModalHeader>
                    {/* <!--Modal title--> */}
                    <h5 className="text-xl font-medium leading-normal text-neutral-800 dark:text-neutral-200">
                      {sourceType == "file" ? "エクセルから取込" : "サイトから取込"}
                    </h5>
                    {/* <!--Close button--> */}
                    <button
                      type="button"
                      className="box-content rounded-none border-none hover:no-underline hover:opacity-75 focus:opacity-100 focus:shadow-none focus:outline-none"
                      onClick={() => setShowModal(false)}
                      aria-label="Close"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth="1.5"
                        stroke="currentColor"
                        className="h-6 w-6"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </TEModalHeader>
                  {/* <!--Modal body--> */}
                  <TEModalBody>
                    {
                      (loading) ?
                        <div className="w-full flex justify-center items-center z-100">
                          <div
                            className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                            role="status">
                            <span
                              className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]"
                            >Loading...</span>
                          </div>
                        </div>
                        :
                        <div className="site-main w-full">
                          <div className="flex flex-col items-center w-full p-5">
                            <div className="flex flex-col items-center w-full">
                              <div className="real-type flex justify-between w-full m-5">
                                <div className="">
                                  <TEDropdown className="flex justify-center w-full">
                                    <TERipple rippleColor="light w-full">
                                      <TEDropdownToggle className="flex items-center whitespace-nowrap rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] motion-reduce:transition-none dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] w-full">
                                        {/* 投稿ユーザー（会社名） */}
                                        {datatype == "rental" ? "賃貸" : "売買"}
                                        <span className="ml-2 [&>svg]:w-5 w-2">
                                          <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 20 20"
                                            fill="currentColor"
                                          >
                                            <path
                                              fillRule="evenodd"
                                              d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                                              clipRule="evenodd"
                                            />
                                          </svg>
                                        </span>
                                      </TEDropdownToggle>
                                    </TERipple>

                                    <TEDropdownMenu>
                                      <TEDropdownItem
                                        onClick={() => setDataType("rental")}
                                      >
                                        <span
                                          href="#"
                                          className="block w-full min-w-[160px] cursor-pointer whitespace-nowrap bg-transparent px-4 py-2 text-sm text-left font-normal pointer-events-auto text-neutral-700 hover:bg-neutral-100 active:text-neutral-800 active:bg-neutral-100 focus:bg-neutral-100 focus:text-neutral-800 focus:outline-none active:no-underline dark:text-neutral-200 dark:hover:bg-neutral-600 dark:focus:bg-neutral-600 dark:active:bg-neutral-600"
                                          value="賃貸"
                                        >
                                          賃貸
                                        </span>
                                      </TEDropdownItem>
                                      <TEDropdownItem
                                        onClick={() => setDataType("selling")}
                                      >
                                        <span
                                          href="#"
                                          className="block w-full min-w-[160px] cursor-pointer whitespace-nowrap bg-transparent px-4 py-2 text-sm text-left font-normal pointer-events-auto text-neutral-700 hover:bg-neutral-100 active:text-neutral-800 active:bg-neutral-100 focus:bg-neutral-100 focus:text-neutral-800 focus:outline-none active:no-underline dark:text-neutral-200 dark:hover:bg-neutral-600 dark:focus:bg-neutral-600 dark:active:bg-neutral-600"
                                        >
                                          売買
                                        </span>
                                      </TEDropdownItem>
                                    </TEDropdownMenu>
                                  </TEDropdown>
                                </div>
                                <div>
                                  <TEInput
                                    type="text"
                                    id="exampleFormControlInputText"
                                    label={"管理⽤タイトル"}
                                    onChange={(e) => {
                                      setMgTitle(e.target.value);
                                    }}
                                    value={mgTitle}
                                  ></TEInput>
                                </div>
                                <div>
                                  <label>
                                    <TEInput
                                      type="text"
                                      id="ptName"
                                      label={"投稿ユーザー（会社名）"}
                                      onChange={(e) => {
                                        setPtName(e.target.value);
                                      }}
                                      list="mgTitleList"
                                      value={ptName}
                                    ></TEInput>
                                    {/* <input
                            list="browsers"
                            name="myBrowser"
                            className="block w-full h-full rounded-md border-0 py-2  pl-7 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                          /> */}
                                  </label>
                                  <datalist
                                    id="mgTitleList"
                                    className="h-full rounded-md border-0 bg-transparent py-0 pl-2 pr-7 text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
                                  >
                                    {/* change part */}
                                  </datalist>
                                </div>
                                <div>
                                  <button
                                    type="button"
                                    className="block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                                    onClick={(e) => handleSave(e)}
                                  >
                                    更新
                                  </button>
                                </div>
                              </div>

                              <div className="flex justify-start gap-10 w-full my-10">
                                <div className="">
                                  <span className="mb-3"> スクレイピング先URL</span>
                                  {sourceType == "site" ? (
                                    <TEInput
                                      type="url"
                                      value={source}
                                      onChange={(e) => handleSource(e, "site")}
                                    ></TEInput>
                                  ) : (
                                    <TEInput
                                      type="file"
                                      ref={fileInput}
                                      onChange={(e) => handleSource(e, "file")}
                                      accept=".xlsx"
                                    // value={source}
                                    ></TEInput>
                                  )}
                                  {source && (
                                    <>
                                      <p>{source}</p>
                                    </>
                                  )}
                                </div>
                                <div className="flex items-end ">
                                  <button
                                    type="button"
                                    className="block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                                    onClick={(e) => handleRun(e)}
                                  >
                                    実⾏
                                  </button>
                                </div>
                              </div>
                            </div>
                            <hr className=""></hr>
                            <div className="grid grid-cols-3 gap-1 w-full ">
                              <div className="col-span-2 p-2">スクレイピング設定</div>
                              <div className="col-span-1 p-2 text-sm"></div>
                              <div className="col-span-2 p-2 grid grid-cols-2">
                                <span className="col-span-1">⼭⼝不動産ガイド</span>
                                <span className="col-span-1">スクレイピング先サイト</span>
                              </div>
                              <div>
                                <label>
                                  <TEInput
                                    type="text"
                                    id="ptName"
                                    label={"物件掲載業者絞り込み"}
                                    onChange={(e) => {
                                      setPtName(e.target.value);
                                    }}
                                    list="ptNameList"
                                  ></TEInput>
                                </label>
                                <datalist
                                  id="ptNameList"
                                  className="h-full rounded-md border-0 bg-transparent py-0 pl-2 pr-7 text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
                                >
                                  {/* change part */}
                                </datalist>
                              </div>
                            </div>

                            {matchingData.item_keys &&
                              matchingData.item_keys.map((value, index) => (
                                <div className="grid grid-cols-3 w-full" key={index}>
                                  <div className="col-span-1 p-3">{value}</div>
                                  <div className="col-span-1 p-3">
                                    {matchingData.first_data[value]}
                                  </div>
                                  <div className="col-span-1 p-3">
                                    <select
                                      value={matchingData.mapping[value]}
                                      onChange={(e) =>
                                        handleMatchingData(value, e.target.value)
                                      }
                                    >
                                      {originKeys[datatype].map((v, i) => (
                                        <option key={i} value={v}>
                                          {v}
                                        </option>
                                      ))}
                                    </select>
                                  </div>
                                </div>
                              ))}
                          </div>
                        </div>
                    }
                  </TEModalBody>
                  <TEModalFooter className="flex justify-center">
                    {/* <TERipple rippleColor="light">
                <button
                  type="button"
                  className="inline-block rounded bg-primary-100 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-primary-700 transition duration-150 ease-in-out hover:bg-primary-accent-100 focus:bg-primary-accent-100 focus:outline-none focus:ring-0 active:bg-primary-accent-200"
                  onClick={() => setShowModal(false)}
                >
                  いいえ
                </button>
              </TERipple>
              <TERipple rippleColor="light">
                <button
                  type="button"
                  className="ml-1 inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                  onClick={(e) => handleSave(e)}
                >
                  変更内容を保存
                </button>
              </TERipple> */}
                    <div className="flex justify-center">
                      <button
                        type="button"
                        className="ml-1 inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                        onClick={(e) => handleMatchingDataSave(e)}
                      >
                        スクレイピング結果の取込
                      </button>
                    </div>
                  </TEModalFooter>
                </TEModalContent>
              </TEModalDialog>
            </TEModal>
          </div>
      }

    </>
  );
}
