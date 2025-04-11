function Navbar() {

    return (
        <div className="bg-transparent w-screen flex flex-row justify-end font-bold text-gray-200 text-xl z-10 absolute left-0 top-0 p-5">
            <span className="flex flex-row font-normal space-x-10 text-md">
                <button className="hover:text-gray-500">About</button>
                <button className="hover:text-gray-500">Run Model</button>
            </span>
        </div>
    )
  }
  
  export default Navbar
  