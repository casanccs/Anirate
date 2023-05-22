import { Link } from "react-router-dom";

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
        //window.location.replace('/recents')
    }

    return (
        <div>
            <h1>Register</h1>
            <Link to='/login'>Already have an account? Login!</Link>
            <form method="post" action="/login">
                <label>Username: </label>
                <input id='username' type='text' name='username' />
                <br />
                <label>Password: </label>
                <input id='password' type='password' name='password' />
                <br />
                <input type='button' value='Register' onClick={Create} />
            </form>
        </div>
    )
}