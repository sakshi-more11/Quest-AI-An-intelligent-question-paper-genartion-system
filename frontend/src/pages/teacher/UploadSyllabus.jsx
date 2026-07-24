import { useState } from "react";

import { Header } from "../../components/UI";
import { uploadFile } from "../../lib/uploadApi";

export default function UploadSyllabus() {

    const [subjectName, setSubjectName] = useState("");

    const [courseCode, setCourseCode] = useState("");

    const [file, setFile] = useState(null);

    const [loading, setLoading] = useState(false);

    const [success, setSuccess] = useState("");

    const [error, setError] = useState("");



    async function handleUpload() {

        setSuccess("");
        setError("");

        if (!subjectName.trim()) {
            setError("Enter Subject Name");
            return;
        }

        if (!courseCode.trim()) {
            setError("Enter Course Code");
            return;
        }

        if (!file) {
            setError("Select syllabus PDF");
            return;
        }

        try {

            setLoading(true);

            const form = new FormData();

            form.append("file", file);

            form.append("upload_category", "syllabus");

            form.append("subject_name", subjectName);

            form.append("course_code", courseCode);

            // subject_id intentionally left empty
            form.append("subject_id", "");

            const response = await uploadFile(form);

            setSuccess(
                `${response.subject.name} (${response.subject.code}) created successfully.
Knowledge Base Ready.
You can now upload Study Material.`
            );

            setSubjectName("");
            setCourseCode("");
            setFile(null);

            document.getElementById("syllabusFile").value = "";

        }

        catch (err) {

            console.log("SYLLABUS ERROR:",err);

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

                title="Upload Syllabus"

                subtitle="Create a subject by uploading its syllabus."

            />



            <div className="rounded-xl p-8 max-w-3xl"style={{background:"#0F1629",border:"1px solid #1E2D4A"}}>

                <div className="space-y-6">

                    <div>

                        <label  className="block mb-2 font-medium" style={{color:"#E2E8F0"}} >

                            Subject Name

                        </label>

                        <input

                            type="text"

                            className="w-full rounded-lg p-3 text-white outline-none"style={{background:"#141B30",border:"1px solid #1E2D4A"}}

                            placeholder="Operating System"

                            value={subjectName}

                            onChange={(e)=>setSubjectName(e.target.value)}

                        />

                    </div>



                    <div>

                        <label  className="block mb-2 font-medium" style={{color:"#E2E8F0"}} >

                            Course Code

                        </label>

                        <input

                            type="text"

                            className="w-full rounded-lg p-3 text-white outline-none"style={{background:"#141B30",border:"1px solid #1E2D4A"}}

                            placeholder="AI402"

                            value={courseCode}

                            onChange={(e)=>setCourseCode(e.target.value)}

                        />

                    </div>



                    <div>

                        <label  className="block mb-2 font-medium" style={{color:"#E2E8F0"}} >

                            Upload Syllabus

                        </label>

                        <input

                            id="syllabusFile"

                            type="file"

                            accept=".pdf"

                            onChange={(e)=>setFile(e.target.files[0])}

                        />

                    </div>



                    {error && (

                        <div className="bg-red-100 text-red-700 p-3 rounded">

                            {error}

                        </div>

                    )}



                    {success && (

                        <div className="bg-green-100 text-green-700 p-3 rounded whitespace-pre-line">

                            {success}

                        </div>

                    )}



                    <button

                        onClick={handleUpload}

                        disabled={loading}

                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"

                    >

                        {

                            loading

                                ? "Uploading..."

                                : "Upload Syllabus"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}