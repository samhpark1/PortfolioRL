import { useEffect, useRef } from 'react';
import { createChart, ColorType, AreaSeries } from 'lightweight-charts';

interface StockData {
    time: string;
    value: number;
}

interface ComponentProps {
    stocks: StockData[];
}

function StockViewer({ stocks }: ComponentProps) {
    const chartContainerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (!chartContainerRef.current) return;

        const chartOptions = { layout: { textColor: 'black', background: { type: ColorType.Solid, color: 'white' } } };
        const chart = createChart(chartContainerRef.current, chartOptions);
        const areaSeries = chart.addSeries(AreaSeries, { lineColor: '#8e51ff', topColor: '#8e51ff', bottomColor: 'rgba(255, 130, 255, 0.28)' });

        areaSeries.setData(stocks);

        chart.timeScale().fitContent();

        return () => chart.remove();
    }, []);

    return (
        <div className='bg-white border-2 border-violet-200 flex flex-col justify-center items-center h-1/2 w-1/2 p-5 gap-y-5 rounded-2xl'>
            <h1 className="font-semibold">Your Portfolio's Historical Performance</h1>
            <div ref={chartContainerRef} style={{width: 600, height: 400}}/>
        </div>
        
    )
}

export default StockViewer;
