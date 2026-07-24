// src/components/ConfirmDialog.jsx


export default function ConfirmDialog({

open,

title,

message,

confirmText,

onCancel,

onConfirm

}){


if(!open)
return null;



return (

<div

className="
fixed inset-0
bg-black/60
flex
items-center
justify-center
z-50
"

>


<div

className="
w-full
max-w-md
rounded-3xl
bg-slate-950
border
border-slate-800
p-6
"

>


<h2

className="
text-xl
font-semibold
text-white
"

>

{title}

</h2>



<p

className="
mt-3
text-sm
text-slate-400
"

>

{message}

</p>





<div

className="
flex
justify-end
gap-3
mt-6
"

>


<button

onClick={onCancel}

className="
px-5
py-2
rounded-xl
bg-slate-800
text-white
"

>

Cancel

</button>





<button

onClick={onConfirm}

className="
px-5
py-2
rounded-xl
bg-red-600
text-white
"

>

{confirmText}

</button>



</div>



</div>



</div>


);


}