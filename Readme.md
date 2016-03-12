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


## To Be Done
* ``!cdb time Tokyo pour avoir l'heure actuelle de Tokyo (+ Décalage UTC)``
* ``!cdb trad en fr "I am tomato"``
* ``!cdb rep DasFranck "J'ai faim"``
* ``!c key = value`` and ``!c key`` which display value
  * Probably saved in pickle or json (I think it'll be JSON)


## Changelog
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
