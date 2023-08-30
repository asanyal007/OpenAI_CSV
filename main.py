from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains import create_qa_with_sources_chain
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key="<YOUR-KEY")

import pandas as pd
import pandasql as ps
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",     # Allow requests from this origin
    "http://localhost:8000" # Add more origins as needed
    "file:///Users/aritrasanyal/Desktop/GPT_workflow_autoation/home.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/query")
def read_item(q: str):
    # data = pd.read_csv("/Users/aritrasanyal/Desktop/GPT_workflow_autoation/titanic.csv")
    data = pd.read_csv("/Users/aritrasanyal/Desktop/GPT_workflow_autoation/COCO COLA.csv")

    data_head = data.head().to_json(orient='records')
    data_types = data.dtypes
    columns = data.columns.to_list()
    system1 = "You are a Data Analyst.  Your task is to create sqlite3 SQL queries based on the QUESTION and the DATA_SAMPLE. Provide only the SQL.The table name is data.Make sure the columns in generated SQL exists in the table."
    system2 = "You are a Data Analyst.  Your task is to create Pandas dataframe filters based on the QUESTION and the DATA_SAMPLE. Provide only the code.The table name is data."
    messages = [
        SystemMessage(
            content=system1
        ),
        
        HumanMessage(
            content=f"""=============================================
    DATA_SAMPLE: {data_head}
    COLUMNS: {columns}
    DATA TYPES: {data_types}
    =============================================
    """
        ),
        HumanMessage(
            content=f"""QUESTION: {q}.
    """
        ),
    ]
    out = llm(messages)
    print("SQL: ",out.content)
    for i in range(0,4):
        try:
            data_temp = ps.sqldf(out.content, locals()).to_json(orient='records')
            break
        except Exception as e:
            print("Error: ",e)
            messages = [
            SystemMessage(
                content="You are a SQL developer, your task is to FIX errors in sqlite3 SQL Codes mentioned in ERROR:"
            ),
            
            HumanMessage(
                content=f"""=============================================
                Provde ONLY the fixed code. 
        ERROR: {e}
        =============================================
        """
            )
        ]
            out = llm(messages)
            data_temp = ps.sqldf(out.content, locals()).to_json(orient='records')

    # data_temp = eval(out.content)
    # data_temp_pd = pd.DataFrame(eval(data_temp))
    token_len = len(data_temp) * 4
    # if token_len>=40000:
    #     return "token limit crossed!"
    print("DATA: ",data_temp)
    prompt = f'''System: You are a web developer tasked with visualizing data. You need to suggest a suitable chart type and generate HTML chart code based on the provided data.ONLY provide the HTML Code.
    Context: You have been provided with data about sales figures for different products over a period of months. You need to ONLY create an HTML chart to visualize this data.

Question: Provide some business suggestion based on the data, Suggest a suitable chart type and generate HTML chart code to display {q} using the provided data below:

Data:
{data_temp}

Response:
'''
    # messages = [
    #     SystemMessage(
    #         content="""You are a Data Analyst.  Your task is to create HTML Chart CODE  based on the data provided in CONTEXT and the QUESTION. Provide only the code.
    #         """
    #     ),
        
    #     HumanMessage(
    #         content=f"""=============================================
    #         Provide ONLY the HTML CODE based on the sample data in CONTEXT & QUESTION
    # CONTEXT: {data_temp}
    # QUESTION: {q}
    # =============================================
    # """
    #     )
    #     ,
    # ]
    messages = [
        SystemMessage(
            content="""You are a web developer tasked with visualizing data. You need to choose a suitable chart type and generate HTML chart code based on the provided data.Also, provide detailed business findings based on the data and SHOW IT in footer of the HTML Code. ONLY provide the HTML Code.
            ALWAYS USE src="https://cdn.jsdelivr.net/npm/chart.js" . ALWAYS adjust Y Axis height based on the data.
            """
        ),
        
        HumanMessage(
            content=f"""Context: You have been provided with data about stock prices for Coca Cola. You need to create an HTML chart to visualize this data. 
Question: Suggest a suitable chart type and generate HTML chart code to display {q} using the provided data below:

Data:
{data_temp}

Response:
    """
        )
        ,
    ]
    out_chart2 = llm(messages)

    Func = open("GFG-1.html","w")
   
    # Adding input data to the HTML file
    Func.write(out_chart2.content)
                
    # Saving the data into the HTML file
    Func.close()
    return HTMLResponse(content=out_chart2.content, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

