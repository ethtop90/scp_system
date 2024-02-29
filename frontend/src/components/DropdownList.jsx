export default function DropdownList({ title, listData }) {
  return (
    <div>
      <label>
        <TEInput
          type="text"
          id="ptName"
          label={title}
          onChange={(e) => {
            setPtName(e.target.value);
          }}
          list={title}
        ></TEInput>
      </label>
      <datalist
        id={title}
        className="h-full rounded-md border-0 bg-transparent py-0 pl-2 pr-7 text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
      >
        {listData?.map((val, index) => {
          return <option value={val} />;
        })}
      </datalist>
    </div>
  );
}
