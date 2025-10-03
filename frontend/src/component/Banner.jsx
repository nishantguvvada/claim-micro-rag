export const Banner = () => {
    return (
        <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">
            <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white"><span className="text-transparent bg-clip-text bg-gradient-to-r to-slate-600 from-rose-400">RAG</span> powered chat interface for insurance</h1>
            <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">Claim-Micro-RAG.ai is powered by AI to delivers instant answers on the tedious insurance claim procedures.</p>
            <div className="pt-4 flex flex-col gap-2">
                <div className="pt-2 px-4 h-96 flex flex-col gap-4 text-center">
                    <span className="font-semibold text-gray-400 uppercase">Claim-Micro-RAG features 2 tools accessible via the askgraph endpoint.</span>
                    <div className="flex flex-row gap-4 h-64 justify-center items-center mt-8 sm:justify-between">
                        <div className="p-8 w-full h-full flex flex-col gap-4 justify-center items-center shadow-xl rounded-lg hover:bg-gray-100 hover:cursor-pointer">
                            <h1 className="mb-2 text-xl font-semibold leading-none tracking-tight">Retrieval Tool</h1>
                            <p className="p-2 text-justify">Our AI-powered assistant connects to the RAG vector store via Retrieval Tool to retrieve and present clear facts on insurance claim procedure.</p>
                        </div>
                        <div className="p-8 w-full h-full flex flex-col gap-4 justify-center items-center shadow-xl rounded-lg hover:bg-gray-100 hover:cursor-pointer">
                            <h1 className="mb-2 text-xl font-semibold leading-none tracking-tight">User Feedback Tool</h1>
                            <p className="p-2 text-justify">A tool to fetch more information from the user.</p>
                        </div>
                    </div>
                </div> 
            </div>
        </div>
    )
}