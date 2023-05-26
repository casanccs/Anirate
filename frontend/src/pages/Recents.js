import {useEffect, useState} from 'react'
import { Link } from 'react-router-dom'
export default function Recents(){

    const [recents, setRecents] = useState([])

    async function getRecents(){
        let response = await fetch('http://localhost:5000/recents')
        let data = await response.json()
        setRecents(data)
    }

    useEffect(() => {
        getRecents()
    }, [])

    const recentItems = recents.map(anime => {
        return (
            <Link key={anime.title} to={`/watch/?anime=${anime.title.replace(/[[\]&\:.()!]+/g, '').replace(/ /g, "-").toLowerCase()}&epNum=${anime.epNum}`}>
                <div >
                    <img src={anime.img} alt={anime.title}/>
                    <br/>
                    <h2>{anime.title}</h2>
                    <h3>{anime.epNum}</h3>
                </div>
            </Link>
        )
    })

    return(
        <div className='Recents'>
            <h1>Recent Anime</h1>
            <div className='items'>
                {recentItems}
            </div>
        </div>
    )
}