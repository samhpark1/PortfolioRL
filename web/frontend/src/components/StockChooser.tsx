import {useState} from 'react'
import {tickers} from '../assets/tickers.ts'

interface ComponentProps {
    setPortfolio: React.Dispatch<React.SetStateAction<string[][]>>;
}

function StockChooser({setPortfolio}: ComponentProps){
    const [stock, setStock] = useState("");
    const [price, setPrice] = useState("");
    const [error, setError] = useState("");

    const handleStockInputChange = (e: { target: { value: string; }; }) => {
        const val = e.target.value;
        setStock(val);
        console.log(stock);
    }

    const handlePriceInputChange = (e: {target: {value: string;}; }) => {
        const val = e.target.value;
        setPrice(val);
        console.log(price);
    }

    const submitHandler = () => {        
        const pattern = /^(?!\b0(\.0+)?\b)(?!\b0(\.\d+)?\b)(\$?\d{1,3}(,\d{3})*(\.\d{2})?)$/;
        const isDollar = pattern.test(price);
        const isTicker = tickers.includes(stock.toUpperCase());

        if (isDollar && isTicker){
            //user setter function passed by parent
            setError("");
            setStock("");
            setPrice("");
            setPortfolio(prev => [...prev, [stock, price]])
            
        }
        else{
            if (!isDollar){
                setError("Please enter a valid dollar amount");
            }
            if (!isTicker){
                setError("Please enter a valid ticker symbol");
            }
            console.log(error);
        }
    }

    return (
        <div className='flex flex-col bg-white w-1/4 h-1/3 rounded-2xl shadow-2xl p-10 border-2 border-violet-300'>
            <h1>Stock Ticker</h1>
            <input
                type="text"
                value={stock}
                onChange={handleStockInputChange}
                placeholder="AAPL"
                className='border-2 border-violet-300 rounded-full mb-5'
                style={{ width: "100%", padding: "8px" }}
            />
            <h1>Stock Amount</h1>
            <input
                type="text"
                value={price}
                onChange={handlePriceInputChange}
                className='border-2 border-violet-300 rounded-full mb-5'
                style={{ width: "100%", padding: "8px" }}
                placeholder="$0.00"
            />
            {error.length > 0 &&
                <h1 className='pb-5 text-red-600'>{error}</h1>
            }
            <button
                onClick={submitHandler}
                className='rounded-full bg-violet-600 hover:bg-violet-700 text-neutral-100 p-2'
            >
                Add
            </button>
        </div>
    )

}

export default StockChooser;