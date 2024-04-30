# SP500-Capstone
The application is designed to interact with S&amp;P 500 stock data, enabling users to fetch, predict, and visualize stock price movements effectively. This tool is particularly useful for investors and financial analysts who require up-to-date stock data and future price predictions to make informed decisions.

## Technologies Used:
- <B>Python</B>: The primary programming language for backend development.
- <B>Flask</B>: A lightweight WSGI web application framework used to build the web interface.
- <B>SQLAlchemy</B>: The SQL toolkit and ORM used for database operations.
- <B>AWS AutoGluon</B>: Open-source tool from Amazon that provides powerful, automated machine-learning capabilities specifically tuned for time series forecasting.
- <B>PostgreSQL</B>: The relational database management system chosen for its robustness and compatibility with large-scale data operations.
- <B>GitHub</B>: Used for source code management and version control, facilitating collaborative features and code reviews.

## Application Workflow:
- Users can input a stock symbol via the web interface.
- The app retrieves the relevant data from the database and displays both historical data and future predictions.
- It allows users to see various quantile predictions (e.g., 10th percentile, median, 90th percentile), providing a comprehensive view of potential stock price scenarios.

## Development Expertise
- <B>API</B> Integration and Data Handling: The application involves extensive use of APIs to fetch real-time and historical stock data, demonstrating skills in API consumption, data extraction, and transformation.
- <B>Time Series Prediction</B>: Advanced use of AutoGluon to handle time series data, forecast future stock prices, and interpret model predictions to provide actionable insights.
- <B>Database Management</B>: Proficient use of SQLAlchemy for database operations, showcasing the ability to design and manage complex data schemas effectively.
- <B>Error Handling and Debugging</B>: Rigorous implementation of error handling within the Flask framework to ensure the application's reliability and stability. Debugging skills are highlighted through systematic identification and resolution of issues during development.
- <B>Version Control and Deployment</B>: Proficient in using Git for version control, including managing and merging branches, handling pull requests, and pushing updates. Experience in deploying web applications, ensuring they are scalable and secure.

## Key Features:
- <B>Stock Data Interaction</B>: The app integrates with various financial data sources to retrieve real-time and historical data about S&P 500 stocks.
- <B>Predictive Analytics</B>: The app utilizes AWS AutoGluon's time series forecasting capabilities to predict future stock prices based on historical data. This feature uses advanced machine learning techniques to forecast stock price movements over several months.
- <B>Data Management</B>: Using SQLAlchemy, the app efficiently manages and queries stock data stored in a PostgreSQL database. This setup allows for robust data retrieval, manipulation, and storage, facilitating complex queries and data analysis.
- <B>User Interface</B>: Built with Flask, the app offers a web-based interface where users can query specific stocks, view historical data, and receive predictions. The interface is designed to be user-friendly, providing clear and actionable insights.
- <B>Version Control and Deployment</B>: The development process involves meticulous version control using Git, with the codebase hosted on GitHub. This setup not only ensures code integrity and collaboration but also simplifies deployment and updates.
