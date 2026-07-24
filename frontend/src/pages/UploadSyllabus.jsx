import { useState } from "react";

import { Header } from "../components/UI";

import UploadDropzone from "../components/UploadDropzone";

import { uploadFile } from "../lib/uploadApi";

export default function UploadSyllabus(){

const [subjectName,setSubjectName]=useState("");

const [courseCode,setCourseCode]=useState("");

const [loading,setLoading]=useState(false);

async function upload(file){

if(!subjectName){

alert("Enter Subject Name");

return;

}

if(!courseCode){

alert("Enter Course Code");

return;

}

const form=new FormData();

form.append("file",file);

form.append("upload_category","syllabus");

form.append("subject_name",subjectName);

form.append("course_code",courseCode);

setLoading(true);

await uploadFile(form);

setLoading(false);

alert("Syllabus Uploaded Successfully");

}

return(

<div>

<Header

title="Upload Syllabus"

subtitle="Create subject and upload syllabus."

/>

<div className="bg-white rounded-xl shadow p-6">

<label>

Subject Name

</label>

<input

className="border rounded-lg p-3 w-full"

value={subjectName}

onChange={(e)=>setSubjectName(e.target.value)}

/>

<label className="mt-5 block">

Course Code

</label>

<input

className="border rounded-lg p-3 w-full"

value={courseCode}

onChange={(e)=>setCourseCode(e.target.value)}

/>

<div className="mt-6">

<UploadDropzone

type="Syllabus"

onUpload={upload}

/>

</div>

</div>

</div>

);

}