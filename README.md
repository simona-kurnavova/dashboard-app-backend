Dashboard web application Django backend   
Client app: https://github.com/simona-kurnavova/dashboard-app

Run locally
--------------

1) Install dependencies from requirements.txt: `pip install -r requirements.txt`
2) Create Superuser: `python3 manage.py createsuperuser`
3) Set up database with following commands:   
`python3 manage.py makemigrations dash_app`   
`python3 manage.py migrate dash_app`
3) Log in to admin: `http://localhost:8000/admin` (for validation) and register client app at: `http://localhost:8000/o/applications/`
4) Run with `python3 manage.py runserver`

Using default applications:
----------------

These two projects (client and server) include 3 functioning applications: OneNote, Google Calendar, Translate (based on Yandex API)

In order to be able to use them follow these steps (you can skip this if you don't want to use these apps):

1) Inserts to database for all 3 applications (via Django admin `http://localhost:8000/admin` or Django shell)
```python
App.objects.create(name='calendar', allows_small_sizes=False, has_backend=False)
App.objects.create(name='onenote', allows_small_sizes=False, has_backend=True)
App.objects.create(name='translate', allows_small_sizes=False, has_backend=False)
```
2) Generate API keys for the apps:      
Microsoft (for OneNote): https://apps.dev.microsoft.com/#/appList (for backend)    
Google (for Calendar): https://console.cloud.google.com/apis/dashboard (for frontend)   
Yandex (for Translate): https://tech.yandex.com/translate/ (for frontend)   

3) Add these keys to project:

***OneNote***: To the backend app (this repository) into `dashboard-app-backend/dashboard/onenote/views.py`, replace existing dummy values of CLIENT_ID and CLIENT_SECRET variables with your own:

```python
CLIENT_ID = '78b9d80b-aab3-4615-8a23-5864573f967a'
CLIENT_SECRET = 'wdhfBEXO*@thfIXA01539;}'
```

***Google Calendar***: To the client (frontend) app into `dashboard-app/src/app/applications/calendar-application/calendar-application.service.ts`, replace variable client_id (no secret necessary for this app):

```typescript
static clientID = '37169070793-3eec0n9hc1b6s8tca1njrc64v6jpejvs.apps.googleusercontent.com';
```

***Translate app***: To the client (frontend) app into `dashboard-app/src/app/applications/translate-application/translate-application.service.ts`, replace KEY variable:

```typescript
static KEY = 'trnsl.1.1.20180420T152727Z.e83c5f4cd6ad348d.419a5e5f6d1b54e5d70f4ec0d651ea3e294650da';
```
