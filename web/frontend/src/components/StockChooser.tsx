import {useState} from 'react'

function StockChooser(){
    const [stock, setStock] = useState("");
    const [price, setPrice] = useState("");

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
        
    }

    return (
        <div className='flex flex-col gap-y-5 bg-white w-1/4 h-1/3'>
            <h1>Stock Ticker</h1>
            <input
                type="text"
                value={stock}
                onChange={handleStockInputChange}
                placeholder="AAPL"
                style={{ width: "100%", padding: "8px" }}
            />
            <h1>Stock Amount</h1>
            <input
                type="text"
                value={price}
                onChange={handlePriceInputChange}
                placeholder="$0.00"
            />
            <button
                onClick={submitHandler}
            >
                Add
            </button>
        </div>
    )

}

export default StockChooser;