import { Card } from "./UI";

export default function AccessDenied() {

    return (

        <Card>

            <div className="text-center py-20">

                <h2
                    className="text-3xl font-bold text-red-400"
                >
                    Access Denied
                </h2>

                <p
                    className="text-slate-400 mt-3"
                >
                    You do not have permission to access this page.
                </p>

            </div>

        </Card>

    );

}