# Find-My-Way

Find My Way is a web based application that allows users to search within the United States for information about careers they may be interested in.


## Developer Tips:
1. Make sure to use a Python virtual environment
2. Exclude the build folder from .gitignore
3. Make sure to update requirements.txt if you add any additional dependencies (pip freeze > requirements.txt)
4. Heroku needs Procfile in root of project in order to deploy
5. Heroku has environmental variables for the database on their server, can retrieve with (os.environ['DATABASE_URL'])