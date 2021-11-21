## incident-app-mw
Enrich 911 emergency incident data to provide better analytics.

## Screenshots of Working App

Default view
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/1.png?raw=true)
-----------
selecting a file view
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/2.png?raw=true)
-----------
selecting a file viewII
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/3.png?raw=true)
-----------
uploading the file, it stored in the db if it does not exist already
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/4.png?raw=true)
-----------
Incident Report after Enriching the data
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/5.png?raw=true)
-----------
Incident Report after Enriching the second data
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/7.png?raw=true)
-----------
Incident Report after Enriching the second data (another view)
![](https://github.com/jemikalajah123/incident-app-mw/blob/master/docs/9.png?raw=true)
-----------

## Steps to install and run your app

### Clone the repository
Run `git clone https://github.com/jemikalajah123/incident-app-mw.git `to clone the repository to your local.

### Start Development server with docker
Make sure docker is installed on your local and is running. Start the development server on docker with the following commands;

Run `cd libraryApp to navigate into the root directory.`

Run `docker-compose build from the root directory.`

Run `docker-compose up from the root directory.`

### view the App
Navigate to **http://0.0.0.0:8000/**. The app will not automatically reload if you change any of the source files.

## best practices
Venv: Started developing on python virtual environment then dockerized it later on.<br />
Docker: I developed in a Docker container, writing the Dockerfile as I went On. Also created a production dockerfile<br />
Ui/Ux: I tried to come up with the best User experience while testing the application.<br />
Instead of the bounding box around the actual parcel, I took a polygon based on the incident lat/long + all deployed emergency crew's arrival lat/long.<br />
Separate production docker file for deployment.

## improvements
Ui/Ux: I would use a single page application like next.js for better Ui/Ux.<br /><br />
CI-CD Pipeline: I would have been able to properly configure CI-CD pipeline to deploy the app on heroku using docker which I started already<br /><br />
Enriching: This is my first time enriching data, I would love to try out other third parties to better enrich the data.<br /><br />
Test case: Write a more robust test suite cases for the application.<br /><br />
Uploaded files will be stored on a cloud service like cloudinary


## Time spent
10 hours of desk time, broken into 10 sprints with rests in between each.
