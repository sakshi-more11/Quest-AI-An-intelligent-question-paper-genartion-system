// src/components/TeacherCard.jsx

export default function TeacherCard({
  teacher,
  onEdit,
  onDisable,
  onDelete
}) {

return (

<div
className="rounded-3xl p-6 mb-5"
style={{
background:"#050B18",
border:"1px solid #1E293B"
}}
>


<div className="flex justify-between items-start">


<div className="flex gap-4">


<div
className="w-14 h-14 rounded-full flex items-center justify-center text-xl font-bold"
style={{
background:"#2563EB",
color:"#fff"
}}
>
{
teacher.full_name?.charAt(0)
}
</div>



<div>

<h3
className="text-lg font-semibold"
style={{
color:"#F8FAFC"
}}
>
{teacher.full_name}
</h3>


<p
className="text-sm"
style={{
color:"#94A3B8"
}}
>
{teacher.email}
</p>


</div>


</div>



<span
className="px-3 py-1 rounded-full text-xs"
style={{
background:
teacher.is_active
?
"#064E3B"
:
"#7F1D1D",

color:
teacher.is_active
?
"#4ADE80"
:
"#FCA5A5"
}}
>

{
teacher.is_active
?
"Active"
:
"Disabled"
}

</span>


</div>





<div className="grid grid-cols-3 gap-5 mt-6">


<div>

<p className="text-xs text-slate-500">
Designation
</p>

<p className="text-sm text-white">
{teacher.designation || "-"}
</p>

</div>




<div>

<p className="text-xs text-slate-500">
Department
</p>

<p className="text-sm text-white">
{teacher.department || "-"}
</p>

</div>




<div>

<p className="text-xs text-slate-500">
Subject
</p>

<p className="text-sm text-white">
{teacher.subject || "-"}
</p>

</div>


</div>





<div className="flex justify-end gap-3 mt-6">


<button
onClick={()=>onEdit(teacher)}
className="px-5 py-2 rounded-xl"
style={{
background:"#2563EB",
color:"#fff"
}}
>
✏️ Edit
</button>




<button
onClick={()=>onDisable(teacher)}
className="px-5 py-2 rounded-xl"
style={{
background:
teacher.is_active
?
"#92400E"
:
"#166534",

color:"#fff"
}}
>

{
teacher.is_active
?
"Disable"
:
"Enable"
}

</button>




<button
onClick={()=>onDelete(teacher)}
className="px-5 py-2 rounded-xl"
style={{
background:"#DC2626",
color:"#fff"
}}
>
🗑 Delete
</button>


</div>


</div>

);

}