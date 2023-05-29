import { Link } from "react-router-dom";
import Cookies from "universal-cookie";
import jwt from "jwt-decode";


export default function Login(){
    const cookies = new Cookies();


    async function login(){
        let username = document.querySelector('#username').value
        let password = document.querySelector('#password').value
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                //'X-CSRFToken': getCookie("csrftoken")
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
            })
        })
        let data = await response.json()
        console.log(data)
        if (data['token']){
            const decoded = jwt(data['token']);
            cookies.set("jwt_authorization", data['token'], {
                expires: new Date(decoded.exp * 1000),
                domain: 'localhost',
            })
            window.location.replace('/recents');
        }
        else{
           window.location.replace('/register');
        }
    }


    return (
        <div>
            <h1>Login</h1>
            <Link to='/register'>Don't have an account? Register!</Link>
            <form method="post" action="/login">
                <label>Username: </label>
                <input id='username' type='text' name='username' />
                <br />
                <label>Password: </label>
                <input id='password' type='password' name='password' />
                <br />
                <input type='button' value='Login' onClick={login} />
            </form>
        </div>
    )
}