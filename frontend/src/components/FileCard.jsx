import { Card } from "./UI";

export default function FileCard({

    file,

    onDelete

}){

    const ext=file.file_type?.toLowerCase();

    let icon="📄";

    if(ext===".pdf") icon="📕";

    if(ext===".ppt"||ext===".pptx") icon="📙";

    if(ext===".doc"||ext===".docx") icon="📘";

    return(

        <Card>

            <div className="flex justify-between items-center">

                <div className="flex items-center gap-3">

                    <span
                        style={{
                            fontSize:"22px"
                        }}
                    >

                        {icon}

                    </span>

                    <div>

                        <div
                            className="font-medium"
                            style={{
                                color:"#E2E8F0"
                            }}
                        >

                            {file.filename}

                        </div>

                        <div
                            className="text-xs"
                            style={{
                                color:"#64748B"
                            }}
                        >

                            {file.file_type}

                        </div>

                    </div>

                </div>

                <button

                    onClick={()=>onDelete(file.id)}

                    className="px-3 py-1 rounded"

                    style={{

                        background:"#991B1B",

                        color:"white"

                    }}

                >

                    🗑

                </button>

            </div>

        </Card>

    );

}