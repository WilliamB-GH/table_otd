# Premier League Table On This Day
#### Video Demo:  <URL HERE>
## Description

This web app displays premier League match information from the formation of the league in 1992 to present day. <br>
### Main Page
By default it displays the most recent table data it has, but any date as far back as August 1st 1992 can be shown. <br>
Tabs are provided showing fixtures in the following week from the selected date, and results from the previous week of fixtures. 

### Head to Head
The dropdowns are populated from the /teams API, with validation to ensure that two distinct teams are selected. A matplotlib chart is returned summarising the results between the two teams in the chosen time period, as well as the results of the games themselves.

### Mini League
This allows users to select teams and dates to construct a custom table from the data. It's probably the most powerful and flexible part of the app, as it allows users to create scenarios or examine results in over a wider range of dates than a normal table would allow.

## Tech Stack

The app is written in Python using Flask with Gunicorn running a WSGI HTTP server, The data is stored in a SQLite database. In front of this is Caddy for reverse proxy functionality. The app is managed and run from Docker containers, one for the Python/ Gunicorn part, and another for Caddy. This is all designed to be hosted locally or on AWS using Terraform the provided Terraform files. 

## How to Deploy

### Locally Hosted

+ Prerequisites:
    + Docker
    + Docker Compose

+ Instructions:
    + Clone the GitHub repo
    + cd into the directory you've saved the repo to.
    + Run: ```docker-compose up --build -d``` to build the containers and run it in detached mode
    + Visit 'http://localhost:80'
    + Run ```docker-compose down``` when you're finished


### AWS Hosting
+ Prerequisites:
    + A functional AWS account
    + AWS CLI installed and configured
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
    + Run ```terraform destroy``` when you're ready to take the app down

