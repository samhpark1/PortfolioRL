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
        <div className='bg-white h-1/2 w-1/2 p-5'>
            <div ref={chartContainerRef} style={{width: 600, height: 400}}/>
        </div>
        
    )
}

export default StockViewer;
