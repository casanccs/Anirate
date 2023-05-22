import './NavBar.css'
import { Outlet, Link } from "react-router-dom";
import Cookies from "universal-cookie";

export default function NavBar() {
  const cookies = new Cookies();

  async function logout(){
    //await fetch("http://127.0.0.1:5000/logout");
    cookies.remove("jwt_authorization");
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
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}