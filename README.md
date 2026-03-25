# UNESCO World Heritage Sites – Flask Web App

> Graded **19 / 20**

A Python/Flask web application that explores the **UNESCO World Heritage Sites** database. It exposes browsable lists and detail pages for sites, countries, criteria, and danger history, plus ten pre-built analytical queries.

---

## Project structure

```
app/
├── app.py               # Flask routes and SQL queries
├── server.py            # Entry point – starts the Flask dev server
├── db.py                # SQLite connection helper
├── UNESCO.db            # SQLite database (not tracked by git)
├── test_db_connection.py# Quick DB connectivity check
├── split_sites.py       # CSV utility – expands multi-country site rows
├── split_crit.py        # CSV utility – expands multi-criteria site rows
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── site-list.html / site.html
│   ├── country-list.html / country.html
│   ├── criteria-list.html / criteria.html
│   ├── dHistory-list.html / danger-history.html
│   ├── question-list.html
│   └── questions/
│       └── question1.html … question10.html
└── static/
    ├── style.css
    └── app_screenshot.png
```

---

## Requirements

- Python 3.8+
- pip

Install the only runtime dependency:

```bash
pip install Flask
```

---

## Configuration

The database file path is set in `db.py`:

```python
DB_FILE = 'UNESCO.db'   # must be in the same directory as app.py
```

Change this value if your database file has a different name or location.

### Verify the connection

```bash
python3 test_db_connection.py <TABLE_NAME>
```

Example:

```bash
$ python3 test_db_connection.py Site
```

If configured correctly, the first rows of the table will be printed.

---

## Running the app

```bash
python3 server.py
```

Then open **http://localhost:9000** in your browser.

---

## Available routes

| Route | Description |
|---|---|
| `/` | Home page |
| `/sites/` | All heritage sites |
| `/sites/<id>/` | Detail page for a site |
| `/countries/` | All countries |
| `/countries/<id>/` | Sites belonging to a country |
| `/criteria/` | All inscription criteria |
| `/criteria/<id>/` | Sites inscribed with a criterion |
| `/danger-history/` | All danger-history records |
| `/danger-history/<id>` | Detail for a danger-history record |
| `/question-list/` | Index of the 10 analytical queries |
| `/question-list/question/<id>/` | Result page for query 1–10 |

---

## Analytical queries (questions 1–10)

1. National Parks in Africa south of the Equator, ordered by name.
2. Total area (ha) per country, descending.
3. Sites in Iberian Peninsula countries (Portugal and Spain), ordered by country then name.
4. Number of sites per country, alphabetical.
5. Name and inscription year of sites in the country with the most sites, ordered by year then name.
6. Sites inscribed per geographic region per decade, ordered by decade and count descending.
7. The most-used inscription criterion (ID, description, usage count).
8. Average number of criteria per site for each country, descending then alphabetical.
9. Top 10 sites that have been (or are currently) in danger the longest, with country, classification, start year and years in danger.
10. Per region: total sites currently in danger, plus the country with the highest count of endangered sites.

---

## CSV utility scripts

**`split_sites.py`** – takes an `input.csv` with a comma-separated `CountryID` column and writes one row per country to `output.csv`.

**`split_crit.py`** – takes an `input.csv` with a `CriteriaID` column (e.g. `(i),(iv),(vi)`) and writes one row per criterion to `output.csv`.

Run either script from the project root:

```bash
python3 split_sites.py
python3 split_crit.py
```

---

## References

- [Flask documentation](https://flask.palletsprojects.com/)
- [Jinja2 templates](https://jinja.palletsprojects.com/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [W3Schools HTML tutorial](https://www.w3schools.com/html/)