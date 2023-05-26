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