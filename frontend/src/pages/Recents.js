import {useEffect, useState} from 'react'

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
            <div key={anime.title}>
                <img src={anime.img} alt={anime.title}/>
                <br/>
                <h2>{anime.title}</h2>
                <h3>{anime.epNum}</h3>
            </div>
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