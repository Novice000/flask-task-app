# MOTIVE
#### Video Demo:  <https://youtu.be/LaGtW6ag-JI>
#### **Description** : 
This project is a goal sharing web app. Essentially an app where you post or upload a goal. Then you can get to click a button if you have achieved it and then others too can get to do the same if they have achieved the same goal.

## Files/Folders

### Template Folder

##### layout.html:
This contains the template for every html file in the templates folder. It contains link to the bootstrap styling and javascript. It also contains a responsive navbar which is present in every other page. The navbars contains links to the different html pages which also includes a dropdown. It also contains two blocks for the title and the main block (jinja templating), for the page title and the main html code respectively. Navbar also contain different element depending on if the user is logged in or not. It also contains a script tag which contains javascript to enable tooltips.

##### index.html:
This page contains multiple elements. The top part of the page contains the project name and what is essentially a motto. It is important to mention that the page requires logging in. It is an archive for all the goals achieved by each user, with an option for other users to also add to their list of attained goals. All of which are in an html table and uses jinja templating. Tables also contain a field to search goals table by goal. It also contains and input tag for the option to add to your list of goals from what is essentially the homepage. It also contains pagination links as the goals table as been paginated to prevent the the html table from getting really long. This page also contains randomly generated motivational quotes, since it's a goal sharing app.

##### login.html:
This page contains a form with input element for username and password to aid logging in. It is the page where users are redirect to in the event they aren't already logged in. This page also contains randomly generated quotes at the top, seeing as the app is a goal sharing app, I decided to add motivation.

##### profile.html
This is the profile page, it contains the users profile photo. The username and a table of all goals posted or uploaded by the user not that of all users. All goals are, of course, in an html table and jinja is used to make rows dynamic. The table also has also been paginated to avoid the the length of the page from becoming unreasonably long. The table also contains button with the option to add a goal to the list of attained goals or to remove it from such list and the ability to delete a goal. This page also contains randomly generated quote and a form with which new goals can be added.

##### register.html
The register page contains a form with multiple input elements; an input element for the username, password, password confirmation and for the user's profile picture. The input types are text, password and file. These are to aid the registration of a new user. The page also contains randomly generated quotes for the aim of motivating the user.

##### error.html
It is a very simple html page that uses jinja template to catch error in the web app. It displays the cause of the error allowing the user to go back. These page is to catch expected errors though.

### static folder
This folder contains the style.css file and the image folder. The first of which contains the css for the the project and the image folder contains the files uplaoded by the user, which will all be images of different file formats. The CSS file contains the styling for the pagination links and background color for the body of all html pages in the project.

### motive.db
This is the database for the project. It contains all tables which are used in the project. The schema of the database is below;

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT,
    gender text);

CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal TEXT NOT NULL,
    status TEXT,
    date_added DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE attained (
    goal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (goal_id) REFERENCES goals (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT goal_user UNIQUE (goal_id, user_id)
);

CREATE TABLE quotes (id integer primary key,author text, quote text not null);
CREATE TABLE IF NOT EXISTS "quotes_temp;"(
  "Author" TEXT,
  "Quote" TEXT
);

```
The project uses sqlite for all database actions.

### helper.py
This is a python script that contains three functions used in the app. The login decorator function written by the cs50 staff which redirects users to the login page in the events they are not already logged in, The allowed_file from the flask documentation which helps check the file formats of uploads in the the register page and the get_type function to get the file format.

### requirements.txt
This contains all the dependencies for the project. All the dependencies can be installed from the CLI with 

```bash
pip install -r requirements.txt
```

The command must be ran from the root folder or the folder containing the requirements.txt file.

### app.py
This python script contains all view functions for almost all functionalities of the app. It has quite a few imports to help with making these functionalities. The app,py implements log-in, log-out, registration, delete, post and many other functionalities which the app comes with.

### conclusion
There's still a lot more to be added to the app. A project is never truly complete. I feel there's still a lot more I could do to make it better.