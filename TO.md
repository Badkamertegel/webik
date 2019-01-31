
# Technisch ontwerp

# Lijst plugins en frameworks:
-Flask framework: https://www.fullstackpython.com/flask.html 
-SQL plugin: https://www.w3schools.com/sql/sql_intro.asp 
-Bootstrap: https://getbootstrap.com/docs/4.2/getting-started/introduction/ 
-Flask plugins: Flask, flash, redirect, render_template, request, session, url_for en 

# Controllers:

- Login: POST request, In de python code gebruiken we de regel: return render_template("login.html") om de html pagina te laden, waarop een gebruiker kan inloggen. De benodigde gegevens heeft de gebruiker ingevoerd in een database. Door middel van de code: db.execute("SELECT FROM ") kunnen wij de gebruiker koppelen aan een session_id. Deze session_id is nodig voor het oproepen van een quiz. Dit gebeurt in de andere html's 
- Register: POST request, In de python code gebruiken we de regel: return render_template("register.html") om de html pagina te laden, waarop een gebruiker zich kan registreren. De benodigde gegevens heeft de gebruiker ingevoerd in een database. Door middel van de code: db.execute("INSERT INTO) kunnen wij de gebruiker koppelen aan een session_id. Deze session_id is nodig voor het oproepen van een quiz. Dit gebeurt in de andere html's 
- Create: POST request, in de python code gebruiken we de regel : return render_template("create.html) om de html pagina te laden waarop de gebruiker een quiz aan kan maken. hierbij wordt een aangemaakte quiz in de database gezet door middel van de code: db.execute(INSERT INTO), daarma kan een aangemaakte quiz ook later weer opgehaald worden.
- Logout: GET request, hoort geen specifieke pagina bij, maar na inloggen kan een gebruiker op elk gegeven moment gebruik maken van logout, zodra dit aangeklikt wordt, wordt de gebruiker doorverwezen naar de login url.
- Studentresult: POST request, In de python code gebruiken we de regel: return render_template("studentresult.html") om de html pagina te laden waarop de student zijn quizresultaten kan bekijken.
- Teacherresult: POST request, In de python code gebruiken we de regel: return render_template("teacherresult.html") om de html pagina te laden waarop de docent de resultaten van de studenten kan bekijken.
- Game: POST request, In de python code gebruiken we de regel: return render_template("game.html") om de html pagina te laden. Op deze pagina worden de quizvragen uit de internet database opgehaald en gecategoriseerd op basis van vraagcategorie en moeilijkheidsgraad.


![](Projectvoorstel.png)


# Helpers:

- een login required functie, dit is een functie die we gebruiken in de python code om aan te geven dat een actie zoals create of bijvoorbeeld game alleen plaats kunnen vinden als de gebruiker is ingelogd.




# View bestanden:

- create.html
- homepage.html
- layout.html
- login.html
- register.html
- result_student.html
- result_teacher.html
