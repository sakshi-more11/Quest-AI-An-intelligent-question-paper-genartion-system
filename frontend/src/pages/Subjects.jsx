import { useEffect, useState } from "react";

import { Header } from "../components/UI";

import {
    getSubjects,
    createSubject
} from "../lib/subjectApi";

export default function Subjects(){

    const [subjects,setSubjects] = useState([]);

    const [name,setName] = useState("");

    const [code,setCode] = useState("");

    const [semester,setSemester] = useState("");

    const [loading,setLoading] = useState(false);

    useEffect(()=>{
        loadSubjects();
    },[]);

    async function loadSubjects(){

        try{

            const data = await getSubjects();

            setSubjects(data);

        }catch(err){

            console.log(err);

        }

    }

    async function saveSubject(){

        if(!name || !code){

            alert("Please enter subject details");

            return;

        }

        setLoading(true);

        try{

            await createSubject({

                name,

                code,

                semester

            });

            setName("");
            setCode("");
            setSemester("");

            loadSubjects();

        }

        catch(err){

            alert(err.message);

        }

        setLoading(false);

    }

    return(

        <div>

            <Header
                title="Subjects"
                subtitle="Create and manage engineering subjects."
            />

            <div className="bg-white rounded-xl p-6 shadow mb-8">

                <h2 className="text-lg font-semibold mb-4">
                    Add Subject
                </h2>

                <div className="grid grid-cols-3 gap-4">

                    <input
                        placeholder="Subject Name"
                        className="border rounded p-2"
                        value={name}
                        onChange={(e)=>setName(e.target.value)}
                    />

                    <input
                        placeholder="Subject Code"
                        className="border rounded p-2"
                        value={code}
                        onChange={(e)=>setCode(e.target.value)}
                    />

                    <input
                        placeholder="Semester"
                        className="border rounded p-2"
                        value={semester}
                        onChange={(e)=>setSemester(e.target.value)}
                    />

                </div>

                <button
                    onClick={saveSubject}
                    disabled={loading}
                    className="mt-5 px-5 py-2 bg-blue-600 text-white rounded"
                >
                    {loading ? "Saving..." : "Add Subject"}
                </button>

            </div>

            <div className="bg-white rounded-xl shadow">

                <table className="w-full">

                    <thead className="bg-gray-100">

                        <tr>

                            <th className="p-3 text-left">Code</th>

                            <th className="p-3 text-left">Subject</th>

                            <th className="p-3 text-left">Semester</th>

                        </tr>

                    </thead>

                    <tbody>

                        {subjects.map(subject=>(

                            <tr key={subject.id}>

                                <td className="p-3">{subject.code}</td>

                                <td className="p-3">{subject.name}</td>

                                <td className="p-3">{subject.semester}</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>

    );

}