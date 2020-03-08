# my Wishlist
An application where you can create a wishlist for various things.

The Python Flask web application will connect to the MySQL db on GCP through configurations


# How to generate the “production” dataset and load it into database.

Raw Data Link:
https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/version/1
We downloaded the data from the above link, the form of a CSV file with 5k data.
The data was imported to CloudSQL. 
The data transformation code is in the project.sql file.
During user signup, we will obtain data from the user such as their chosen “username” and “password”,  and our backend will build out custom database tables to account for this. This is present in the app.py file.
A unique “userID” will be created for each user based on uuid function to establish a primary key. 
When user clicks the "Add to wishlist" button, the movieID, userID in session, and time will be inserted to the wishlist database.



# Features implemented and files that contain the implementation

Feature 1: User registration to the movie wishlist app
File: app.py (register function) and register.html 

Feature 2: User login to the movie wishlist app and remember login session
File: app.py (login function and is_user_logged_in function) and login.html 

Feature 3: Returning all the movies available and sorting by various requirements
File: app.py (dashboard function) and home.html

Feature 4: Adding movies to wishlist through AJAX
File: app.py (processing_wishlist function and dashboard function), home.html and layout.html

Feature 5: Displaying wishlist through AJAX
File: app.py (wishlist function), wishlist.html

Feature 6: Providing different recommendations
File: app.py (recommendation function), recommendation.html

