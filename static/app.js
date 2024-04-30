const ctx = document.getElementById('stockChart').getContext('2d');
let stockChart;
let stockData = []; // This will hold stock data

document.addEventListener('DOMContentLoaded', function() {
    initializeSelect2();
    fetchStockData();
});

function initializeSelect2() {
    $('#searchInput').select2({
        placeholder: "Search for a stock...",
        minimumInputLength: 0
    }).on('select2:select', function (e) {
        const selectedSymbol = e.params.data.id;
        if (selectedSymbol) {
            fetchStockPrices(selectedSymbol);
        }
    });
}

function fetchStockData() {
    axios.get('https://sp500-capstone.onrender.com/stocks')
        .then(response => {
            stockData = response.data;
            console.log("Data loaded successfully");
            populateSearchOptions();
            if (stockData.length > 0) {
                fetchStockPrices(stockData[0].symbol);
            }
        })
        .catch(error => {
            console.log("Error fetching data:", error);
        });
}

function populateSearchOptions() {
    const selectData = stockData.map(stock => ({
        id: stock.symbol,
        text: `${stock.symbol} - ${stock.name}`
    }));
    
    $('#searchInput').select2({ data: selectData });
}

function fetchStockPrices(symbol) {
    axios.get(`https://sp500-capstone.onrender.com/price_data/${symbol}`)
        .then(response => {
            const stockPrices = response.data;
            console.log("Stock prices loaded successfully");
            const selectedStock = stockData.find(stock => stock.symbol === symbol);
            updateChart(selectedStock, stockPrices);
        })
        .catch(error => {
            console.log("Error fetching stock prices:", error);
        });
}

function updateChart(stock, stockPrices) {
    if (stockChart) {
        stockChart.destroy(); // Destroy the previous chart instance if exists
    }

    const labels = stockPrices.map(price => new Date(price.dt).toLocaleString('default', { month: 'short', year: 'numeric' }));
    const data = stockPrices.map(price => price.close);

    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${stock.name} Stock Price`,
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function changeTimescale(timescale) {
    console.log("Changing timescale to:", timescale);
}
