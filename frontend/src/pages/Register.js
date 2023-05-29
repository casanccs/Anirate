import { Link } from "react-router-dom";
import './Register.css'

export default function Register(){

    async function Create(){
        let username = document.querySelector('#username').value
        let password = document.querySelector('#password').value
        const response = await fetch('http://127.0.0.1:5000/register', {
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
        window.location.replace('/login')
    }

    return (
        <div className="Register">
            <h1>Register</h1>
            <Link to='/login'>Already have an account? Login!</Link>
            <form method="post" action="/login">
                <label>Username: (Make sure it is the SAME USERNAME is in MyAnimeList!!!)</label>
                <br/>
                <input id='username' type='text' name='username' onKeyDown={
                    e => {
                        if (e.key === 'Enter') {
                            Create()
                          }
                    }
                }/>
                <br />
                <label>Password: </label>
                <br/>
                <input id='password' type='password' name='password' onKeyDown={
                    e => {
                        if (e.key === 'Enter') {
                            Create()
                          }
                    }
                }/>
                <br />
                <input id='submit' type='button' value='Register' onClick={Create} />
            </form>
        </div>
    )
}