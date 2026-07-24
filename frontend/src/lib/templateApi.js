const API_BASE =
process.env.REACT_APP_API_BASE ||
"http://127.0.0.1:8000";



export async function getTemplates(){

const response =
await fetch(
`${API_BASE}/api/templates`
);


if(!response.ok){

throw new Error(
"Failed to fetch templates"
);

}


return await response.json();

}





export async function uploadTemplate(formData){

const response =
await fetch(
`${API_BASE}/api/templates/upload`,
{
method:"POST",
body:formData
}
);



if(!response.ok){

throw new Error(
"Template upload failed"
);

}



return await response.json();

}