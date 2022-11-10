function view_upload(){
    document.getElementById('list_panel').style.display="none";
    document.getElementById('upload_panel').style.display="block";
    document.getElementById('list_button').style.background="url('/static/images/list_button.png')";
    document.getElementById('upload_button').style.background="url('/static/images/upload_button2.png')";
}

function view_list(){
    get_list();
    document.getElementById('list_panel').style.display="block";
    document.getElementById('upload_panel').style.display="none";
    document.getElementById('upload_button').style.background="url('/static/images/upload_button.png')";
    document.getElementById('list_button').style.background="url('/static/images/list_button2.png')";
}

const videoInputElem = document.getElementById('video_input');
const videoInputbox = document.getElementById('video_input_box');
const videoPreviewElem = document.getElementById('video_preview');
const videoPreviewSource = document.getElementById('video_preview_source');
const loadingDisplayElem = document.getElementById('loading_display');
const loadingElem = document.getElementById('loading_loading');
const uploaduploadButtonElem = document.getElementById('upload_upload_button');
const nextuploadButtonElem = document.getElementById('next_upload_button');
videoInputElem.addEventListener('change',(e)=>{
    videoInputbox.style.display="none";
    videoPreviewSource.src=URL.createObjectURL(videoInputElem.files[0]);
    videoPreviewElem.load();
    videoPreviewElem.style.display="block";
    uploaduploadButtonElem.style.display="block";
});

function upload(){
    let data = new FormData();
    const title = document.getElementById('title_input').value;

    if(title=='') return;
    data.append('title',title);
    data.append('video',videoInputElem.files[0]);
    let filename='';
    fetch('/upload',{method:'PUT',body:data}).then(response=>response.json()).then((data)=>{
        console.log(data);
        if(!data['valid']){
            alert("오류 발생 : "+data['code']);
            reset();
        }
        else{
            filename=data['filename'];
        }
    });

    // 악보 생성중!
    loadingDisplayElem.style.display='block';
    loadingElem.src='/static/images/loading.gif';
    i=0
    
    const interval = setInterval(()=>{
        fetch('/check?filename='+filename).then(response=>response.json()).then((data)=>{
            console.log(data);
            if(data['finished']){
                console.log("finished!");
                loadingElem.src="/static/images/finished.gif";
                nextuploadButtonElem.style.display="block";
                clearInterval(interval);
            }
        });
    
    },1000);
}

function reset(){
    videoInputbox.style.display="block";
    document.getElementById('title_input').value="";
    videoPreviewElem.style.display="none";
    uploaduploadButtonElem.style.display="none";
    loadingElem.src='/static/images/loading.gif';

    loadingDisplayElem.style.display='none';

    nextuploadButtonElem.style.display="none";
}

const list_container = document.getElementById('sheet_list');

function get_list(){
    fetch("/list").then((result)=>result.json()).then((data)=>{
        if(!data['valid']){
            alert("unknown error : "+data['code']);
        }
        else{
            list_container.innerHTML='';
            for(let lelem of data.list){
                let title = lelem;
                title=title.substr(0,title.lastIndexOf('.'));
                const video_url = "/video/"+lelem;
                const sheet_url = "/sheet/"+lelem+".musicxml";
                const elem = document.createElement('li');
                elem.classList.add('sheet_container');
                elem.innerHTML=`<span>${title}</span><span><a href="${video_url}" class="download_video"></a><a href="${sheet_url}" download class="download_button"></a></span>`;
                list_container.appendChild(elem);
            }
        }
    });
}