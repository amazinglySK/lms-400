import mysql.connector

from views import check_credentials
from models import Books, Member

conn = check_credentials()
books = [
    {
        "sub_code" : "Physics",
        "title" : "Nucleus",
        "author" : "J. Chadwick",
        "publisher" : "ABC",
        "price" : "20",
    },
    {
        "sub_code" : "Comp Sc.",
        "title" : "C and C++",
        "author" : "B. Stroustrup",
        "publisher" : "ABC",
        "price" : "30",
    },
    {
        "sub_code" : "Comp Sc.",
        "title" : "Python",
        "author" : "G. Rossum",
        "publisher" : "ABC",
        "price" : "30",
    },
    {
        "sub_code" : "Chemistry",
        "title" : "Synthetics",
        "author" : "XYZ",
        "publisher" : "ABC",
        "price" : "30",
    },
    {
        "sub_code" : "Mathematics",
        "title" : "Approaching Infinity",
        "author" : "Aryabhatta",
        "publisher" : "ABC",
        "price" : "50",
    },
]

members = [
    {
        "name" : "J. Thomas",
        "address" : "23, Olive Garden, Shj",
        "phone" : "2334598721", 
    },
    {
        "name" : "S. Krishna",
        "address" : "24, Baghdad Street, Shj",
        "phone" : "2334509009", 
    },
    {
        "name" : "M. Raza",
        "address" : "26, Oak Avenue, Shj",
        "phone" : "1244509001", 
    }
]
if conn.is_connected() : 

    # Loading books

    book_model = Books(conn)
    member_model = Member(conn)

    for i in books : 
        book_model.add_new_book(i)
    for j in members : 
        member_model.new(j)

    print("Done")
else:
    print("Oops something went wrong")