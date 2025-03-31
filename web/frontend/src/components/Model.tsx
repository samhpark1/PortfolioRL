function Model() {
    return(
        <div className="h-screen w-screen bg-purple-400 flex flex-col justify-center items-center p-10 gap-y-20">
            <h1 className="text-7xl text-white font-semibold p-10">Try it Out</h1>
            <p className="text-md text-white text-center">Give our model a shot! Select up to 10 unique ticker symbols for a portfolio. You'll get a suggestions on how much to buy, hold, or sell, tailored for each individual stock</p>
            <button className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-white transition-all [box-shadow:0px_6px_4px_#8200db] active:translate-y-[2px] active:shadow-none m-5">Lets Go!</button>
        </div>
    )
}

export default Model;