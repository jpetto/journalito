Basically a customized version of [Miguel Grinberg's excellent Flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). A web version (yucK!) of [Gretchen Rubin's One-Sentence Journal](https://www.goodreads.com/book/show/38621692-the-happiness-project-one-sentence-journal).

# Setup

1. Create a virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Upgrade pip: `pip install --upgrade pip`
4. Install requirements: `pip install -r requirements.txt`

## DB

1. Inintialize the database: `flask db init`
2. Create migrations: `flask db migrate`
3. Run the migrations: `flask db upgrade`

## Testing email error handling

1. Start a fake SMTP server: `python -m smtpd -n -c DebuggingServer localhost:8025`
2. Make sure `FLASK_DEBUG=0`
3. Put `MAIL_SERVER=localhost` and `MAIL_PORT=8025` in your `.env` file


## Deploying on Linode

### Set up the daterbase

1. Connect to MySQL as your custom user (see Ansible branch): `mysql -u
   [someusername] -p` (enter your password when prompted)
2. Create the new database: `create database journalito character set utf8
   collate utf8_bin;`
3. Create a user for this specific application/database: `create user
   'journalito'@'localhost' identified by 'SOMEGOODPASSWORD';`
4. Grant this new user privileges: `grant all privileges on journalito.* to
   'journalito'@'localhost';`
5. Reload/flush privileges: `flush privileges;`
6. Exit MySQL: `quit;`

### Install the application

Make sure you're in the correct user's home directory (see Ansible branch),
then:

1. `mkdir src && cd src`
2. `git clone [repo URL]`
3. `cd journalito`
4. Set up your virtual environment: `python3 -m venv venv`
5. Activate your venv: `source venv/bin/activate`
6. Install core packages: `pip install -r requirements.txt`

*Note!* If the above throws erorrs like `error: invalid command 'bdist_wheel'`:
	a. Deactivate the venv: `deactivate`
	b. Delete the `venv` directory: `rm -r venv`
	c. Repeat steps 4 and 5 above, then before step 6, run: `pip install
wheel`

7. Install production packages: `pip install -r requirements-prod.txt`
8. Get the database in order: `flask db upgrade`

### Start the application

1. Configure supervisor to run the application privately on port 8000:

```
[program:journalito]
command=/home/deployer/src/journalito/venv/bin/gunicorn -b localhost:8000 -w 4 journalito:flapp
directory=/home/deployer/src/journalito
user=deployer
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

2. Set up an SSL cert TODO
3. Configure nginx TODO

### Update the application

1. Get the new code: `git pull`
2. Stop the server real quick: `sudo supervisorctl stop journalito`
3. Update the db: `flask db upgrade`
4. Start ye olde server back up: `sudo supervisorctl start journalito`

