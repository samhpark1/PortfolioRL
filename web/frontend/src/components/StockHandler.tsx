import ModelResult from "./ModelResult";
import StockChooser from "./StockChooser";
import StockViewer from "./StockViewer";

import {useEffect, useState} from 'react';

interface StockData {
    time: string;
    value: number;
}

function StockHandler() {

    const [portfolio, setPortfolio] = useState<string[][]>([]);
    const [timeSeries, setTimeSeries] = useState<StockData[]>([])

    useEffect(() => {
        const fetchSeries = async () => {
            if (portfolio.length == 0) return;
            console.log(JSON.stringify(portfolio));
            try {
                const response = await fetch("http://127.0.0.1:5000/api/hist", {
                    method: "POST",
                    headers: {
                        "Content-Type": "applications/json",
                    },
                    body: JSON.stringify(portfolio),
                })
                if (!response.ok){
                    throw new Error("API call for time series failed");
                }
                
                const data = await response.json();
                console.log(data);
            }
            catch(err){
                console.log("API call no workies")
            }
        };

        fetchSeries();
    }, [portfolio, timeSeries]);

    return (
        <div className="flex flex-col justify-center items-center p-10">
            <h1 className="font-semibold text-5xl text-neutral-200 py-10">Your Portfolio's Historical Performance</h1>
            <section className="flex w-[90vw] bg-white rounded-3xl justify-around items-center py-10">
                <StockChooser setPortfolio={setPortfolio}/>
                <StockViewer stocks={timeSeries} />
                {/* <StockViewer stocks = {[{ time: '2018-12-22', value: 45.72 },
                    { time: '2018-12-23', value: 48.09 },
                    { time: '2018-12-24', value: 59.29 },
                    { time: '2018-12-25', value: 60.50 },
                    { time: '2018-12-26', value: 91.04 },
                    { time: '2018-12-27', value: 111.40 },
                    { time: '2018-12-28', value: 131.25 },
                    { time: '2018-12-29', value: 96.43 },
                    { time: '2018-12-30', value: 98.10 },
                    { time: '2018-12-31', value: 111.26 },
                    { time: '2019-01-01', value: 115.30 },
                    { time: '2019-01-02', value: 119.85 },
                    { time: '2019-01-03', value: 116.00 }, 
                    { time: '2019-01-04', value: 122.40 },
                    { time: '2019-01-05', value: 127.00 },
                    { time: '2019-01-06', value: 124.20 },  
                    { time: '2019-01-07', value: 130.50 },
                    { time: '2019-01-08', value: 138.90 },
                    { time: '2019-01-09', value: 134.75 }, 
                    { time: '2019-01-10', value: 142.80 },
                    { time: '2019-01-11', value: 145.10 },
                    { time: '2019-01-12', value: 149.60 },
                    { time: '2019-01-13', value: 147.20 },  
                    { time: '2019-01-14', value: 153.90 },
                    { time: '2019-01-15', value: 160.75 },
                    { time: '2019-01-16', value: 158.10 },
                    { time: '2019-01-17', value: 164.00 },
                    { time: '2019-01-18', value: 171.50 }]}
                    /> */}
            </section>
            <ModelResult stocks={portfolio}/>

        </div>
    )

}

export default StockHandler;