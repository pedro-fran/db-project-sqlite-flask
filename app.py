import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    # TODO
    return render_template('index.html',message='UNESCO World Heritage Sites database')

# Sites
@APP.route('/sites/')
def list_sites():
    sites = db.execute(
      '''
      SELECT s.SiteID, s.SiteName, s.Classification, s.Region, s.Year
      FROM Site s
      ORDER BY s.SiteName
      ''').fetchall()
    return render_template('site-list.html', sites=sites)

@APP.route('/sites/<int:id>/')
def get_site(id):
    site = db.execute(
      '''
      SELECT *
      FROM Site
      WHERE SiteID = ?
      ''', [id]).fetchone()
    
    if site is None:
        abort(404, 'Site id {} does not exist.'.format(id))

    countries = db.execute(
      '''
      SELECT c.CountryID, c.CountryName
      FROM Country c
      JOIN LocatedIn li ON c.CountryID = li.CountryID
      WHERE li.SiteID = ?
      ORDER BY c.CountryName
      ''', [id]).fetchall()
    
    criteria = db.execute(
        '''
        SELECT c.CriteriaID
        FROM Criteria c
        JOIN InscribedWith iw ON c.CriteriaID = iw.CriteriaID
        WHERE iw.SiteID = ?
        ORDER BY c.CriteriaID
        ''', [id]).fetchall()
    
    dangerHistory = db.execute(
        '''
        SELECT DangerID, StartDate, EndDate
        FROM DangerHistory dh
        WHERE dh.SiteID = ?
        ORDER BY dh.DangerID
        ''', [id]).fetchall()
    
    return render_template('site.html', 
           site=site, countries=countries, criteria=criteria, dangerHistory=dangerHistory)


# Countries
@APP.route('/countries/')
def list_countries():
    countries = db.execute(
      '''
      SELECT * 
      FROM Country
      ORDER BY CountryName
      ''').fetchall()
    return render_template('country-list.html', countries=countries)

@APP.route('/countries/<country_id>/')
def get_country(country_id):
    country = db.execute(
        '''
        SELECT *
        FROM Country c
        WHERE c.CountryID = ?
        ''', [country_id]).fetchone()
    
    if country is None:
        abort(404, 'Country id {} does not exist.'.format(country_id))

    sites = db.execute(
        '''
        SELECT s.siteID, s.SiteName
        FROM Site s 
        JOIN LocatedIn li ON s.SiteID = li.SiteID
        WHERE li.CountryID = ?
        ORDER BY s.SiteName
        ''', [country_id]).fetchall()
    
    return render_template('country.html', country=country, sites=sites)

# Criteria
@APP.route('/criteria/')
def list_criteria():
    criteria = db.execute(
      '''
      SELECT *
      FROM Criteria
      ORDER BY CriteriaID 
      ''').fetchall()
    return render_template('criteria-list.html', criteria=criteria)

@APP.route('/criteria/<criteria_id>/')
def get_criteria(criteria_id):
    criteria = db.execute(
    '''
    SELECT *
    FROM Criteria c
    WHERE c.CriteriaID = ?
    ''', [criteria_id]).fetchone()

    if criteria is None:
        abort(404, 'Criteria id {} does not exist.'.format(criteria_id))

    sites = db.execute(
        '''
        SELECT s.siteID, s.SiteName
        FROM site s 
        JOIN Inscribedwith iw ON s.SiteID = iw.SiteID
        WHERE iw.CriteriaID = ?
        ORDER BY s.SiteName
        ''', [criteria_id]).fetchall()

    return render_template('criteria.html', criteria = criteria, sites=sites)

# DangerHistory
@APP.route('/danger-history/')
def list_dangerHistory():
    dHistory = db.execute(
      '''
      SELECT dh.DangerID, s.SiteID, s.SiteName
      FROM DangerHistory dh
      JOIN Site s ON dh.SiteID = s.SiteID
      ORDER BY s.SiteName
      ''').fetchall()
    return render_template('dHistory-list.html', dHistory=dHistory)

@APP.route('/danger-history/<int:id>')
def get_dangerHistory(id):
    dangerHistory = db.execute(
        '''
        SELECT *
        FROM DangerHistory dh
        WHERE dh.DangerID = ?
        ''', [id]).fetchone()
    
    if dangerHistory is None:
        abort(404, 'Danger History id {} does not exist.'.format(id))
    
    site = db.execute(
        '''
        SELECT s.SiteID, s.SiteName
        FROM Site s
        JOIN DangerHistory dh ON s.SiteID = dh.SiteID
        WHERE dh.DangerID = ?
        ''', [id]).fetchone()
    
    if dangerHistory['StartDate'] is None and dangerHistory['EndDate'] is None:
        message = "This site has never been in danger."
        return render_template('danger-history.html',
                               dangerHistory=None,
                               site=site,
                               message=message)

    return render_template('danger-history.html',
                           dangerHistory=dangerHistory,
                           site=site,
                           message=None)

#Questions
@APP.route('/question-list/')
def question_list():
    questions = [
        {"id": 1, "title": "Quais os nomes e respetivos países dos Parques Nacionais localizados em África abaixo da linha do Equador? Ordenado pelo nome dos Parques Nacionais."},
        {"id": 2, "title": "Qual a área total em hectares de todos os Sites de cada país? Ordenado descendentemente pela área total."},
        {"id": 3, "title": "Quais os nomes e respetivos países dos sites que se localizam em qualquer país da Península Ibérica? Ordenando pelo nome do país e nome do Site."},
        {"id": 4, "title": "Quantos sites existem em cada país? Ordenado pelo nome do país."},
        {"id": 5, "title": "Qual o nome e ano de inscrição dos sites do país com o maior número de sites? Ordenado pelo ano de inscrição e nome do Site."},
        {"id": 6, "title": "Qual o número de sites inscritos por área geográfica em cada década? Ordenado por década e número de Sites descendente."},
        {"id": 7, "title": "Qual o ID e descrição do critério de inscrição mais usado, assim como quantas vezes foi usado?"},
        {"id": 8, "title": "Qual a média do número de critérios usados para inscrever um site em cada país? Ordenado pela média de critérios usados descendente e pelo nome do país."},
        {"id": 9, "title": "Quais os 10 Sites que estão ou estiveram em perigo durante mais anos, assim como o país onde se encontram, classificação dos mesmos, ano de início de perigo e anos em perigo? Ordenado pelo tempo em perigo descendente e pelo nome do Site."},
        {"id": 10,"title": "Em cada região existem quantos sites em perigo atualmente e qual o nome e número de sites em perigo do país com mais sites em perigo de cada região atualmente? Ordenado descendentemente pelo total de sítios em perigo de cada região."},
    ]
    return render_template('question-list.html', questions=questions)

@APP.route('/question-list/question/<int:id>/')
def get_question(id):
    if id == 1:
        result = db.execute(
            '''
            SELECT s.SiteName, c.CountryName
            FROM Site s
	            JOIN 
	            LocatedIn li ON s.SiteID = li.SiteID
	            JOIN
	            Country c ON li.CountryID = c.CountryID
            WHERE c.Region = 'Africa'
            AND s.SiteName LIKE '%National Park%'
            AND s.Latitude < 0
            ORDER BY s.SiteName;
            '''
        ).fetchall()
        return render_template('questions/question1.html', result=result)
    
    elif id == 2:
        result =  db.execute(
            '''
            SELECT c.CountryName, SUM(sub.AreaInHa) AS TotalAreaInHa
            FROM (
            SELECT SiteID, MAX(AreaInHa) AS AreaInHa
            FROM Site
            GROUP BY SiteID
            ) sub
                JOIN 
                LocatedIn li ON sub.SiteID = li.SiteID
                JOIN 
                Country c ON li.CountryID = c.CountryID
            GROUP BY c.CountryName
            ORDER BY TotalAreaInHa DESC;
            '''
        ).fetchall()
        return render_template('questions/question2.html', result=result)

    elif id == 3:
        result =  db.execute(
            '''
            SELECT s.SiteName, c.CountryName
            FROM Site s
                JOIN 
                LocatedIn li ON s.SiteID = li.SiteID
                JOIN 
                Country c ON li.CountryID = c.CountryID
            WHERE c.CountryName = "Portugal" OR
            c.CountryName = "Spain"
            ORDER BY c.CountryName, s.SiteName;
            '''
        ).fetchall()
        return render_template('questions/question3.html', result=result)
    
    elif id == 4:
        result =  db.execute(
            '''
            SELECT c.CountryName, COUNT( * ) AS Num
            FROM Site s
                JOIN
                LocatedIn li ON s.SiteID = li.SiteID
                JOIN
                Country c ON li.CountryID = c.CountryID
            GROUP BY c.CountryName
            ORDER BY c.CountryName;
            '''
        ).fetchall()
        return render_template('questions/question4.html', result=result)
    
    elif id == 5:
        result =  db.execute(
            '''
            SELECT s.SiteName, s.year
            FROM Site s
                JOIN LocatedIn li ON s.SiteID = li.SiteID
                JOIN Country c ON li.CountryID = c.CountryID
            WHERE c.CountryName = (
            SELECT c2.CountryName
            FROM Site s2
                JOIN LocatedIn li2 ON s2.SiteID = li2.SiteID
                JOIN Country c2 ON li2.CountryID = c2.CountryID
            GROUP BY c2.CountryName
            ORDER BY COUNT(s2.SiteID) DESC
            LIMIT 1
            )
            ORDER BY s.Year ASC, s.SiteName;
            '''
        ).fetchall()
        return render_template('questions/question5.html', result=result)
    
    elif id == 6:
        result =  db.execute(
            '''
            SELECT (s.Year/10)*10 AS Decade, c.Region, COUNT(*) AS NumSites
            FROM Site s
                JOIN LocatedIn li ON s.SiteID = li.SiteID
                JOIN Country c ON li.countryID = c.CountryID
            GROUP BY Decade, c.Region
            ORDER BY Decade ASC, NumSites DESC;
            '''
        ).fetchall()
        return render_template('questions/question6.html', result=result)
    
    elif id == 7:
        result =  db.execute(
            '''
            SELECT c.CriteriaID, c.Description, COUNT( * ) AS Num
            FROM InscribedWith iw
                JOIN
                Criteria c ON iw.CriteriaID = c.CriteriaID
            GROUP BY c.CriteriaID, c.Description
            ORDER BY Num DESC
            LIMIT 1;
            '''
        ).fetchall()
        return render_template('questions/question7.html', result=result)
    
    elif id == 8:
        result =  db.execute(
            '''
            SELECT c.CountryName, AVG(CritCount) AS AverageCritPerSite
            FROM (
            SELECT s.SiteID, li.CountryID, COUNT(iw.CriteriaID) AS CritCount
            FROM Site s
                JOIN 
                LocatedIn li ON s.SiteID = li.SiteID
                JOIN 
                InscribedWith iw ON s.SiteID = iw.SiteID
            GROUP BY s.SiteID, li.CountryID
            ) AS Sub
                JOIN 
                Country c ON Sub.CountryID = c.CountryID
            GROUP BY c.CountryName
            ORDER BY AverageCritPerSite DESC, CountryName
            '''
        ).fetchall()
        return render_template('questions/question8.html', result=result)
    
    elif id == 9:
        result =  db.execute(
            '''
            SELECT s.SiteName, c.CountryName, s.Classification, dh.StartDate,
            (dh.EndDate - dh.StartDate) AS Years
            FROM DangerHistory dh
                JOIN Site s ON dh.SiteID = s.SiteID
                JOIN LocatedIn li ON s.SiteID = li.SiteID
                JOIN Country c ON li.CountryID = c.CountryID
            WHERE dh.StartDate IS NOT NULL
            AND dh.EndDate IS NOT NULL

            UNION ALL

            SELECT s.SiteName, c.CountryName, s.Classification, dh.StartDate,
            (2025 - dh.StartDate) AS Years
            FROM DangerHistory dh
                JOIN Site s ON dh.SiteID = s.SiteID
                JOIN LocatedIn li ON s.SiteID = li.SiteID
                JOIN Country c ON li.CountryID = c.CountryID
            WHERE dh.StartDate IS NOT NULL
            AND dh.EndDate IS NULL
            ORDER BY Years DESC, s.SiteName
            LIMIT 10;
            '''
        ).fetchall()
        return render_template('questions/question9.html', result=result)
    
    elif id == 10:
        result =  db.execute(
            '''
            SELECT c.Region,
            COUNT(DISTINCT s.SiteID) AS TotalSitesInDanger,
            (
            SELECT c2.CountryName
            FROM DangerHistory dh2
                JOIN
                Site s2 ON dh2.SiteID = s2.SiteID
                JOIN
                LocatedIn li2 ON s2.SiteID = li2.SiteID
                JOIN
                Country c2 ON li2.CountryID = c2.CountryID
            WHERE dh2.EndDate IS NULL
            AND dh2.StartDate IS NOT NULL
            AND c2.Region = c.Region
            GROUP BY c2.CountryName
            ORDER BY COUNT(DISTINCT s2.SiteID) DESC
            LIMIT 1
            ) AS TopCountry,
            (
            SELECT COUNT(DISTINCT s2.SiteID) 
            FROM DangerHistory dh2
                JOIN
                Site s2 ON dh2.SiteID = s2.SiteID
                JOIN
                LocatedIn li2 ON s2.SiteID = li2.SiteID
                JOIN
                Country c2 ON li2.CountryID = c2.CountryID
            WHERE dh2.EndDate IS NULL
            AND dh2.StartDate IS NOT NULL
            AND c2.Region = c.Region
            GROUP BY c2.CountryName
            ORDER BY COUNT(DISTINCT s2.SiteID) DESC
            LIMIT 1
            ) AS NumSites
            FROM DangerHistory dh
                JOIN
                Site s ON dh.SiteID = s.SiteID
                JOIN
                LocatedIn l ON s.SiteID = l.SiteID
                JOIN
                Country c ON l.CountryID = c.CountryID
            WHERE dh.EndDate IS NULL
            AND dh.StartDate IS NOT NULL
            GROUP BY c.Region
            ORDER BY TotalSitesInDanger DESC;
            '''
        ).fetchall()
        return render_template('questions/question10.html', result=result)
    
    else:
        abort(404, f"Question {id} not implemented.")