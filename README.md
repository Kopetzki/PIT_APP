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

For this production deployment, a newly registered user is automatically made an Admin which gives access to the Django Admin Dashboard.  When deployed at a volunteer event, this automation can be turned off.  This is how the system is designed to work, with newly registered users automatically being placed into the "Unapproved Users" group.  In this deployment however, your registration will make you an Admin, granting access to all features available in the system.  

![Admin User Guide](https://user-images.githubusercontent.com/46574970/89105668-2d5efb80-d3f1-11ea-8f08-c72432a6a5dd.png)

## Contributions
### Justin Calma
* To be filled in 

### Timothy Crowley
* Login & Registration
    * Users propogate to Admin dashboard
    * Recognize user group on login
    * Implement different user flows based on group
* User groupings
    * Custom permissions for each group
    * Process for admin to easily move users to different groups

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
* Expanded user registration forms and added "Profile" page based on user logged in
* Added a user "History" page that allows users to see all forms they have submitted by category in table format

### Edwin Fuquen
* Setup local testing and PyPi deployment.
* Optimized pages to be responsive on mobile screens.
* Performance tweaks to reduce page load times.
* Number of bug fixes and UI tweaks/enhancements.
  * Removed duplicative fields on forms and computed them on the backend.
  * Fixed a few login and regisration bugs.
  * Improved the navbar to have highlights on hover.
  * Added flow from home page, to registration, to login to forms.

### Edin Sabanovic
* Initial setup of postgres db that was scrapped
* Data Model
* Charts/Admin Dashboard
