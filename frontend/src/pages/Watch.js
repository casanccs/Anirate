import { useEffect } from "react";
import Hls from "hls.js";
import { useSearchParams } from "react-router-dom";
export default function Home(){

    const [searchParams, setSearchParams] = useSearchParams();
    const anime = searchParams.get('anime')
    const epNum = searchParams.get('epNum')

    async function getData(){
        /*
            In order for me to get the correct url, I have to send a request to the anime API
            - When I click on 
            1. Let's assume I clicked on "Dr Stone: New World"
            2. Split the title so that it becomes "dr-stone-new-world", so get rid of weird characters, and turn spaces into "-"
            3. Get the latest episode by using the fetch api, which gets the link to the latest episode as well
        */
       let url;
        try {
            const mainurl = `https://api.consumet.org/anime/gogoanime/info/${anime}`
            const initresponse = await fetch(mainurl)
            const predata = await initresponse.json()
            console.log(predata)
            console.log(predata['episodes'])
            console.log(predata['totalEpisodes'])
            console.log(predata['episodes'][predata['totalEpisodes']-1]['url'])
            url = `https://api.consumet.org/anime/gogoanime/watch/${anime}-episode-${predata['totalEpisodes']}`
        }
        catch{
            url = `https://api.consumet.org/anime/gogoanime/watch/${anime}-episode-${parseInt(epNum.replace(/\D/g,''))}`
        }
        console.log(url)
        const response = await fetch(url);
        let data = await response.json();
        console.log(data);
        let x = data['sources'][3]['url'];
        if(Hls.isSupported())
        {
            var video = document.getElementById('video');
            var hls = new Hls();
            hls.loadSource(x);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED,function()
            {
                video.play();
            });
        }
        else if (video.canPlayType('application/vnd.apple.mpegurl'))
        {
            video.src = 'playlist.m3u8';
            video.addEventListener('canplay',function()
            {
                video.play();
            });
        }
        return data;
    }

    useEffect(() => {
        getData();
    },[])

    return(
    <div>
        {/* <video width="352" height="198" controls>
            <source src={vidURL} type="application/x-mpegURL" />
        </video> */}
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <video id="video" controls></video>
        
    </div>
    )


}