# PIT App

Django app with web forms to assist with the collection of data for Point-in-Time (PIT) counts for the Annual Homeless Assessment Report (AHAR) sent to the U.S. Congress. You can view these annual reports at:
https://www.hudexchange.info/homelessness-assistance/ahar

Examples PDFs of the forms:
 - Intervew: https://files.hudexchange.info/resources/documents/Model-Interview-Based-Unsheltered-Night-of-Count-PIT-Survey.pdf
 - Observation: https://files.hudexchange.info/resources/documents/Model-Observation-Based-Unsheltered-Night-of-Count-PIT-Survey.pdf 

## Running Locally
1. Run using run.sh to set up
2. Start locally by going to http://127.0.0.1:8000/
3. Set up an account and submit surveys

## Contributions
### Justin Calma

### Timothy Crowley

### Zoe Frongillo
* Front end UI design
* Forms submission handling (observation, survey, individuals)
    * Backend management for saving multiple objects and their inter-dependencies within object models

* Forms front end display
    * Forms generated
    * Section survey to dynamically require certain sections based on the selections (i.e. Only clients that were 
     veterans need to fill out the VHS section, and only clients over 18 need to fill out the over 18 section)
    * Redirect detail page to query the just submitted form object(s) to display to user the information they just submitted;
    created functions to make the information readable to the user
    * Add individuals to forms more dynamically: the forms query individual form objects based on which user logged in

### Edwin Fuquen

### Edin Sabanovic
