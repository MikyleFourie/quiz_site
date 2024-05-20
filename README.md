# quiz_site
 A repository for the Django quiz site. Developed for an Assignment for the ELEN3020A - Professional Practice and Software Development course at Wits University 2024

Before cloning this repository, please follow these steps:

  1. Use this in the control panel 
pip install virtualenv
  2. use ‘cd’ to navigate to wherever you want to create your virtual environment to work on the project.
  3. Use this in the command terminal to create the virtual environment 
virtualenv qs_virtual_env
  4. now in the terminal use this to activate the virtual environment (you can deactivate it by just typing deactivate). You must activate it to work in the project
qs_virtual_env\Scripts\activate.bat
  5. Now that you’re in the virtual environment, use this to install Django into it
python -m pip install Django
  6. From here. Check you’ve got Python 3.12.3 using this line
python --version 
  7. Then check the Django version is 5.0.4 with this
django-admin --version
  8. Clone the quiz_site Repo from GitHub and save it into your virtual environment folder 📁


Refer to the requirements.txt folder for all the necessary packages one must have installed to run the server locally. Generally these can be installed by using pip install 

Notable CMD Prompts
To activate your virtual environment navigate to the environments Scripts folder, and simply type [ activate.bat ] in the CMD 
To run the local server, navigate into the quiz_site folder. Then in the CMD Prompt type [ python manage.py runserver ]
To ensure the most recent static files (such as CSS or JS) have been uploaded to the deployed version of the site, use: [ python manage.py collectstatic ]
To reset the PK sequence (especially after a large amount of data is added locally) use the following command in psql to avoid an IntegrityError - do this for every database table:
[ SELECT setval(pg_get_serial_sequence('app_dbtable', 'id'), coalesce(max(id), 1) + 1, false) FROM app_dbtable; ]
After every change to the Django models run both commands : 
 [ python manage.py makemigrations ] 
 [ python manage.py migrate ]
