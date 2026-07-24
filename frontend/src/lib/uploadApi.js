const API_BASE =
    process.env.REACT_APP_API_BASE ||
    "http://127.0.0.1:8000";


// --------------------------------------------------
// Generic Request
// --------------------------------------------------

async function request(path, options = {}) {

    const token =
        JSON.parse(localStorage.getItem("user"))?.token;

    const response = await fetch(
        `${API_BASE}${path}`,
        {
            ...options,

            headers: {

                ...(token && {
                    Authorization: `Bearer ${token}`
                }),

                ...(options.headers || {})

            }

        }
    );

    const data = await response.json();

    if (!response.ok) {

        let message = "Upload Failed";

        if(data.detail){

            if(typeof data.detail === "string"){

                message = data.detail;

            }
            else{

                message = JSON.stringify(data.detail);

            }

        }

        else if(data.error){

            message = data.error;

        }


        throw new Error(message);

    }

    return data;

}


// ==================================================
// Upload File
// ==================================================

export async function uploadFile(formData) {

    const token =
        JSON.parse(localStorage.getItem("user"))?.token;


    const response = await fetch(

        `${API_BASE}/upload/`,

        {
            method:"POST",

            headers:{
                Authorization:`Bearer ${token}`
            },

            body:formData
        }

    );


    let data;

    try{

        data = await response.json();

    }
    catch{

        data = {};

    }



    if(!response.ok){


        console.log("BACKEND ERROR:",data);



        let message="Upload Failed";


        if(data.detail){

            if(Array.isArray(data.detail)){

                message=data.detail
                .map(e=>e.msg)
                .join(",");

            }

            else if(typeof data.detail==="object"){

                message=JSON.stringify(data.detail);

            }

            else{

                message=data.detail;

            }

        }


        throw new Error(

        data.detail
        ?
        (
        typeof data.detail==="string"
        ?
        data.detail
        :
        JSON.stringify(data.detail)
        )
        :
        "Upload failed"

        );

    }


    return data;

}


// ==================================================
// Teacher Uploaded Files
// ==================================================

export async function getUploads() {

    return request(

        "/upload/files",

        {

            method: "GET"

        }

    );

}

// ==================================================
// Get Subjects for Material Upload
// ==================================================

export async function getSubjects() {

    return request(
        "/subjects/",
        {
            method:"GET"
        }
    );

}
// ==================================================
// Upload Previous Paper
// (Phase 9.4)
// ==================================================

export async function uploadPreviousPaper(formData) {

    formData.set(

        "upload_category",

        "previous_paper"

    );

    return uploadFile(formData);

}

export async function deleteUpload(id){

    return request(

        `/upload/files/${id}`,

        {

            method:"DELETE"

        }

    );

}
// ==================================================
// Download Generated Files
// ==================================================

export function downloadPDF() {

    return `${API_BASE}/export/download/question_paper.pdf`;

}

export function downloadDOCX() {

    return `${API_BASE}/export/download/question_paper.docx`;

}

export function downloadJSON() {

    return `${API_BASE}/export/download/question_paper.json`;

}