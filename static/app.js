let stockData = []; // This will hold stock data

document.addEventListener('DOMContentLoaded', function() {
    fetchStockData();
});

function fetchStockData() {
    axios.get('http://127.0.0.1:5000/stocks')
        .then(function (response) {
            stockData = response.data;  // Store the fetched data
            console.log("Data loaded successfully");
        })
        .catch(function (error) {
            console.log("Error fetching data:", error);
        });
}
