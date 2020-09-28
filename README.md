Attu web application
====================

This flask/sqlite web application hosts nicely formatted scripture quotes.
You can select the verses to show and the rendered html will show them compiled into a single passage.


## Development ##

```cmd
py -m venv venv
venv\Scripts\pip install -r requirements.txt

set FLASK_APP=attu
set FLASK_ENV=development
venv\Scripts\flask run
```
