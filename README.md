# README

De naam die wij hebben gekozen voor de website is: TRIVIATOR. De studenten die aan deze website hebben gewerkt zijn: Ruben Vreeken, Kaan Tastan en Kevin Tran.

# Screenshot:

![Alt text](/screenshot/banaan.png?raw=true "Screenshot")

# Huidige features:

# Als teacher:

- Een teacher kan een quiz aanmaken en van alle studenten, die de desbetreffende quiz hebben gemaakt, per student de resultaten zien.
- Deze resultaten worden opgeslagen in een database en kunnen op elk moment worden opgeroepen.
- Een teacher, wanneer deze registreert, krijg een teacher id van 1. Dit is van belang om de juiste resultaten te zien in results. Deze resultaten zijn anders dan die van de studenten.

# Als student:

- Een student kan zelf een quiz aanmaken voor zichzelf, of een bestaan quiz joinen. Na het maken van deze quiz, krijgt de student zijn score te zien.
- Als een student zijn score terug wil zijn, dan kan de student deze terugvinden in results.
- Een student krijgt een teacher id van 0, waardoor een student andere resultaten zien dan de teachers.

Tijdens dit project hebben wij veel gewerkt met MYSQL. Op elke pagina implementeren wij functionaliteit waarbij gegevens uit de database gehaald worden of juist in de database gezet worden.
Wij gebruiken bijvoorbeeld de gegevens die in "create" opgeslagen zijn, om de juiste vragen in "game" op te roepen. Deze worden vervolgens ook weer gebruikt om de juiste resultaten de laten zien in results.
De juist resultaten kunnen wij correct weergeven, door gebruik te maken van een teacher id. Dit kunnen jullie terugvinden in application.py def result().

Om alle juiste tekens tijdens de quiz goed weer te geven, hebben wij een omzet functie in helpers.py geschreven. Deze functie zorgt ervoor dat bijvoorbeeld een quote goed weergegeven wordt.
Omdat wij het juiste antwoord meesturen met de vraag en de mogelijkheden, hebben wij een encrype functie geschreven om het antwoord te encrypten. Om deze manier kan een student niet stiekem kijken wat het goede antwoord is.

In application.py staan overal comments, zodat jullie weten wat alles doet.
In de static folder staat het css bestand.
In de templates folder staan de html pages.

# Wie wat heeft gedaan:

Ruben Vreeken: Python (Teacher register, result en student_result) en html code.
Kevin Tran: Python (Game, create, register en helpers.py) en database en html code.
Kaan Tastan: Python (Login) en css.
