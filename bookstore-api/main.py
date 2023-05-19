from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models import Book
from database import *

app = FastAPI()


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "message": "Validation error",
            "detail": exc.errors(),
        },
    )


# Test the aggregation functions
@app.on_event("startup")
async def test_aggregation_functions():
    # Insert the sample data
    # await insert_sample_data()
    print("On Load")
    #total_books = await get_total_books()
    #print(f"Total books: {total_books}")


    #top_5_authors = await get_top_5_authors()
    #print("Top 5 authors with the most books:")
    #for author in top_5_authors:
    #    print(author)

    #books = await get_all_books()
    #print("ALL BOOK TEST")
    #for book in top_5_books:
    #    print(book)


# Retrieves a list of all books in the store
@app.get("/books")
async def get_books():
    books = await get_all_books()
    return [document_to_dict(book) for book in books]



# Retrieves a specific book by ID
@app.get("/books/{book_id}")
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return document_to_dict(book)



# Adds a new book to the store
@app.post("/books")
async def add_book(book: Book):
    book_data = book.dict()
    inserted_book = await books_collection.insert_one(book_data)
    return {"_id": str(inserted_book.inserted_id)}

# Updates an existing book by ID
@app.put("/books/{book_id}")
async def update_book(book_id: str, updated_book: Book):
    existing_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book_data = updated_book.dict()
    if "_id" in updated_book_data:
        del updated_book_data["_id"]

    existing_book.update(updated_book_data)

    await books_collection.replace_one({"_id": ObjectId(book_id)}, existing_book)
    return {"_id": book_id}



# Deletes a book from the store by ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"_id": book_id}


# Searches for books by title, author, and price range
@app.get("/search")
async def search_books(title: str = None, author: str = None, min_price: float = None, max_price: float = None):
    query = {}

    if title:
        query["title"] = {"$regex": title, "$options": "i"}

    if author:
        query["author"] = {"$regex": author, "$options": "i"}

    if min_price is not None and max_price is not None:
        query["price"] = {"$gte": min_price, "$lte": max_price}
    elif min_price is not None:
        query["price"] = {"$gte": min_price}
    elif max_price is not None:
        query["price"] = {"$lte": max_price}

    matching_books = await books_collection.find(query).to_list(length=None)
    return [document_to_dict(book) for book in matching_books]



def document_to_dict(document):
    document_dict = dict(document)
    document_dict["_id"] = str(document_dict["_id"])
    return document_dict


