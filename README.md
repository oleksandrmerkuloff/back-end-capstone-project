# Little Lemon booking project
Django project `littlelemon`, app `restaurant`, MySQL, date/time reservations, and JavaScript Fetch API.

## Setup
1. Install Python 3.11, Pipenv, and MySQL.
2. Create the database: `CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
3. Set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` environment variables (see `.env.example`).
4. Run `pipenv install`, then `pipenv run python manage.py migrate`, then `pipenv run python manage.py runserver`.

## Endpoints
- `/book/` booking form, current date preselected.
- `/reservations/` JSON view with date filtering.
- `GET /api/bookings/` all bookings; `GET /api/bookings/?date=YYYY-MM-DD` for a date.
- `GET /api/bookings/YYYY-MM-DD/` date-specific JSON.
- `POST /api/bookings/` JSON: `{"first_name":"Jane","reservation_date":"YYYY-MM-DD","reservation_slot":1020}`. Slots are minutes after midnight; 17:00 is 1020.

Hourly slots 10:00–21:00. Unique database constraint on date and slot prevents duplicates, including concurrent requests. Changing the date reloads bookings and disables taken slots. The MySQL database is local and intentionally not included in the zip.
