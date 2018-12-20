

*development environment setup  see http://taswar.zeytinsoft.com/visual-studio-code-with-python-django/
install python 3.x

pip install virtualenv
pip install virtualenvwrapper-win
mkvirtualenv DjangoEnv

*using git posh 
clone repo
cd .\Deep-Learning-Art\DeepLearningArt\      

*alter activate.ps1 to execute script something like   C:\Users\*\Envs\DjangoEnv\Scripts\activate.ps1
notepad .\activate.ps1

*execute env
.\activate.ps1

*install infrastructure
pip install django
pip install opencv-python==3.4.1.15
pip install pillow

*run web app
python manage.py runserver

*browse site
http://localhost:8000/
