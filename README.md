# OpenAI_CSV

# GPT-3 CSV Data Analysis and Visualization Codebase

This codebase utilizes the power of OpenAI's GPT-3 to perform data analysis tasks and generate visualization suggestions based on CSV data. The code involves setting up a FastAPI web application that interacts with GPT-3 to provide SQL queries, Pandas dataframe filters, and HTML chart code. The application reads CSV data, processes it using GPT-3 models, and generates corresponding outputs. Below is an overview of the components and how to use the codebase effectively.

## Prerequisites

1. **Python Environment**: Make sure you have Python installed on your system.

2. **Required Packages**: Install the necessary Python packages using the following command:

   ```bash
   pip install pandas pandasql fastapi uvicorn langchain
   ```

3. **OpenAI API Key**: Replace `<YOUR-KEY>` in the code with your actual OpenAI API key.

## Code Explanation

The codebase consists of a FastAPI application with endpoints for handling data analysis and visualization tasks. Here's an explanation of the key components:

### 1. Import Statements

The code starts with necessary import statements, including the required modules from `langchain` and other packages.

### 2. FastAPI Setup

The FastAPI web application is set up, including the configuration of Cross-Origin Resource Sharing (CORS) middleware to allow requests from specific origins.

### 3. `/query` Endpoint

This endpoint is used for data analysis and visualization tasks. It accepts a query parameter `q`, which represents the user's query.

1. The CSV data is read using Pandas from a provided CSV file path (`COCO COLA.csv` in this case).

2. A series of messages are constructed to interact with GPT-3. These messages include system messages for setting the context and task for GPT-3, human messages containing data details, questions, and error messages, if applicable.

3. The `ChatOpenAI` model is used to generate responses from GPT-3 based on the constructed messages.

4. The generated SQL query is used to filter the CSV data using the `pandasql` library. If an error occurs during execution, the code attempts to fix the error by interacting with GPT-3.

5. The filtered data is then used to generate an HTML chart code suggestion. GPT-3 is again used to generate a suitable chart type and HTML code based on the provided data.

6. The HTML chart code is written to a file named `GFG-1.html`, which can be used to visualize the suggested chart.

7. The HTML content is returned as an `HTMLResponse` to be displayed in the web browser.

### 4. Running the Application

The code includes a block to run the FastAPI application using the `uvicorn` server. The application will run on `http://0.0.0.0:8080`.

## Usage

1. Ensure you have the required packages installed and replace `<YOUR-KEY>` with your actual OpenAI API key.

2. Place your CSV data file (e.g., `COCO COLA.csv`) in the appropriate location.

3. Run the application using the following command:

   ```bash
   python your_script_name.py
   ```

   Replace `your_script_name.py` with the name of your Python script containing the provided code.

4. Access the web application through your browser at `http://localhost:8080`.

5. Use the `/query` endpoint by appending `?q=your_question` to the URL, where `your_question` is the query you want to analyze and visualize based on the provided CSV data.

6. The application will generate an HTML chart code and display it in your browser. You can also find the HTML code saved in the `GFG-1.html` file.

## Notes

- Ensure that the CSV data is appropriately formatted and contains the required columns for the SQL queries and data analysis tasks.

- Adjust the CORS origins and other settings in the FastAPI setup according to your requirements.

- The codebase is designed to interact with GPT-3 models from the `langchain` library. Make sure you have the correct version of the library installed.

- This README provides an overview of the codebase. Ensure you have a deep understanding of the code and its components before deploying it to a production environment.
