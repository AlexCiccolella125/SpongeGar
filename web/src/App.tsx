import React, { useState } from 'react';
import './App.css';
import MyTopAppBar from './Layout/MyTopAppBar';
import MyDrawer from "./Layout/Drawer";

const sendRequest = () => {
    return fetch("http://localhost:5000/command", {method: 'POST'})
}

const App: React.FC<any> = () => {
    const [open, setOpen] = useState(false);
  return (
    <>
        <MyTopAppBar open={open} setOpen={(isOpen: boolean) => setOpen(isOpen)}/>
        <MyDrawer open={open} content={<button onClick={() => sendRequest()}>CLICK ME!</button>}/>
    </>
  );
}

export default App;
