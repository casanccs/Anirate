import './NavBar.css'
import { Outlet, Link } from "react-router-dom";
import Cookies from "universal-cookie";
import addNotification from 'react-push-notification';
import { useEffect } from 'react';

export default function NavBar() {
  let cookies = new Cookies();

  function timeout(delay) {
    return new Promise( res => setTimeout(res, delay) );
  }

  async function checkNewEpisodes(){
        const response = await fetch(`http://127.0.0.1:5000/check`,{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'token': cookies.get('jwt_authorization')
            })
        })
        let data = await response.json()
        console.log(data)
        for (var i = 0; i < data.length; i++){
          if (data[i]['notificate']){
            addNotification({
              title: `New Episode: ${data[i]['title']}`,
              message: data[i]['epNum'],
              duration: 5000,
              native: true,
              onClick: () => window.location="login/"
            })
            await timeout(6000)
          }
        }
  }

  useEffect(() => {
      checkNewEpisodes()
  }, [])

  async function logout(){
    // This does not refresh the page
    document.querySelector('.log').textContent = "Login"
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

  if (cookies.get('jwt_authorization')){
    return (
      <>
        <div id="navbar">
        <Link style={{ textDecoration: 'none' }} to='/home'><h1>Anirate</h1></Link>
          <Link style={{ textDecoration: 'none' }} to='/recents' className='recents'>Recents</Link>
          <Link style={{ textDecoration: 'none' }} to='/watching' className='watching'>Watching</Link>
          <Link style={{ textDecoration: 'none' }} to='/login' onClick={logout} className='log'>Logout</Link>
        </div>
        <div id="detail">
          <Outlet />
        </div>
      </>
    );
  }
  else{
    return (
      <>
        <div id="navbar">
          <Link style={{ textDecoration: 'none' }} to='/home'><h1>Anirate</h1></Link>
          <Link style={{ textDecoration: 'none' }} to='/recents' className='recents'>Recents</Link>
          <Link style={{ textDecoration: 'none' }} to='/watching' className='watching'>Watching</Link>
          <Link style={{ textDecoration: 'none' }} to='/login' className='log'>Login</Link>
        </div>
        <div id="detail">
          <Outlet />
        </div>
      </>
    );
  }

}