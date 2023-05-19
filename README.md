# Final Project
CPSC449-02: Web Back-End Engineering

DUE: 19 May 2023 

## Group Members

- **Geovanny Casian** -
- **Dilhan Franco** - dilhanfranco@csu.fullerton.edu
- **Sergio Murguia** - 
  
## Project Overview
In this project, you will create an online bookstore API that allows users to view, search, and purchase books. The API will be built using FastAPI and the book data will be stored
in MongoDB.

## Technology Used
Python 3.11.0, MongoDB, FastAPI, & Pydantic

# How to Execute
Clone the Repository into desired file directory
```
git clone https://github.com/Sergiom1535/Final-Backend.git
```
Change directory to bookstore-api folder
```
cd bookstore-api
```
Install all necessary requirements to run app
```
pip freeze > requirements.txt
pip install -r requirements.txt
```
Run app using Uvicorn
```
uvicorn main:app --reload
```
Using SwaggerUI docs, Run endpoints!
```
http://127.0.0.1:8000/docs
```
<img width="1440" alt="Screenshot 2023-05-19 at 1 12 04 AM" src="https://github.com/Sergiom1535/Final-Backend/assets/53587310/77494db5-e26c-45f9-b889-f9e6a7ba332f">

## Test Runs
```/books``` Get Books
<img width="1070" alt="Screenshot 2023-05-19 at 1 21 35 AM" src="https://github.com/Sergiom1535/Final-Backend/assets/53587310/51f7e15e-8d63-463a-b5f3-5941d9e0ff3b">


