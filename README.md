# Premier League Table On This Day
#### Video Demo:  <URL HERE>
## Description

This web app displays Premier League match information from the formation of the league in 1992 to present day. Users can select any date in that window and the app will return the league table as it would have existed on that day. There are also pages for users to compare results between a pair of teams in head-to-head format, or between larger sets of teams in a table.<br><br>
The app was designed to be deployed either locally or on AWS with as few commands as possible, see the [deployment steps](#deployment-steps) for more information on how to do this.


### Main Page
By default it displays the most recent table data it has, but any date as far back as August 1st 1992 can be shown. Previous and next week buttons are provided to allow users to move through the data with less effort.<br>
Tabs are provided showing fixtures in the following week from the selected date, and results from the previous week of fixtures. 

### Head to Head
The dropdowns are populated from the /teams API, with validation to ensure that two distinct teams are selected. A matplotlib chart is returned summarising the results between the two teams in the chosen time period, as well as the results of the games themselves.

### Mini League
This allows users to select teams and dates to construct a custom table from the data. It's probably the most powerful and flexible part of the app, as it allows users to create scenarios or examine results in over a wider range of dates than a normal table would allow.

## Tech Stack

The app is written in Python using Flask with Gunicorn running a WSGI HTTP server, and the data is stored in a SQLite database. In front of this is Caddy for reverse proxy functionality. The app is managed and run from Docker containers, one for the Python/ Gunicorn/ SQLite part, and another for Caddy. This is designed to be hosted locally or on AWS using Terraform the provided Terraform files. 

## Deployment Steps

This app is designed to be as close to a one-click deployment as possible, though some prerequisites do exist for some of the technnology choices I have made in order to achieve this. These, and the steps required to get the app running, are listed below.

### Locally Hosted

+ Prerequisites:
    + Docker
    + Docker Compose

+ Instructions:
    + Clone the GitHub repo
    + cd into the directory you've saved the repo to.
    + Run: ```docker-compose up --build -d``` to build the containers and run it in detached mode
    + Visit 'http://localhost'
    + Run ```docker-compose down``` when you're finished


### AWS Hosting
+ Prerequisites:
    + A functional AWS account
    + AWS CLI installed and configured locally
    + Teraform installed locally
    + (Optional) A domain to host the site
+ Instructions:
    + Copy terraform.tf and startup.yaml locally
    + Public domain:
        + If you want to host on a public domain, you'll also need to download route53.tf
        + Update line 50 of startup.yaml with your domain
        + Update lines 2 & 8 of route53.tf with your domain
    + Direct IP connection only:
        + Comment out line 50 of startup.yaml
        + Do not download route53.tf
    + Run ```terraform init```
    + Run ```terraform apply```
    + This will return the public IP address of the EC2 instance that gets created
    + It will take a few minutes after the apply has finished before the startup script has finished running and the site is live
    + Run ```terraform destroy``` when you're ready to take the app down



## Role of Each File in the Repo
### App Folder
This is the main body of work, it contains all the python, html, css, javascript used to run the site, as well as the SQLite database it relies on.

The pages are controlled from **app.py**, which handles all the user input. There is one function for each page, and a small function to provide an API to allow the head-to-head page to populate the list of teams to have been in the Premier League.

**data.py** controls the database queries, the app is read-only as I decided that the ongoing maintainence of the site was beyond the scope of this project. As such when new data is entered it requires the site to be torn down and rebuilt, as well as a github commit to update the database. The get_results and get_mini_league_results functions have a lot of overlap and might at first glance seem like bad practice; however as I don't store a list of team IDs for a given season I use the get_results function to identify the team IDs, whereas for the mini-league page the user is responsible for selecting the teams they want to display. By using different functions 

**head_to_head.py** contains two functions specific to creating the head-to-head results graph, the first builds a numpy array to be consumed by the chart function which gives the number of wins and draws in the time frame. The second is a matplotlib-based function to create and return the chart as a fully fleshed out HTML tag.

**helpers.py** does most of the heavy lifting of constructing tables, getting results, and most of the more generic odd jobs. 

**page_build.py** returns most of the data for the index page, it's only 20ish lines of code, but with all the comments and whitespace, the app file is easier to read and understand with that abstracted away.

**wsgi.py** runs the app file when called by gunicorn.

**requirements.txt** is used by venv (during the development process) and docker (for testing and production) to install the required packages to run the app.
fixtures.db is the SQLite database with all the results and teams stored. See the [database schema](#database-schema) for more information about the makeup of the data.

#### Static Folder
**style.css** - Where possible I have preferred to use pure HTML & CSS over Javascript, for the benefit of performance and accessibility.

**head-to-head.js** - Handles the Javascript to populate the team dropdowns. It does this by calling the /teams API from the app

#### Templates Folder
### Caddy Folder
This is only for the Caddyfile referenced by docker-compose and the Caddy container. It takes an environment variable to allow the app to be deployed to a given domain on AWS. If no domain is provided in the docker-compose file, it defaults to localhost to enable testing. If used in production without a domain specified it is still possible to access the app using the IP address of the EC2 instance.



### Database Schema
![Database schema diagram for ./app/fixtures.db](schema.svg)
## Design Choices

## Use of AI

## Accessibility

## Further Enhancements
+ It'd be cool to update the site in place, or failing that, implement GitHub Actions to look for updates made to the database and when found redeploy the app.
+ The site is not at all mobile friendly.
+ I have built the teams & leagues tables of the database with the expectation of adding a lot more data to the app in due course.
+ The app is currently greyscale, whilst this was by design to get around team-colour based tribalism and arguments, it would be good to make the head-to-head graph pull team-appropriate colours
+ I'd like to be able to make the app identify when a team has been relegated/ won the title etc.
+ Outside events that impact the table (points deductions for financial breaches for example) are not currently included.

