# GitHub-Issue-Backend
This is the source code for my API project [Issue Tracker](https://www.djangoissuetracker.com/). Visit the site [here](https://www.djangoissuetracker.com/).

# Motivation

I wanted a project that dove deeper into Django functionality. I also wanted to learn the Django REST framwork and practice integrating with a third party API.

# Goals

I strove to achieve the following:
* A fully deployed, functional, and secure web application.
* A site integrated with GitHub's public API, using Django REST to consume API data.
* A clone of some of GitHub's issue tracking features, adding the ability to associate issues to folders, files, and lines of code. These associations are tracked in GitHub by "stamping" the issue body with the added data.
* A backend relying heavily on class based Django views to serve site pages instead of function based views.
* A backend designed to keep as much code in the Django models as reasonably possible.
* A clean, user friendly frontend.

# Script Files of Interest

Want to see the core logic of this project without digging through the repo structure? Check out these files:

* [issues/models.py](https://github.com/RHAM231/GitHub-Issue-Backend/blob/master/app/issues/models.py): Houses issue database logic, including custom stamping methods for adding/updating issue associations.
* [sync/github_client.py](https://github.com/RHAM231/GitHub-Issue-Backend/blob/master/app/sync/github_client.py): My custom client script for connecting GitHub's API and Django REST to my site. Any data traveling from my site to GitHub or vice versa, gets routed through this script.

# My Thought Process and Methods



For a more detailed write up of my general approach to web development see the [README](https://github.com/RHAM231/My-Django-Website/blob/master/README.md) of my portfolio site.

### Issue Tracker Django Apps

Following Django convention, I split the site into apps based on function. The apps include:

##### 'base'
Serves the generic site pages 'home' and 'about', as well as the site search results page. Also establishes a base.html template for the navbar and footer that all other templates inherit from.

##### 'consume_api'
The app that houses all Django REST specific functionality such as serializers.py. Contains all the logic for serializing GitHub JSON objects to the database as well as the views needed to display Issue Tracker's API user interface.

##### 'GITB (GitHub Issue Tracker Backend)'
The default generated app when the Django project was created. Controls admin functions such as overall url mapping, email settings, security settings, installed Django apps, Django REST settings, etc.

##### 'issues'
Houses all logic for creating, reading, updating, and closing issues. The models.py file in this app also defines custom stamping methods for issues to enable extra data not tracked by GitHub.

##### 'repositories'
Houses all logic for storing and displaying GitHub repo structures. Handles repositories, folders, and files.

##### 'sync'
Houses the heart of the project, a Python script called [github_client.py](https://github.com/RHAM231/GitHub-Issue-Backend/blob/master/app/sync/github_client.py). This script is responsible for moving GitHub data between my site's frontend, backend, Django REST, and GitHub's API. It utilizes custom code for importing a repo and the third party Python package, [PyGithub](https://pygithub.readthedocs.io/en/latest/introduction.html) for editing and creating issues from the site's frontend.

##### 'users'
Contains logic for overriding Django's User class with a CustomUser class, allowing me to easily add fields and user types.

# Security

This site scores an A on [SecurityHeaders.com](https://securityheaders.com/?q=https%3A%2F%2Fwww.djangoissuetracker.com%2F&followRedirects=on). For more detailed information on my approach to security see the [README](https://github.com/RHAM231/My-Django-Website#readme) on my portfolio site.

# Deployment

I utilized the following process to deploy the site to an AWS EC2 instance, connect it with an AWS RDS instance, and configure it with my site domain.

## Pre-Deployment

1. **Run through my [Checklist](https://rexhmitchell.com/portfolio-project/project_checklist/)**
1. **Run through the [Django deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)**
1. **Create Deploy Branch**
    1. Create branch “deploy” on Github then pull from server
      1. Use “git checkout branch name” to swap between master and deploy
      1. Use “git branch” to see the current branch
    1. Remove all comments from deploy branch
    1. Add deployment settings to settings.py on deploy branch
    1. Commit and push to repository
1. **Create AWS Account (If needed)**
1. **Update Ubuntu on computer**
    1. apt-get update && apt-get upgrade

## Deployment

### Setup and test development server on EC2 instance

1. **Create EC2 instance**
    1. Pick Ubuntu
    1. Pick appropriate region
    1. Configure security group settings on EC2
    1. Temporarily allow all traffic to test server on port 8000
    1. Save site key to folder
    1. Backup site key in safe place
1. **Set file permissions on key to allow SSH, if needed**
    1. Give ourselves the ability to modify file permissions on Ubuntu for Windows
        1. sudo umount /mnt/c
        1. sudo mount -t drvfs C: /mnt/c -o metadata
        1. cd /mnt/c/path/to/file/we/want/to/modify
    1. Change the file permissions on the key
        1. sudo chmod 400 KEY_NAME.pem
1. **SSH into EC2 instance**
    1. cd /mnt/c/path/to/.pem/file
    1. sudo ssh -i "FILE_NAME.pem" <span>ubuntu@ec2-IP-ADDRESS.REGION.compute.amazonaws.com</span>
1. **Upgrade instance**
    1. apt-get update && apt-get upgrade
1. **Make Django Directory (while in ~)**
    1. mkdir django
    1. cd django
1. **Clone deploy branch from GitHub into Django directory (while in ~/django)**
    1. git clone -b deploy https://github.com/RHAM231/GitHub-Issue-Backend
1. **Install Python with pip (while in ~)**
    1. sudo apt-get install python3-pip
1. **Install venv (while in ~)**
    1. sudo apt-get install python3-venv
1. **Create env inside the django directory (while in ~)**
    1. python3 -m venv django/env
1. **Activate env (while in ~/django)**
    1. source env/bin/activate
1. **Install packages (while in ~/django/GitHub-Issue-Backend/app)**
    1. pip install -r requirements.txt
    1. Manually install as needed
1. **Update settings.py (while in ~/django/GitHub-Issue-Backend/app/GITB)** (home/django/TOP_FOLDER/PROJECT/SETTINGS APP)
    1. nano settings.py
    1. Set ALLOWED HOSTS to temporary IP address
    1. Turn on config settings and make sure that the secrect key is loading from a config file.
1. **Create config.json file in etc directory to house sensitive info**
    1. sudo touch /etc/config.json
    1. sudo nano /etc/config.json
    1. Add necessary entries
    1. Ctrl x, y, Enter to save file
1. **Run collectstatic (while in ~/django/GitHub-Issue-Backend/app)**
    1. python manage.py collectstatic
1. **Test Development Server on EC2 instance (while in ~/django/GitHub-Issue-Backend/app)** (home/django/TOP_FOLDER/PROJECT)
    1. python manage.py runserver 0.0.0.0:8000
    1. Type “temporary IP address:8000” into browser
    1. Everything should be running, test the site
    1. Anything that requires a production database will not work yet
    1. Stop server, Ctrl c

### Configure Apache2

 1. **Install apache2 and Django mod_wsgi (while in ~)**
     1. sudo apt-get install apache2 libapache2-mod-wsgi-py3
 1. **Navigate to apache2 configuration directory and create the .conf file**
     1. cd /etc/apache2/sites-available/
     1. sudo cp 000-default.conf django_project.conf
     1. sudo nano django_project.conf
     1. Ctrl x, y, Enter to save file
 1. **Enable the django_project.conf file and disable the default.conf file**
     1. cd ~/
     1. sudo a2ensite PROJECT NAME
     1. sudo a2dissite 000-default.conf
 1. **Give Apache access to the development database**
     1. Within the ~/ directory, set apache as the group owner of the db.sqlite3 file and parent directory, and set file permissions on  db.sqlite3 and parent directory
         1. sudo chown :www-data PATH TO FILE/db.sqlite3
         1. sudo chmod 664 PROJECT NAME/db.sqlite3
         1. sudo chown :www-data PROJECT NAME/
         1. sudo chmod 775 PROJECT NAME/
         1. ls -la, verify permissions
     1. Set owner and permissions for project media folder so we can access it with our database
         1. sudo chown -R :www-data PROJECT NAME/media/
         1. sudo chmod -R 775 PROJECT NAME/media
     1. Verify DEBUG = True (we will set this to False once we’re using the real domain)
 1. **Restart apache and test the site**
     1. sudo service apache2 restart
     1. navigate to site’s IP (remove :8000 from development test if needed)
     1. Test functionality, everything should work

## Post Deployment

### Database

1. **Create RDS instance**
    1. Set public accessiblity to “No”
1. **Configure security group settings on RDS**
    1. Add the EC2 instance’s security group to the RDS instance (this should be the default instance) allow access to the EC2 instance by Postgres from the default instance
1. **If you haven’t already, install psycopg2 on EC2 (while in ~)**
    1. pip install psycopg2 (or to avoid building from source … )
    1. pip install psycopg2-binary
1. **Comment out development database in settings.py**
1. **Edit the config file to replace remaining environment variables in settings.py**
    1. sudo nano /etc/config.json
    1. Edit the file to look like the following:
1. **Verify proper settings for postgres db in settings.py, comment out development database, and uncomment real database**
1. **Initilize database (while in ~/django/GitHub-Issue-Backend/app)** (home/django/TOP_FOLDER/PROJECT)
    1. python manage.py makemigrations
    1. python manage.py migrate
    1. python manage.py createsuperuser
1. **Test the database**
    1. sudo service apache2 restart
    1. go to temporary ip address/admin
1. **Build production database**

### Build additional security settings in settings.py

1. Turn on all security settings except for SSL, HSTS, and cookie settings (we will turn these on after enabling the SSL certificate:
1. Build up a Content Security Policy using Django-CSP, test each value

### Custom Domain

1. **Configure domain settings on domain provider**
    1. Add AWS’s name servers on provider
    1. Name servers can be found in AWS Route 53, Hosted Zones, Type NS (don't leave the period at the end off)
        1. ns-####.awsdns-##.net.
        1. ns-####.awsdns-##.co.uk.
        1. ns-####.awsdns-##.com.
        1. ns-####.awsdns-##.org.
1. **Create Route 53**
    1. Create record
    1. Use CNAME to display site as "domain.com" rather than "w<span>ww.</span>domain.com"
    1. Copy EC2 IP4 address to Type A record name
1. **In settings.py change ALLOWED HOSTS to new domain**
1. **Set DEBUG = False**
1. **Test that everything is working**

### Security Certificate

1. **Set up Certbot or equivalent**
    1. sudo apt-get update
    1. sudo apt-get install software-properties-common
    1. sudo add-apt-repository universe
    1. sudo snap install core; sudo snap refresh core
    1. sudo apt-get remove certbot
    1. sudo snap install --classic certbot
1. **Edit .conf file**
    1. sudo nano /etc/apache2/sites-available/django_project.conf
    1. set ServerName to domain name
    1. Temporarily comment out the three WSGI lines at the bottom
    1. Ctrl x, y, Enter
1. **Run certbot to auto-update configuration settings**
    1. sudo certbot –apache
    1. input email address, A, No, Enter, 2
1. **Modify old .conf file**
    1. sudo nano /etc/apache2/sites-available/django_project.conf
    1. Delete Alias, Directory, and WSGI lines only
    1. Ctrl x, y, Enter
1. **Modify new .conf file**
    1. sudo nano /etc/apache2/sites-available/django_project-le-ssl.conf
    1. Uncomment out WSGI lines
1. **Test**
    1. sudo apachectl configtest
    1. sudo service apache2 restart
    1. Test the site
1. **Turn on the last of the security settings**
    1. Leave HSTS seconds at 60 for now to avoid breaking the site (we will gradually increase this over time)
    1. Test new settings
3. **Setup auto rewew**
    1. sudo certbot renew--dry-run
    1. sudo crontab -e, 1 to use nano
    1. Add cron commands, also add command to periodically expire the Sandbox-Import repository
    1. Manually renew if needed
    1. sudo certbot renew –apache

### Add auto update to crontabs

1. **Open crontab file for editing**
    1. cd /etc/
    1. sudo nano crontab -e
    1. Add Ubuntu update command

# Build Status

Deployed. Site recieves periodic updates.

# Languages/Frameworks/Tools Used

### Tools
Visual Studio Code, Pycharm

### Backend
Python, Django, Django REST, AWS, Apache2, Ubuntu, Postgres, Sqlite

### Frontend
Bootstrap, HTML, CSS, SCSS, Javascript, AJAX

# License

No copyright. GitHub clone, Rex Mitchell
