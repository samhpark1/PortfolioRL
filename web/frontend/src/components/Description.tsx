function Description() {

    return (
      <div className="h-screen bg-black flex flex-col p-10">
        <h1 className="text-4xl text-gray-200 font-bold py-10">Behind the Scenes</h1>
        <section className="flex flex-col gap-y-10 max-w-1/2">
          <section>
            <h2 className="text-xl text-gray-100">Our Dataset</h2>
            <ul className="text-gray-300 marker:text-gray-300 list-disc pl-5">
              <li>
                We obtained our historical data using 
                <a target="_blank" className="text-blue-300 hover:text-blue-500"href="https://pypi.org/project/yfinance/"> yfinance's </a>
                API.
              </li>
              <li>With 40,000 samples we cover the daily changes over the past 4 years of 20 unique stocks, specifically chosen for their distribution in volatility</li>
            </ul>
          </section>
          <section>
            <h2 className="text-xl text-gray-100">Model Architecture</h2>
            <ul className="text-gray-300 marker:text-gray-300 list-disc pl-5">
              <li>Our model is based off of the Proximal Policy Optimization (PPO) algorithm developed by
                <a target="_blank" className="text-blue-300 hover:text-blue-500" href="https://spinningup.openai.com/en/latest/algorithms/ppo.html"> OpenAI.</a>
              </li>
            </ul>
          </section>
        </section>
      </div>
    )
  }
  
  export default Description
  