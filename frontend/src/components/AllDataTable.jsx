import { isNumber } from "lodash";
import { useEffect, useState } from "react"
import { TEInput } from "tw-elements-react";
import originKeys from '../settings/origin_keys.json'
import _ from 'lodash'


export default function AllDataTable({ allData }) {
    const [currentID, setCurrentID] = useState(1);
    const [cnt, setCnt] = useState(0);

    const handleNext = () => {
        setCurrentID = setCurrentID(Math.min(cnt, currentID + 1))
    }

    const handlePrev = () => {
        setCurrentID = setCurrentID(Math.max(0, currentID - 1))
    }

    const handlePageInput = (e) => {
        e.preventDefault();
        const page = e.target.value;
        if (isNumber(page) && page > 0 && page <= cnt) {
            setCurrentID(page);
        }
    }

    useEffect(() => {
        if (allData) setCnt(allData.length);
        console.log(allData);
    }, [allData])

    useEffect(() => {
        console.log(allData);
        if (allData.length) setCnt(allData.length);
    }, [])
    return (
        <div className="flex flex-col w-full m-10 h-screen">
            <div className="flex flex-row w-1/4 justify-center mx-auto p-5">
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
                        onChange={handlePageInput}
                        width={20}
                    ></TEInput>
                </div>
            </div>
            <div className="flex w-1/2 min-w-min flex-col mx-auto overflow-y-scroll">
                {
                    originKeys.map((val, index) => {
                        return <dl key={index} className="flex flex-row justify p-3">
                            <dt className="w-1/2 bg-">{val}</dt>
                            <dd className="w-1/2">{_.get(allData[currentID], val)}</dd>
                        </dl>
                    })
                }
            </div>
            <div className="flex flex-row w-1/4 justify-center mx-auto p-5">
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
            </div>
        </div>
    )
}