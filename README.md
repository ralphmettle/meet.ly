# **meet.ly** - A Hangout Planning Web Application

## Running meet.ly
To run **meet.ly** on your local device you have two options depending on which database schema you want to test. For ease of testing and review, I recommend using the SQLite3 version.

Once you have selected a version of **meet.ly** you wish to use, follow the instructions below:

## Instructions

### Step 1:
Unzip the file archive and open the directory in your text editor/IDE.

### Step 2:
Create a Virtual Environment in the directory to which we will install the dependencies. Use the following commands to do so:

`python -m venv .venv`

and activate the Virtual Environment with:

`.venv/Scripts/activate`

### Step 3:
While in the Virtual Environment, in the terminal run the following command to download the dependencies: 

`pip install -r requirements.txt`

---

With the dependencies installed, the instructions will diverge from this point depending on the database schema.

---

***For the SQLite3 version:***

The directory `/instance/` contains a `test.db` file prepared for you to test the application's features. Therefore, we can run the application from the terminal with:

`py run.py`

Navigate to your LocalHost at port 5000 `localhost:5000` in your browser, or whatever route is specified by Flask in the console.

The login credentials for the test account are:

Username: `test` Password: `test`

All preset accounts follow this naming structure if you want to log into any other of them to do things such as sending/accepting friend requests.

---

***For the PostgreSQL version:***

For this, you are required to already have PostgreSQL installed on your device. Once installed and a new database is set up, proceed with the instructions below.

In `app.py`, change the `app.config['SQLALCHEMY_DATABASE_URI']` variable to direct to your PostgreSQL database.

In the terminal, run `flask db init` to initialise the database. If this does not work, remove the `/migrations` folder from the directory and retry, or run `flask db upgrade` to use the latest migration in the folder to initialise.

To get the test users, in `user_test.py`, run the Python file, executing `init_db()`. You should receive console responses indicating progress.

You can now run `py run.py` in the terminal.

Navigate to your LocalHost at port 5000 `localhost:5000` in your browser, or whatever route is specified by Flask in the console.

