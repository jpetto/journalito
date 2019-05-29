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

TBD