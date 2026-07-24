import { useEffect, useState } from "react";

import { Header } from "../../components/UI";

import { uploadFile,getSubjects } from "../../lib/uploadApi";

export default function UploadMaterial() {

    const [subjects, setSubjects] = useState([]);

    const [subjectId, setSubjectId] = useState("");

    const [files, setFiles] = useState([]);

    const [loading, setLoading] = useState(false);

    const [success, setSuccess] = useState("");

    const [error, setError] = useState("");



    useEffect(() => {

        loadSubjects();

    }, []);



    async function loadSubjects() {

        try {

            const data = await getSubjects();

            setSubjects(data.subjects || data);

        }

        catch (err) {

            console.log(err);

        }

    }



    async function handleUpload() {

        setError("");

        setSuccess("");



        if (!subjectId) {

            setError("Please select subject.");

            return;

        }



        if (!file) {

            setError("Please choose study material.");

            return;

        }



        try {

            setLoading(true);
            for (const file of files){
            const form = new FormData();

            form.append("file", file);
            form.append("upload_category", "material");
            form.append("subject_id", String(subjectId));


            console.log("FILE SENT:", file);

            for (let pair of form.entries()) {
                console.log(pair[0], pair[1]);
            }


            const response = await uploadFile(form);
        }

            setSuccess(

            `Study Material uploaded successfully.

            Subject : ${response.subject?.name || "Selected Subject"}

            Knowledge Base Updated.`

            );



            document.getElementById("materialFile").value = "";

            setFile(null);

        }

        catch (err) {

            console.log("UPLOAD ERROR:",err);

            setError(
                typeof err.message === "string"
                ? err.message
                : JSON.stringify(err)
            );

        }

        finally {

            setLoading(false);

        }

    }



    return (

        <div className="space-y-8">

            <Header

                title="Upload Study Material"

                subtitle="Upload PDFs, PPTs and Notes for an existing subject."

            />



            <div className="rounded-xl p-8 max-w-3xl"style={{background:"#0F1629",border:"1px solid #1E2D4A"}}>

                <div className="space-y-6">

                    <div>

                        <label  className="block mb-2 font-medium" style={{color:"#E2E8F0"}} >

                            Select Subject

                        </label>

                        <select

                            value={subjectId}

                            onChange={(e)=>setSubjectId(e.target.value)}

                            className="w-full rounded-lg p-3 text-white outline-none"style={{background:"#141B30",border:"1px solid #1E2D4A"}}

                        >

                            <option value="">

                                Select Subject

                            </option>

                            {

                                subjects.map(subject=>(

                                    <option

                                        key={subject.id}

                                        value={subject.id}

                                    >

                                        {subject.name} ({subject.code})

                                    </option>

                                ))

                            }

                        </select>

                    </div>



                    <div>

                        <label  className="block mb-2 font-medium" style={{color:"#E2E8F0"}} >

                            Upload Study Material

                        </label>

                        <input
                            id="materialFile"
                            type="file"
                            multiple
                            accept="*/*"
                            onChange={(e)=>setFiles([...e.target.files])}
                        />

                    </div>



                    {

                        error &&

                        <div  className="rounded p-3 text-sm" style={{ background:"#450A0A", color:"#FCA5A5" }} >

                            {error}

                        </div>

                    }



                    {

                        success &&

                        <div className="rounded p-3 text-sm" style={{ background:"#052E16", color:"#86EFAC" }} >

                            {success}

                        </div>

                    }



                    <button

                        onClick={handleUpload}

                        disabled={loading}

                        className="px-6 py-3 rounded-lg text-white font-semibold"style={{background:"linear-gradient(135deg,#1D4ED8,#3B82F6)"}}>

                        {

                            loading

                            ?

                            "Uploading..."

                            :

                            "Upload Study Material"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}
