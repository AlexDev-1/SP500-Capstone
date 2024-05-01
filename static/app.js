const ctx = document.getElementById('stockChart').getContext('2d');
let stockChart;
let stockData = [];

let smooth = false;

const actions = [
  {
    name: 'Fill: false (default)',
    handler: (chart) => {
      chart.data.datasets.forEach(dataset => {
        dataset.fill = false;
      });
      chart.update();
    }
  },
  {
    name: 'Fill: origin',
    handler: (chart) => {
      chart.data.datasets.forEach(dataset => {
        dataset.fill = 'origin';
      });
      chart.update();
    }
  },
  {
    name: 'Fill: start',
    handler: (chart) => {
      chart.data.datasets.forEach(dataset => {
        dataset.fill = 'start';
      });
      chart.update();
    }
  },
  {
    name: 'Fill: end',
    handler: (chart) => {
      chart.data.datasets.forEach(dataset => {
        dataset.fill = 'end';
      });
      chart.update();
    }
  },
  {
    name: 'Smooth',
    handler(chart) {
      smooth = !smooth;
      chart.options.elements.line.tension = smooth ? 0.4 : 0;
      chart.update();
    }
  }
];

function adjustNewsContainerHeight() {
    var dataContainer = document.querySelector('.container_data');
    var newsContainer = document.querySelector('.container_news');
    var searchInput = document.querySelector('#searchInput');

    if (dataContainer && newsContainer && searchInput) {
        newsContainer.style.height = dataContainer.offsetHeight + 'px';

        // Calculate the total width of data container and news container
        var totalWidth = dataContainer.offsetWidth + newsContainer.offsetWidth;

        // Set the width of the search input to match the total width
        searchInput.style.width = totalWidth + 'px';

    }
}


document.addEventListener('DOMContentLoaded', function() {
    initializeSelect2();
    fetchStockData(); 
    setTimeout(() => {adjustNewsContainerHeight()},2000)
    setTimeout(() => {fetchNews('AAPL')},2200);
    window.addEventListener('resize', adjustTopBarWidth);
    window.addEventListener('resize', adjustNewsContainerHeight);
});

function adjustTopBarWidth() {
    var rowWidth = document.querySelector('.row').offsetWidth;
    var rowTopbar = document.querySelector('.row_topbar');
    if (rowTopbar) {
        rowTopbar.style.width = rowWidth + 'px';
    }
}



function initializeSelect2() {
    $('#searchInput').select2({
        placeholder: "Search for a stock...",
        minimumInputLength: 0
    }).on('select2:select', function (e) {
        const selectedSymbol = e.params.data.id;
        if (selectedSymbol) {
            fetchStockPrices(selectedSymbol);
            fetchNews(selectedSymbol);
        }
    });
}

function fetchStockData() {
    axios.get('https://sp500-capstone.onrender.com/stocks')
        .then(response => {
            stockData = response.data;
            populateSearchOptions();
            if (stockData.length > 0) {
                fetchStockPrices('AAPL');
                fetchNews('AAPL')
            }
        })
        .catch(error => {
            console.log("Error fetching data:", error);
        });
}

function populateSearchOptions() {
    const selectData = stockData.map(stock => ({ id: stock.symbol, text: `${stock.symbol} - ${stock.name}` }));
    $('#searchInput').select2({ data: selectData });
}

function fetchStockPrices(symbol) {
    axios.get(`https://sp500-capstone.onrender.com/price_data/${symbol}`)
        .then(response => {
            const stockPrices = response.data;
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
                backgroundColor: 'rgba(115, 159, 165, .2)',
                borderColor: 'rgba(115, 159, 165, 1)',
                borderWidth: 4,
                
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                filler: {
                    propagate: false,
                },
                legend: {
                    labels: {
                        font: {
                            size: 25
                        }
                    }
                },
                title: {
                    display: false,
                    text: (ctx) => 'Fill: ' + ctx.chart.data.datasets[0].fill
                }
            },
            interaction: {
                intersect: false,
            }
        }
    });

    // Attach event listeners to the chart actions
    actions.forEach(action => {
        const actionElement = document.querySelector(`[data-action="${action.name}"]`);
        actionElement.addEventListener('click', () => {
            action.handler(stockChart);
        });
    });
    adjustNewsContainerHeight();
}
function fetchNews(symbol) {
    axios.get(`https://sp500-capstone.onrender.com/get_news/${symbol}`)
        .then(response => {
            const newsData = response.data;
            console.log(newsData);
            displayNews(newsData);
        })
        .catch(error => {
            console.log("Error fetching news:", error);
        });
}

function displayNews(news) {
    const newsContainer = document.querySelector('.container_news');
    newsContainer.innerHTML = ''; // Clear previous news
    news.forEach(item => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';
        newsItem.innerHTML = `
            <h5>${item.headline}</h5>
            <h6>${item.created}</h6>
            <p>${item.content}</p>
            <a href="${item.url}" target="_blank">Read more</a>
            <hr>
        `;
        newsContainer.appendChild(newsItem);
    });
}

function changeTimescale(timescale) {
    console.log("Changing timescale to:", timescale);
}
