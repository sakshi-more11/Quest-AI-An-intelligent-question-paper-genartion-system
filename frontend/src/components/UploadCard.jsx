import { Card } from "./UI";

export default function UploadCard({

title,

description,

icon,

onClick

}){

return(

<Card
className="cursor-pointer hover:border-blue-500 transition-all"
onClick={onClick}
>

<div className="text-4xl mb-4">

{icon}

</div>

<h2
className="text-lg font-semibold text-white"
>

{title}

</h2>

<p
className="text-sm mt-2 text-slate-400"
>

{description}

</p>

</Card>

);

}