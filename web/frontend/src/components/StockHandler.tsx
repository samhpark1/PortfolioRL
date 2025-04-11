import StockChooser from "./StockChooser";
import StockViewer from "./StockViewer";

function StockHandler() {

    return (
        <div className="flex flex-col bg-white rounded-3xl m-5">
            <section className="flex justify-center items-center">
                <StockChooser />
                <StockViewer stocks={[
                    { time: '2018-12-22', value: 45.72 },
                    { time: '2018-12-23', value: 48.09 },
                    { time: '2018-12-24', value: 59.29 },
                    { time: '2018-12-25', value: 60.50 },
                    { time: '2018-12-26', value: 91.04 },
                    { time: '2018-12-27', value: 111.40 },
                    { time: '2018-12-28', value: 131.25 },
                    { time: '2018-12-29', value: 96.43 },
                    { time: '2018-12-30', value: 98.10 },
                    { time: '2018-12-31', value: 111.26 }]}/>
            </section>

        </div>
    )

}

export default StockHandler;