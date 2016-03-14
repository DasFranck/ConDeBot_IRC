# ConDeBot
Un con de bot IRC.

## Features

* Make a good coffee  
``!cdb coffee`` or ``!cdb café`` or ``!cdb cafe``

* Display help  
``!cdb help``

* Display random quotes and specific quotes from Kaamelott.txt  
``!cdb kaamelott [-q ID]``

* Display his own version  
``!cdb version``

* Display actual weather and temperature of a location  
``!cdb weather CITY_NAME``

* Manage Operators (OPs):
  * Add an operator  
  ``!cdb op NICK`` (OP Rights required)
  * Delete an operator  
    ``!cdb op NICK`` (OP Rights required)
  * Check if some is an operator  
    ``!cdb isop NICK``
  * List operators  
    ``!cdb list_op``

* Remotly kill the bot  
  ``!cdb suicide`` (OP Rights required)

* Display his source code  
  ``!cdb source``


## To Be Done
* ``!cdb time Tokyo pour avoir l'heure actuelle de Tokyo (+ Décalage UTC)``
* ``!cdb trad en fr "I am tomato"``
* ``!cdb rep DasFranck "J'ai faim"``
* ``!c key = value`` and ``!c key`` which display value
  * Probably saved in pickle or json (I think it'll be JSON)
* Redirections (_e.g._ ``!cdb weather Paris > HS-157``)


## Changelog
### Version 0.5 (xx/03/2016)
* Operator managing module added
* Remote kill
* Command to display his source code (git repositories)

### Version 0.4 (11/03/2016)
* Kaamellot and weather are back from the dead.
* Full rewrite finished.

### Version 0.3nw (09/03/2016)
* Complete rewriting of CDB
* CDB is now standalone and doesn't need WeeChat anymore
* Coffee service added
* Logging added (Logger)
* Kaamelott and weather are actually KO (cause they're still Weechat coded)
* Source code is no longer just one big python file

### Version 0.3 (11/09/2015)
* Help Added
* Random Kaamelott quotes from kaamelott.txt
* Specific Kaamelott quotes from kaamelott.txt

### Version 0.2 (09/09/2015)
* Actual weather/temperature of a location added.

### Version 0.1 (08/09/2015)
* Initial Release
