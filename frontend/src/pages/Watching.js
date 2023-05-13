import {useEffect, useState} from 'react'

export default function Watching(){

    const [items, setItems] = useState([])
    const [username, setUsername] = useState('zirolet')

    async function getWatching(){
        const response = await fetch(`http://127.0.0.1:5000/watching/${username}`)
        let data = await response.json()
        console.log(data)
        setItems(data)
    }

    useEffect(() => {
        getWatching()
    },[])

    const current = items.map(anime => {
        return (
            <div key={anime.title}>
                <img src={anime.src} alt={anime.title}/>
                <br/>
                <h2>{anime.title}</h2>
            </div>
        )
    })


    return (
        <div className='items'>
            {current}
        </div>
    )
    
}