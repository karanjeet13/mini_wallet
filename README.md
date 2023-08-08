# mini_wallet
mini_wallet_assignment

1.Clone the project using the copied repository link:
        git clone <repository-link>
2. Make a virtual env for python 3.10 
        python3.10 -m venv <name>
  Activate the virtual environment:
          source <name>/bin/activate
3. In the activated virtual environment, install Django and Django Rest Framework using pip:
        pip install django
        pip install djangorestframework
4. Run the makemigrations command to create migration files::
        python manage.py makemigrations
   Apply the migrations to the database using the migrate command:
        python manage.py migrate
5. Start the development server using the following command:
        python manage.py runserver
