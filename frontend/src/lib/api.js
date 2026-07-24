// src/lib/api.js

const API_BASE =
  process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000";


// -----------------------------
// Generic Request Handler
// -----------------------------

async function request(
  path,
  options = {}
) {

const token = JSON.parse(localStorage.getItem("user")).token;

  const response = await fetch(
    `${API_BASE}${path}`,
    {
      ...options,

      headers:{
        "Content-Type":"application/json",

        ...(token && {
          Authorization:`Bearer ${token}`
        }),

        ...(options.headers || {})
      }
    }
  );


  const data = await response.json()
    .catch(() => ({}));


  if(!response.ok){

    let message = "Request failed";


    if(data.detail){

        if(Array.isArray(data.detail)){

            message = data.detail
              .map(err => err.msg)
              .join(", ");

        }
        else{

            message = data.detail;

        }

    }
    else if(data.error){

        message = data.error;

    }


    throw new Error(message);

}


  return data;

}



// -----------------------------
// Authentication
// -----------------------------


export async function login(email,password){

    const response = await fetch(
        `${API_BASE}/auth/login`,
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                email,
                password
            })
        }
    );


    if(!response.ok){

        throw new Error("Login failed");

    }


    return await response.json();

}
// ======================================================
export async function getTeachers(){

return request(
"/admin/teachers",
{
method:"GET"
}
);

}



export async function createTeacher(data){

return request(
"/admin/teachers",
{
method:"POST",
body:JSON.stringify(data)
}
);

}



export async function updateTeacher(id,data){

return request(
`/admin/teachers/${id}`,
{
method:"PUT",
body:JSON.stringify(data)
}
);

}



export async function deleteTeacher(id){

return request(
`/admin/teachers/${id}`,
{
method:"DELETE"
}
);

}



export async function disableTeacher(id){

return request(
`/admin/teachers/${id}/disable`,
{
method:"PATCH"
}
);

}



export async function enableTeacher(id){

return request(
`/admin/teachers/${id}/enable`,
{
method:"PATCH"
}
);

}


// -----------------------------
// Knowledge Status
// -----------------------------

export function knowledgeStatus(){

  return request(
    "/knowledge/status",
    {
      method:"GET"
    }
  );

}



// -----------------------------
// Generate Questions
// -----------------------------

export function generateQuestions(
  payload
){

  return request(
    "/generate/",
    {

      method:"POST",

      body:
      JSON.stringify(payload)

    }
  );

}



// -----------------------------
// Generate Paper
// -----------------------------

export function generatePaper(
  payload
){

  return request(
    "/paper/",
    {

      method:"POST",

      body:
      JSON.stringify(payload)

    }
  );

}

// -----------------------------
// Parse Syllabus
// -----------------------------

export async function parseSyllabus(payload){

  return request(
    "/upload/",
    {
      method:"POST",
      body:JSON.stringify(payload)
    }
  );

}


// -----------------------------
// Download Files
// -----------------------------

export function downloadPDF(){

  return `${API_BASE}/export/download/question_paper.pdf`;

}


export function downloadDOCX(){

  return `${API_BASE}/export/download/question_paper.docx`;

}


export function downloadJSON(){

  return `${API_BASE}/export/download/question_paper.json`;

}

