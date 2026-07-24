const API_BASE =
process.env.REACT_APP_API_BASE ||
"http://127.0.0.1:8000";

async function request(path,options={}){

    const token =
    JSON.parse(localStorage.getItem("user"))?.token;

    const response = await fetch(
        `${API_BASE}${path}`,
        {
            ...options,

            headers:{
                "Content-Type":"application/json",

                Authorization:`Bearer ${token}`,

                ...(options.headers||{})
            }
        }
    );

    const data = await response.json();

    if(!response.ok){

        throw new Error(
            data.detail || "Request Failed"
        );

    }

    return data;

}

export function getSubjects(){

    return request("/subjects");

}

export function createSubject(subject){

    return request(

        "/subjects",

        {

            method:"POST",

            body:JSON.stringify(subject)

        }

    );

}