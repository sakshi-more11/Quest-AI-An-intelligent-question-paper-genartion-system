// src/lib/questionBankApi.js

const API_BASE =
    process.env.REACT_APP_API_BASE ||
    "http://127.0.0.1:8000";


// ------------------------------------
// Get Question Bank by Subject
// ------------------------------------

export async function getQuestionBank(subjectId){


    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const token = user.token;


    const response = await fetch(

        `${API_BASE}/question-bank/${subjectId}`,

        {

            method:"GET",

            headers:{

                "Accept":"application/json",

                "Authorization":
                `Bearer ${token}`

            }

        }

    );



    if(!response.ok){

        const error =
            await response.json();

        throw new Error(
            error.detail ||
            "Failed to fetch question bank"
        );

    }



    return await response.json();

}




// ------------------------------------
// Generate Question Bank
// ------------------------------------

export async function generateQuestionBank(subjectId){

    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const token = user.token;

    const response = await fetch(
        `${API_BASE}/question-bank/generate/${subjectId}`,
        {
            method:"POST",
            headers:{
                "Accept":"application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || data.error || "Failed to generate question bank");
    }
    return data;
}
// ------------------------------------
// Fetch Questions By Subject
// ------------------------------------

export async function fetchQuestions(subjectId){


    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const token = user.token;


    const response =
    await fetch(

        `${API_BASE}/question-bank/${subjectId}`,

        {

            headers:{

                Authorization:
                `Bearer ${token}`

            }

        }

    );



    if(!response.ok){

        throw new Error(
            "Unable to load questions"
        );

    }


    return await response.json();

}
