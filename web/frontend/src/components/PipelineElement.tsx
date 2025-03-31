interface ComponentProps{
    title: string;
    description: string;
}

function PipelineElement({title, description}: ComponentProps){
    return(
        <div className="border-2 border-purple-700 bg-purple-200 font-extrabold p-5 rounded-xl max-w-40 shadow-2xl">
            <h1 className="text-purple-500">{title}</h1>
            <p className="text-[0.5rem] font-normal">{description}</p>
        </div>
    )
}

export default PipelineElement;