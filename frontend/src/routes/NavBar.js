import './NavBar.css'
import { Outlet, Link } from "react-router-dom";

export default function NavBar() {
    return (
      <>
        <div id="navbar">
          <h1>Anirate</h1>
          <Link to='/home'>Home</Link>
          <Link to='/recents'>Recents</Link>
          <Link to='/watching'>Watching</Link>
          <input type='text' placeholder="Search" />
          <input type='button' value='Submit' />
        </div>
        <div id="detail">
          <Outlet />
        </div>
      </>
    );
  }