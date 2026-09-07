// src/pages/LoginPage.jsx

import {
  useState
} from "react";

import {
  login
} from "../lib/api";


export default function LoginPage({
  onLogin,
  theme,
  onToggleTheme,
}){


  const [email,setEmail] = useState("");

  const [password,setPassword] = useState("");

  const [error,setError] = useState("");

  const [loading,setLoading] = useState(false);



  const attempt = async()=>{


    if(!email || !password){

      setError("Please enter email and password");
      return;

    }


    setLoading(true);

    setError("");



    try{


      const data = await login(
        email,
        password
      );

      const userNames = {

        "teacher1@questai.com": "Prof. Priya Sharma",

        "teacher2@questai.com": "Prof. Arjun Verma",

        "admin@questai.com": "Dr. Raj Mehta"

      };

      const user = {
          role: data.role,
          email: data.email,

          name:
            data.role === "admin"
              ? "Dr. Raj Mehta"
              : data.email.includes("teacher1")
              ? "Prof. Priya Sharma"
              : "Prof. Arjun Verma",

          username: data.email,
          token: data.access_token,
      };



      localStorage.setItem(
      "user",
      JSON.stringify(user)
      );


      localStorage.setItem(
      "token",
      data.access_token
      );



      onLogin(user);



    }

    catch(err){


      setError(
        err.message || "Login failed"
      );


    }


    finally{


      setLoading(false);


    }


  };





return (

<div
className="min-h-screen flex items-center justify-center px-4 login-screen"
style={{
background:"#08121F"
}}
>

<button type="button" onClick={onToggleTheme} aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} theme`} title={`Switch to ${theme === "dark" ? "light" : "dark"} theme`} className="theme-icon-toggle">
{theme === "dark" ? <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg> : <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/></svg>}
</button>


<div
className="
w-full max-w-4xl
overflow-hidden
rounded-[32px]
border border-slate-800
bg-slate-950/90
shadow-[0_32px_70px_rgba(15,23,42,0.35)]
login-card
"
>


<div
className="
grid md:grid-cols-[1.2fr_1fr]
"
>



{/* LEFT SIDE */}

<div
className="p-10 md:p-14"
style={{
background:
"linear-gradient(180deg, rgba(15,23,42,1), rgba(15,23,42,0.86))"
}}
>


<div className="mb-8">


<div className="login-logo mb-5" aria-label="QuestAI logo"><span>Q</span><div><strong>QuestAI</strong><small>QUESTION PAPER SYSTEM</small></div></div>



<h1
className="text-3xl font-semibold"
style={{
color:"#F8FAFC"
}}
>
QuestAI
</h1>



<p
className="
mt-3
max-w-sm
text-sm
leading-6
"
style={{
color:"#94A3B8"
}}
>
Intelligent AI based question paper generation system.
Manage syllabus, generate questions and create examination papers.
</p>


</div>


</div>





{/* RIGHT SIDE */}

<div
className="p-10 md:p-14"
>


<h2
className="text-2xl font-semibold"
style={{
color:"#F8FAFC"
}}
>
Welcome back
</h2>



<p
className="
mt-2
text-sm
text-slate-400
"
>
Login using your registered email.
</p>





{
error &&

<div
className="
mt-5
rounded-3xl
border
border-red-500/20
bg-red-500/10
px-4
py-3
text-sm
text-red-200
"
>

{error}

</div>

}






<div className="space-y-5 mt-6">



{/* EMAIL */}

<div>


<label
className="
block
text-xs
font-medium
text-slate-400
mb-2
"
>
Email
</label>



<input

type="email"

value={email}

onChange={
e=>setEmail(e.target.value)
}

onKeyDown={
e=>e.key==="Enter" && attempt()
}

className="
w-full
rounded-2xl
border
border-slate-800
bg-slate-950
px-4
py-3
text-sm
text-slate-100
outline-none
focus:border-sky-500
"

placeholder="admin@questai.com"

/>


</div>





{/* PASSWORD */}

<div>


<label
className="
block
text-xs
font-medium
text-slate-400
mb-2
"
>
Password
</label>



<input

type="password"

value={password}

onChange={
e=>setPassword(e.target.value)
}

onKeyDown={
e=>e.key==="Enter" && attempt()
}

className="
w-full
rounded-2xl
border
border-slate-800
bg-slate-950
px-4
py-3
text-sm
text-slate-100
outline-none
focus:border-sky-500
"

placeholder="••••••••"

/>


</div>







<button

onClick={attempt}

disabled={loading}

className="
w-full
rounded-2xl
bg-sky-600
px-4
py-3
text-sm
font-semibold
text-white
hover:bg-sky-500
disabled:bg-slate-700
"

>


{
loading
?
"Signing in..."
:
"Sign in"
}


</button>



</div>



</div>



</div>


</div>


</div>


);


}
