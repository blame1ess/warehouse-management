### DEPLOYMENT

- Start application:

```$ run app.py```
- Seeding database:
  - using Python3
```
>>> from app import db
>>> db.create_all()
```


```$ mysql -u username -p database_name < commodity.sql```