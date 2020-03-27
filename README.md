# FAKERECIPES project

Check [fakerecipes.herokuapp.com](https://fakerecipes.herokuapp.com/)

___


Actually I tried from scratch to learn about **Django**, so this project is basically cleaned version of it to serve at **Heroku**. 

So to run locally there is a need to mock the *os environment* variables, like providing a _database_ or _AWS_ credentials.

---

The structure of the project is quite simple. I've implemented **models**, **forms** from models and of course **views**. 

To handle the **user authentication**, I customized the **default Django user class**

File uploads made with the **Django-S3-Direct** library. 