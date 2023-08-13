import { useState } from "react";
import { Button } from "flowbite-react";
import { ServerInterface } from "../JS/ServerInterface";

function App() {
  const [count, setCount] = useState(0);

  console.log(new ServerInterface().getTest());

  return (
    <div className="main">
      <h1 className="font-extrabold text-5xl">Basic Template</h1>
      <div className="center">
        <Button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </Button>
        <p>
          Basic &nbsp;<code>Vite + React + Tailwind + FlowBite</code> Template
        </p>
      </div>
    </div>
  );
}

export default App;
