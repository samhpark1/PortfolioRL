import Arrow from "./Arrow";
import PipelineElement from "./PipelineElement";

function Pipeline() {
    return (
        <div className="flex flex-col justify-center items-center h-screen bg-gradient-to-b from-black to-purple-400">
            <h1 className="font-bold text-7xl text-purple-600 pb-20">Our Pipeline</h1>
            <section className="flex">
                <PipelineElement title="Data Scraping" description="Obtain data from yfinance API with data_scraper.py"/>
                <Arrow />
                <PipelineElement title="Data Cleaning" description="Clean data using our data_cleaner.py"/>
                <Arrow />
                <PipelineElement title="Training" description="Train model using PPO algorithm" />
                <Arrow />
                <PipelineElement title="Web Backend" description="Implement model into website API" />
            </section>
        </div>
    );
}
  
export default Pipeline;
  