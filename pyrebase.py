import pyrebase
import time

def sendFirebase(data,drctNa,drctNo):

    firebaseConfig = {
        "apiKey": "AIzaSyB4MdTq_Q1UxEqG8Hysxv_4548u9OEqKe0",
        "authDomain": "connectingfirebase-b95c6.firebaseapp.com",
        "projectId": "connectingfirebase-b95c6",
        "databaseURL": "https://connectingfirebase-b95c6-default-rtdb.firebaseio.com/",
        "storageBucket": "connectingfirebase-b95c6.appspot.com",
        "messagingSenderId": "693135522422",
        "appId": "1:693135522422:web:d0a5959a08d89b6a49fd57",
        "measurementId": "G-EWZWY041VP"
    };
 
    firebase = pyrebase.initialize_app(firebaseConfig)

    db = firebase.database()

    db.child("Users").child(drctNa).child(drctNo).set(data)
    


  



