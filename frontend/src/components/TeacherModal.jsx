// src/components/TeacherModal.jsx

import { useEffect, useState } from "react";


export default function TeacherModal({

open,

teacher,

onClose,

onSave

}){


const [form,setForm]=useState({

full_name:"",

email:"",

password:"",

designation:"",

department:"",

subject:""

});





useEffect(()=>{


if(teacher){


setForm({

full_name:
teacher.full_name || "",


email:
teacher.email || "",


password:"",


designation:
teacher.designation || "",


department:
teacher.department || "",


subject:
teacher.subject || ""

});


}

else{


setForm({

full_name:"",

email:"",

password:"",

designation:"",

department:"",

subject:""

});


}



},[teacher]);






if(!open)
return null;






const change=(e)=>{


setForm({

...form,

[e.target.name]:
e.target.value

});


};






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
max-w-lg
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
mb-5
"

>

{

teacher

?

"Edit Teacher"

:

"Add Teacher"

}


</h2>







<div className="space-y-4">



{

[

["full_name","Full Name"],

["email","Email"],

["password","Password"],

["designation","Designation"],

["department","Department"],

["subject","Subject"]

].map(([key,label])=>(



<div key={key}>


<label

className="
text-xs
text-slate-400
"

>

{label}

</label>



<input

name={key}

value={form[key]}

onChange={change}

type={
key==="password"

?

"password"

:

"text"

}

className="
w-full
mt-1
px-4
py-2
rounded-xl
bg-slate-900
border
border-slate-700
text-white
"

/>



</div>



))


}





</div>






<div

className="
flex
justify-end
gap-3
mt-6
"

>


<button

onClick={onClose}

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

onClick={()=>onSave(form)}

className="
px-5
py-2
rounded-xl
bg-blue-600
text-white
"

>

Save

</button>



</div>



</div>



</div>


);


}