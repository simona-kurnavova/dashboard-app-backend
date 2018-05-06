Dashboard web application Django backend

Run locally
--------------

1) Install dependencies from requirments.txt
2) Create Superuser: `python3 manage.py createsuperuser`
3) Register client app at: `http://127.0.0.1:8000/o/applications/ `
4) Run with `python3 manage.py runserver`

Database inserts:
----------------
Inserts to database for applications to work (via Django admin `http://127.0.0.1:8000/admin` or Django shell)
```typescript
App.objects.create(name='calendar', allows_small_sizes=False, has_backend=False)
App.objects.create(name='onenote', allows_small_sizes=False, has_backend=True)
App.objects.create(name='translate', allows_small_sizes=False, has_backend=False)
```
