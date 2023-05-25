import './NavBar.css'
import { Outlet, Link } from "react-router-dom";
import Cookies from "universal-cookie";
import addNotification from 'react-push-notification';

export default function NavBar() {
  const cookies = new Cookies();

  async function logout(){
    //await fetch("http://127.0.0.1:5000/logout");
    cookies.remove("jwt_authorization");
  }

  function notification(){
    addNotification({
      title: 'New Episode!',
      message: 'From some anime',
      duration: 5000,
      native: true,
      onClick: () => window.location="login/"
    })
    console.log("Testing")
  }

  return (
    <>
      <div id="navbar">
        <h1>Anirate</h1>
        <Link to='/home'>Home</Link>
        <Link to='/recents'>Recents</Link>
        <Link to='/watching'>Watching</Link>
        <Link to='/login'>Login</Link>
        <input type='text' placeholder="Search" />
        <input type='button' value='Submit' />
        <Link to='/login' onClick={logout} >Logout</Link>
        <button onClick={notification}>Notificate</button>
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}