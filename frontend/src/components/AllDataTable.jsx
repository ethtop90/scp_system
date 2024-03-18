import { isNumber } from "lodash";
import { useEffect, useState } from "react"
import { TEInput } from "tw-elements-react";
import originKeys from '../settings/origin_keys.json'
import _ from 'lodash'
import axios from "axios";
import { toast } from "react-toastify";


export default function AllDataTable({ allData, scpSettingId, dataType }) {
    const username = localStorage.getItem('username');
    const [currentID, setCurrentID] = useState(1);
    const [cnt, setCnt] = useState(1);

    const handleNext = () => {
        setCurrentID(Math.min(cnt - 1, currentID + 1))
    }

    const handlePrev = () => {
        setCurrentID(Math.max(1, currentID - 1))
    }

    const handlePageInput = (e) => {
        // e.preventDefault();
        const page = e.target.value;
        if (isNumber(page) && page > 0 && page <= cnt) {
            setCurrentID(page);
        }
    }

    const handleSave = async () => {
        const username = localStorage.getItem('user');
        const applicationPassword = localStorage.getItem('application_password');
        const cookie_data = document.cookie;
        console.log("cookies:", cookie_data);
        await axios.post(`http://localhost:8080/scp-running/save-alldata?username=${username}&id=${scpSettingId}&dataType=${dataType}&application_password=${applicationPassword}`, {
            'data': allData,
        })
            .then((response) => {
                console.log(response.data);
                toast.success(response.data.message);
            }

            )
            .catch(err => {

            })

        // await axios.post(`http://localhost:8080/scp-running/post-to-wp?username=${username}&id=${scpSettingId}&dataType=${dataType}&application_password=${applicationPassword}&status=draft`, {
        //     'data': allData,
        //     'Cookie': cookie_data,
        //     withCredentials: true, // Include cookies in the request
        //     headers: {
        //         'Content-Type': 'application/json',
        //          // Set the Cookie header with your cookie string
        //     }
        // })
        //     .then((response) => {
        //         console.log(response.data);
        //         toast.success(response.data.message);
        //     }

        //     )
        //     .catch(err => {

        //     })
    }

    useEffect(() => {
        if (allData) setCnt(allData.length);
        console.log(allData);
    }, [allData])

    useEffect(() => {
        console.log(allData.length);
        if (allData.length) setCnt(allData.length);
    }, [])
    return (
        <div className="flex flex-col w-full m-10 h-screen justify-center">
            <div className="flex flex-col w-1/2 mx-auto">
                <div className="flex flex-row w-full justify-center p-5 mx-auto">
                    <div className="prev-btn w-1/4">
                        <button
                            onClick={handlePrev} className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">prev</button>
                    </div>
                    <div className="pages w-1/4 flex justify-center">
                        <span className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">{currentID}</span>
                    </div>
                    <div className="next-btn w-1/4">
                        <button onClick={handleNext} className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">next</button>
                    </div>
                    <div className="w-1/4">
                        <TEInput
                            type="number"
                            id="exampleFormControlInputNumber"
                            label="Number input"
                            value={currentID}
                            onChange={(e) => handlePageInput(e)}
                            width={20}
                        ></TEInput>
                    </div>
                </div>
                <div className="w-full">
                    <div className=" w-[100px] mx-auto">
                        <button onClick={handleSave} className=" inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]">save</button>
                    </div>


                </div>
            </div>

            <div className="flex w-1/2 min-w-min flex-col mx-auto overflow-y-scroll">
                {
                    originKeys[dataType].map((val, index) => {
                        return <dl key={index} className="flex flex-row justify p-3">
                            <dt className="w-1/2 bg-">{val}</dt>
                            <dd className="w-1/2">{_.get(allData[currentID], val)}</dd>
                        </dl>
                    })
                }
            </div>
            {/* <div className="flex flex-row w-1/4 justify-center mx-auto p-5">
                <div className="prev-btn w-1/4">
                    <button className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">prev</button>
                </div>
                <div className="pages w-1/4 flex justify-center">
                    <span className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">{currentID}</span>
                </div>
                <div className="next-btn w-1/4">
                    <button className="relative block rounded bg-transparent px-3 py-1.5 text-sm text-neutral-600 transition-all duration-300 hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-700 dark:hover:text-white">next</button>
                </div>
                <div className="w-1/4">
                    <TEInput
                        type="number"
                        id="exampleFormControlInputNumber"
                        label="Number input"
                        value={currentID}
                        onChange={handlePageInput}
                        width={20}
                    ></TEInput>
                </div>
            </div> */}
        </div>
    )
}