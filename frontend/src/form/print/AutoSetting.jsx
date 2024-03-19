import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { TEInput } from "tw-elements-react";
import { toast } from "react-toastify"

export default function AutoSetting() {
  const week = [
    "月曜⽇",
    "火曜⽇",
    "水曜⽇",
    "木曜⽇",
    "金曜⽇",
    "土曜⽇",
    "日曜⽇",
  ];

  // const [id, setId] = useState(useParams("id"));
  const [hours, setHours] = useState([]);
  const [ptTime, setPtTime] = useState("");
  const [check, setCheck] = useState([]);

  const fetchData = async () => {
    //change part
    //fetch hours by using settingName
    const username = localStorage.getItem("user");
    const url = window.location.href;
    const searchParams = new URLSearchParams(new URL(url).search);
    let id = searchParams.get("id");

    if (id != null && username != null) {
      console.log(searchParams.get("id"));
      await axios
        .get(
          `http://49.212.185.58:8080/scp-settings/get-item?username=${username}&id=${id}`
        )
        .then((response) => {
          setHours([...response.data.up_settings]);
          setPtTime(response.data.pt_start_time);
          setCheck([...response.data.week_check]);
          toast.success(response.data.message);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  const handlePtTime = (e) => {
    setPtTime(e.target.value);
    console.log(ptTime);
  };

  const handleCheck = (index) => {
    let c = check;
    c[index] = !c[index];
    setCheck([...c]);
    console.log(check);
  };

  const handleAutoSettingSave = async () => {
    const username = localStorage.getItem("user");
    const url = window.location.href;
    const searchParams = new URLSearchParams(new URL(url).search);
    let id = searchParams.get("id");
    await axios
      .put(
        `http://49.212.185.58:8080/scp-settings/update-item?username=${username}&id=${id}`,
        {
          enabled: true,
          pt_start_time: ptTime,
          week_check: check,
          up_settings: hours,
          next_time: ptTime,
        }
      )
      .then((response) => {
        toast.success(response.data.message);
      })
      .catch((error) => {
        console.log(error);
      });
    fetchData();
  };

  const handleHours = (e, index) => {
    let newArray = [...hours];
    newArray[index] = e.target.value;
    newArray = newArray.map(Number);
    setHours(newArray);
  }

  const giveData = () => { };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-10 mx-10">
        <div className="flex justify-center mt-10">
          <h2 className="text-3xl">⾃動投稿</h2>
          {/* <h3>{settingName}</h3> */}
        </div>
        <div className="datetime-seletor flex flex-col w-100 ">
          <div className="w-80">
            <p className="text-xl text-blue mb-5">初回投稿開始</p>
            <TEInput
              type="datetime-local"
              id="printingTime"
              name="printingTime"
              className="w-1/2 mb-5"
              value={ptTime}
              onInput={handlePtTime}
            />
          </div>

          <span>※件数によって投稿時間に遅れが出る可能性があります。</span>
        </div>
        <div className="printing-seletor">
          <h3>更新設定</h3>
          {/* change part */}
          {week.map((val, index) => (
            <div className="flex flex-row m-5">
              <div className="flex items-center">
                <input
                  className="relative float-left -ml-[1.5rem] mr-[6px] mt-[0.15rem] h-[1.125rem] w-[1.125rem] appearance-none rounded-[0.25rem] border-[0.125rem] border-solid border-neutral-300 outline-none before:pointer-events-none before:absolute before:h-[0.875rem] before:w-[0.875rem] before:scale-0 before:rounded-full before:bg-transparent before:opacity-0 before:shadow-[0px_0px_0px_13px_transparent] before:content-[''] checked:border-primary checked:bg-primary checked:before:opacity-[0.16] checked:after:absolute checked:after:-mt-px checked:after:ml-[0.25rem] checked:after:block checked:after:h-[0.8125rem] checked:after:w-[0.375rem] checked:after:rotate-45 checked:after:border-[0.125rem] checked:after:border-l-0 checked:after:border-t-0 checked:after:border-solid checked:after:border-white checked:after:bg-transparent checked:after:content-[''] hover:cursor-pointer hover:before:opacity-[0.04] hover:before:shadow-[0px_0px_0px_13px_rgba(0,0,0,0.6)] focus:shadow-none focus:transition-[border-color_0.2s] focus:before:scale-100 focus:before:opacity-[0.12] focus:before:shadow-[0px_0px_0px_13px_rgba(0,0,0,0.6)] focus:before:transition-[box-shadow_0.2s,transform_0.2s] focus:after:absolute focus:after:z-[1] focus:after:block focus:after:h-[0.875rem] focus:after:w-[0.875rem] focus:after:rounded-[0.125rem] focus:after:content-[''] checked:focus:before:scale-100 checked:focus:before:shadow-[0px_0px_0px_13px_#3b71ca] checked:focus:before:transition-[box-shadow_0.2s,transform_0.2s] checked:focus:after:-mt-px checked:focus:after:ml-[0.25rem] checked:focus:after:h-[0.8125rem] checked:focus:after:w-[0.375rem] checked:focus:after:rotate-45 checked:focus:after:rounded-none checked:focus:after:border-[0.125rem] checked:focus:after:border-l-0 checked:focus:after:border-t-0 checked:focus:after:border-solid checked:focus:after:border-white checked:focus:after:bg-transparent dark:border-neutral-600 dark:checked:border-primary dark:checked:bg-primary dark:focus:before:shadow-[0px_0px_0px_13px_rgba(255,255,255,0.4)] dark:checked:focus:before:shadow-[0px_0px_0px_13px_#3b71ca]"
                  type="checkbox"
                  value=""
                  id="checkboxChecked"
                  checked={check[index] ? true : false}
                  onChange={() => handleCheck(index)}
                />
              </div>
              <div className="mx-10 flex items-center">
                <p>{val}</p>
              </div>
              <div className="mx-10">
                <TEInput
                
                  type="number"
                  id="ptTime"
                  width={10}
                  onChange={(e) => {
                    handleHours(e, index);
                  }}
                  label={val}
                  list="weekTime"
                  className="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  disabled={!check[index]}
                ></TEInput>

                <datalist id="weekTime">
                  {Array.from({ length: 23 }, (_, index) =>
                    index.toString().padStart(2, "0")
                  ).map((hour) => (
                    <option value={hour}></option>
                  ))}
                </datalist>
              </div>
            </div>
          ))}
        </div>
        <div className="flex justify-center">
          <button
            type="button"
            className="inline-block rounded bg-primary-700 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
            onClick={() => handleAutoSettingSave()}
          >
            投稿予約
          </button>
        </div>
      </div>
    </div>
  );
}
