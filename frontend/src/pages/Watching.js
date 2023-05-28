import {useEffect, useState} from 'react'
import Cookies from "universal-cookie";
import { Link } from 'react-router-dom';

export default function Watching(){

    const [items, setItems] = useState([])
    const [user, setUser] = useState("Not Logged In!")

    async function getWatching(){
        let cookies = new Cookies();

        const response = await fetch(`http://127.0.0.1:5000/watching`,{
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
        if (data['message']){
            console.log(data['message'])
        }
        else{
            setItems(data['data'])
            setUser(data['username'])
        }
    }

    useEffect(() => {
        getWatching()
    },[])

    let current;
    if (items){
        current = items.map(anime => {
            return (
                <Link key={anime.title} to={`/watch/?anime=${anime.title.replace(/[[\]&\:.()!]+/g, '').replace(/ /g, "-").toLowerCase()}&epNum=${anime.epNum}`}>
                    <div >
                        <img src={anime.src} alt={anime.title}/>
                        <br/>
                        <h2>{anime.title}</h2>
                    </div>
                </Link>
            )
        })
    }

    return (
        <div className='items'>
            <h1>Watch list for: {user}</h1>
            {current}
        </div>
    )
    
}