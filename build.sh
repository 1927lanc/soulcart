#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

### File 2: `Procfile`
Create a new file called `Procfile` (no extension at all) and paste this:
```
web: gunicorn soulcart.wsgi