import { useRef } from "react";

export default function UploadDropzone({

type,

onUpload

}){

const inputRef = useRef();

const chooseFile=()=>{

inputRef.current.click();

};

const change = (e) => {

    if (e.target.files.length === 0) return;

    onUpload([...e.target.files]);

};

return(

<div
onClick={chooseFile}
className="
border-2
border-dashed
border-slate-700
rounded-3xl
p-10
cursor-pointer
text-center
hover:border-blue-500
transition
"
>

<div className="text-5xl">

📂

</div>

<p
className="mt-4 text-white"
>

Click to Upload

</p>

<p
className="text-sm text-slate-400"
>

PDF DOCX XLSX

</p>

<input
    ref={inputRef}
    type="file"
    multiple
    hidden
    onChange={change}
/>

</div>

);

}