// src/pages/TeacherManagement.jsx

import { useMemo, useState, useEffect } from "react";

import { Header, Stat, Card } from "../components/UI";

import TeacherCard from "../components/TeacherCard";
import TeacherModal from "../components/TeacherModal";
import ConfirmDialog from "../components/ConfirmDialog";

import {
  getTeachers,
  createTeacher,
  updateTeacher,
  deleteTeacher,
  enableTeacher,
  disableTeacher
} from "../lib/api";


export default function TeacherManagement() {


  const [teachers,setTeachers] = useState([]);

  const [loading,setLoading] = useState(true);

  const [error,setError] = useState("");

  const [search,setSearch] = useState("");


  const [modalOpen,setModalOpen] = useState(false);

  const [editingTeacher,setEditingTeacher] = useState(null);


  const [confirmOpen,setConfirmOpen] = useState(false);

  const [confirmMode,setConfirmMode] = useState("");

  const [selectedTeacher,setSelectedTeacher] = useState(null);



  // -----------------------------------------
  // LOAD TEACHERS
  // -----------------------------------------

  const loadTeachers = async()=>{

    try{

      setLoading(true);

      const data = await getTeachers();

      setTeachers(
        data.teachers || data
      );

      setError("");

    }

    catch(err){

      console.log(err);

      setError(err.message);

    }

    finally{

      setLoading(false);

    }

};



  useEffect(()=>{

    loadTeachers();

  },[]);





  // -----------------------------------------
  // SEARCH
  // -----------------------------------------

  const filteredTeachers = useMemo(()=>{


    return teachers.filter(t=>{


      const value = (

        t.full_name +

        t.email +

        t.department +

        t.subject

      )
      .toLowerCase();


      return value.includes(
        search.toLowerCase()
      );


    });


  },[teachers,search]);





  const activeTeachers =
    teachers.filter(
      t=>t.is_active
    ).length;



  const disabledTeachers =
    teachers.filter(
      t=>!t.is_active
    ).length;





  // -----------------------------------------
  // ADD
  // -----------------------------------------

  const openAddModal = ()=>{

    setEditingTeacher(null);

    setModalOpen(true);

  };




  // -----------------------------------------
  // EDIT
  // -----------------------------------------

  const openEditModal=(teacher)=>{

    setEditingTeacher(teacher);

    setModalOpen(true);

  };





  // -----------------------------------------
  // SAVE
  // -----------------------------------------

  const saveTeacher = async(data)=>{

    console.log("FRONTEND FORM DATA:", data);

    try{

      if(editingTeacher){

        await updateTeacher(
          editingTeacher.id,
          data
        );

      }
      else{

        await createTeacher(data);

      }


      setModalOpen(false);
      setEditingTeacher(null);

      loadTeachers();


    }
    catch(err){

      console.log("ERROR:", err);

      alert(err.message);

    }

};




  // -----------------------------------------
  // ENABLE DISABLE
  // -----------------------------------------

  const openStatusDialog=(teacher)=>{


    setSelectedTeacher(teacher);


    setConfirmMode(

      teacher.is_active

      ?

      "disable"

      :

      "enable"

    );


    setConfirmOpen(true);


  };





  // -----------------------------------------
  // DELETE
  // -----------------------------------------

  const openDeleteDialog=(teacher)=>{


    setSelectedTeacher(teacher);

    setConfirmMode("delete");

    setConfirmOpen(true);


  };





  const confirmAction = async()=>{


    if(!selectedTeacher)
      return;



    try{


      if(confirmMode==="delete"){


        await deleteTeacher(

          selectedTeacher.id

        );


      }


      else if(confirmMode==="disable"){


        await disableTeacher(

          selectedTeacher.id

        );


      }


      else{


        await enableTeacher(

          selectedTeacher.id

        );


      }



      setConfirmOpen(false);

      setSelectedTeacher(null);


      loadTeachers();



    }

    catch(err){

 console.error(
   "Teacher API Error:",
   err
 );


 alert(
   err.message || "Something went wrong"
 );

}


  };







return (

<div>


<Header

title="Teacher Management"

subtitle="Manage all faculty members of QuestAI"

/>



<div className="grid grid-cols-4 gap-4 mb-6">


<Stat

label="Total Teachers"

value={teachers.length}

color="#2563EB"

/>


<Stat

label="Active"

value={activeTeachers}

color="#16A34A"

/>


<Stat

label="Disabled"

value={disabledTeachers}

color="#F59E0B"

/>


<Stat

label="Departments"

value={
new Set(
teachers.map(
t=>t.department
)
).size
}

color="#8B5CF6"

/>


</div>





<Card className="mb-5">


<div className="flex justify-between items-center">


<div>

<h2

className="text-xl font-semibold"

style={{
color:"#F8FAFC"
}}

>

Faculty Members

</h2>


<p

className="text-sm mt-1"

style={{
color:"#94A3B8"
}}

>

Add, edit, disable or remove teachers.

</p>


</div>



<button

onClick={openAddModal}

className="px-5 py-3 rounded-2xl"

style={{

background:"#2563EB",

color:"#fff"

}}

>

➕ Add Teacher

</button>



</div>




<input

type="text"

placeholder="Search teacher..."

value={search}

onChange={
e=>setSearch(e.target.value)
}

className="
w-full mt-5 rounded-2xl
px-4 py-3
bg-slate-900
border border-slate-700
text-white
"

/>


</Card>






{
loading ?


<Card>

<p className="text-center py-8 text-slate-400">

Loading teachers...

</p>


</Card>



:


error ?


<Card>

<p className="text-center py-8 text-red-400">

{error}

</p>


</Card>



:


filteredTeachers.map(teacher=>(


<TeacherCard

key={teacher.id}

teacher={teacher}

onEdit={openEditModal}

onDisable={openStatusDialog}

onDelete={openDeleteDialog}

/>


))


}





<TeacherModal


open={modalOpen}


teacher={editingTeacher}


onClose={()=>{

setModalOpen(false);

setEditingTeacher(null);

}}


onSave={saveTeacher}


/>






<ConfirmDialog


open={confirmOpen}


title={

confirmMode==="delete"

?

"Delete Teacher"

:

confirmMode==="disable"

?

"Disable Teacher"

:

"Enable Teacher"

}



message={

confirmMode==="delete"

?

`Delete ${selectedTeacher?.full_name}?`

:

confirmMode==="disable"

?

`Disable ${selectedTeacher?.full_name}?`

:

`Enable ${selectedTeacher?.full_name}?`

}



confirmText={

confirmMode==="delete"

?

"Delete"

:

confirmMode==="disable"

?

"Disable"

:

"Enable"

}



onCancel={()=>{

setConfirmOpen(false);

setSelectedTeacher(null);

}}



onConfirm={confirmAction}


/>



</div>


);


}