import { useEffect, useState } from "react";

import { Header } from "../components/UI";

import UploadDropzone from "../components/UploadDropzone";

import FileCard from "../components/FileCard";

import {
    getUploads,
    uploadFile,
    deleteUpload
} from "../lib/uploadApi";

import { getSubjects } from "../lib/subjectApi";


export default function UploadCenter() {

    const [subjects, setSubjects] = useState([]);

    const [selectedSubject, setSelectedSubject] = useState("");

    const [uploads, setUploads] = useState([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        loadSubjects();

        loadUploads();

    }, []);

    async function loadSubjects() {

        try {

            const data = await getSubjects();

            setSubjects(data);

        }

        catch (err) {

            console.log(err);

        }

    }

    async function loadUploads() {

    try {

        const data = await getUploads();

        console.log("UPLOADS RESPONSE:", data);

        setUploads(Array.isArray(data) ? data : data.files || []);

    }

    catch (err) {

        console.log(err);

    }

}

    async function upload(files) {

    if (!selectedSubject) {

        alert("Please select a subject first.");
        return;

    }

    try {

        setLoading(true);

        for (const file of files) {

            const form = new FormData();

            form.append("file", file);
            form.append("upload_category", "material");
            form.append("subject_id", selectedSubject);

            await uploadFile(form);

        }

        await loadUploads();

        alert("Study Material uploaded successfully.");

    }

    catch (err) {

        alert(err.message);

    }

    finally {

        setLoading(false);

    }

}
const groupedUploads = uploads.reduce((acc, file) => {

    const subject = file.subject_name || "Unknown Subject";

    if (!acc[subject]) {

        acc[subject] = [];

    }

    acc[subject].push(file);
    return acc;

}, {});
async function handleDelete(id){

    const ok=

    window.confirm(

        "Delete this file?"

    );

    if(!ok)

        return;

    try{

        await deleteUpload(id);

        loadUploads();

    }

    catch(err){

        alert(err.message);

    }

}

    return (

        <div>

            <Header

                title="Upload Study Material"

                subtitle="Upload PDFs, PPTs and Notes. These materials will be linked with the selected subject and used for automatic Question Bank generation."

            />

            <div className="rounded-xl p-6" style={{background:"#0F1629",border:"1px solid #1E2D4A"}}>


                <label className="block font-medium mb-2">

                    Select Subject

                </label>

                <select

                    className="rounded-lg p-3 w-full"style={{background:"#141B30",border:"1px solid #1E2D4A",color:"#E2E8F0"}}

                    value={selectedSubject}

                    onChange={(e) => setSelectedSubject(e.target.value)}

                >

                    <option value="">

                        -- Select Subject --

                    </option>

                    {

                        subjects.map((subject) => (

                            <option

                                key={subject.id}

                                value={subject.id}

                            >

                                {subject.code} - {subject.name}

                            </option>

                        ))

                    }

                </select>

                <div className="mt-6">

                    <UploadDropzone

                        type="Study Material"

                        onUpload={upload}

                    />

                </div>

                {

                    loading &&

                    <p className="mt-4 text-blue-600">

                        Uploading...

                    </p>

                }

            </div>

            <div className="mt-10">

    <h2
        className="text-xl font-semibold mb-6"
        style={{ color:"#E2E8F0" }}
    >
        Uploaded Study Materials
    </h2>

    {

        uploads.length===0 ?

        (

            <div
                className="rounded-xl p-12 text-center"
                style={{
                    background:"#0F1629",
                    border:"1px solid #1E2D4A"
                }}
            >

                <div className="text-6xl">

                    📂

                </div>

                <p
                    className="mt-4"
                    style={{color:"#94A3B8"}}
                >
                    No files uploaded yet.
                </p>

            </div>

        )

        :
        Object.entries(groupedUploads).map(([subjectName, files]) => (

    <div
        key={subjectName}
        className="mb-8"
    >

        <div className="flex items-center gap-2 mb-2">

            <span
                style={{
                    fontSize:"18px"
                }}
            >
                📚
            </span>

            <h3
                className="font-semibold"
                style={{
                    color:"#E2E8F0",
                    fontSize:"18px"
                }}
            >
                {subjectName}
            </h3>

            <span
                className="text-xs"
                style={{
                    color:"#64748B"
                }}
            >
                ({files.length} files)
            </span>

        </div>

        <div
            style={{
                height:"1px",
                background:"#1E2D4A",
                marginBottom:"18px"
            }}
        />

        <div
            className="
            grid
            grid-cols-1
            md:grid-cols-2
            lg:grid-cols-3
            gap-4
            "
        >

            {

                files.map(file => (

                    <FileCard
                        key={file.id}
                        file={file}
                        onDelete={handleDelete}
                    />

                ))

            }

        </div>

    </div>

))
}
        

</div>

       

        </div>

    );

}