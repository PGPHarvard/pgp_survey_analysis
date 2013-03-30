pgp_survey_analysis
===================

Code for parsing Personal Genome Project survey data.

Included in the **surveys_20130213** directory are copies of survey data from 
Feb 23 2013. You can upload new copies of these surveys from the PGP site.

PGP Participant Survey:
* https://my.personalgenomes.org/google_surveys/1

2012 PGP Trait & Disease Surveys:
* https://my.personalgenomes.org/google_surveys/6
* https://my.personalgenomes.org/google_surveys/7
* https://my.personalgenomes.org/google_surveys/8
* https://my.personalgenomes.org/google_surveys/9
* https://my.personalgenomes.org/google_surveys/10
* https://my.personalgenomes.org/google_surveys/11
* https://my.personalgenomes.org/google_surveys/12
* https://my.personalgenomes.org/google_surveys/13
* https://my.personalgenomes.org/google_surveys/14
* https://my.personalgenomes.org/google_surveys/15
* https://my.personalgenomes.org/google_surveys/16
* https://my.personalgenomes.org/google_surveys/17

Usage
-----

The code in **demo.py** is included as an example. It can be run with 
`python demo.py` and outputs some tab-separated data associating traits with 
participant identifiers to stdout. There are other data in the surveys not 
presented in this parsed output; **demo.py** is simply included as a 
demonstration of usage of **pgp_survey.py**.
