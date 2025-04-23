import { useEffect } from 'react';

interface ComponentProps {
  stocks: string[][];
}

function ModelResult({ stocks }: ComponentProps) {

  useEffect(() => {
  }, [stocks])

  return (
    <div className='flex flex-col bg-white w-[90vw] h-[40vw] items-center justify-center rounded-3xl mt-10'>
      <h1 className='text-5xl font-semibold text-violet-950 p-10'>Your Portfolio</h1>
      <div className="flex flex-col items-center justify-start bg-white w-[70vw] h-[20vw] rounded-3xl overflow-y-auto p-10 border-2 border-violet-400">
        {stocks.map((item, index) => (
          <div 
            key={index} 
            className="w-full bg-gray-200 rounded-md p-4 mb-4 shadow-md flex justify-between items-center"
          >
            <span className="text-lg font-medium text-gray-800">{item[0]}</span>
          </div>
        ))}
      </div>
      <button className='bg-violet-600 hover:bg-violet-700 text-neutral-100 font-semibold p-5 rounded-full m-10'>Get Suggestions</button>
    </div>
  )
}

export default ModelResult;
