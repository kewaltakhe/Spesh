# [Spesh](https://spesh-nine.vercel.app/)

A photo sharing website built using Django 4.2.4.

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About [Spesh](https://spesh-nine.vercel.app/): A Beginner-Friendly Social Media Platform

  Welcome to Spesh, a simple project that allows users to share photos and follow other users. It is designed with beginners in mind. Spesh offers a hands-on opportunity to explore full-stack web development using Django while building a basic social media website.

## Getting Started

To test out locally, install python3.9 then create a virtual environment using python3.9 
```bash
#install python3.9-venv
sudo apt install python3.9-venv
#create virtual env and activate
python3.9 -m venv venv39
source venv39/bin/activate
#upgrade pip
pip install --upgrade pip
```
Get the repository.
```bash
# Example commands
git clone https://github.com/kewaltakhe/Spesh.git
cd Spesh
# install requirements
pip install -r requirements.txt
```

To test out locally, generate `SECRET_KEY`, use sqlite as database and local disk as storage.<br>
Run in terminal while inside the virtual env and the get the `SECRET_KEY`

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
e.g. `vh+qtogenex-k2*xy&peox*lz*v99=0ea4*gb9m@1o61%k299(`
<br>
Update `config/settings.py`.
```python
# insert the secret key
SECRET_KEY = "vh+qtogenex-k2*xy&peox*lz*v99=0ea4*gb9m@1o61%k299("

# Database

#uncomment these lines 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#comment this line
#DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'], engine='django_cockroachdb')}
```

Now run the following commands
```python
python manage.py makemigrations
python manage.py migrate
#launch
python manage.py runserver
```





## T
