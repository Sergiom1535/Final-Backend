import motor.motor_asyncio
from motor.frameworks import asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGODB_URL = "mongodb+srv://dev-regal:NerdStreet@nerdsofwallstreet.rf2byhq.mongodb.net/test"  # Replace this with your MongoDB URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.bookstore
books_collection = db.books

# For testing the connection
sync_client = MongoClient(MONGODB_URL)

def test_connection():
    try:
        sync_client.server_info()
        print("MongoDB connection established.")

        # Print database and collection info
        database = sync_client.bookstore
        print(f"Connected to the '{database.name}' database.")
        print("Collections in the database:", database.list_collection_names())

    except ServerSelectionTimeoutError:
        print("Error: Unable to connect to MongoDB.")

test_connection()

async def get_all_books():
    pipeline = [
        {"$sort": {"stock": -1}}
    ]
    all_books = await books_collection.aggregate(pipeline).to_list(length=None)
    return all_books
    
async def get_total_books():
    total_books = await books_collection.count_documents({})
    return total_books

async def get_top_5_bestselling_books():
    pipeline = [
        {"$sort": {"stock": -1}},
        {"$limit": 5},
    ]
    top_books = await books_collection.aggregate(pipeline).to_list(length=None)
    return top_books

async def get_top_5_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    top_authors = await books_collection.aggregate(pipeline).to_list(length=None)
    return top_authors



async def insert_sample_data():
    sample_books = [
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "description": "A classic novel about teenage angst and alienation.",
            "price": 12.99,
            "stock": 50,
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice.",
            "price": 9.99,
            "stock": 75,
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "description": "A humorous story of love and life among English gentility during the Georgian era.",
            "price": 14.99,
            "stock": 60,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "description": "A dystopian novel set in Airstrip One, formerly Great Britain, a province of the superstate Oceania.",
            "price": 13.99,
            "stock": 100,
        },
        {
            "title": "Animal Farm",
            "author": "George Orwell",
            "description": "An allegorical novella reflecting events leading up to the Russian Revolution of 1917 and then on into the Stalinist era of the Soviet Union.",
            "price": 10.99,
            "stock": 80,
        },
    ]

    await books_collection.insert_many(sample_books)


