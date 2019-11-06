# webauthv2
login service with support for partial password entry

<a href="https://webauthv2.ml">webauthv2</a> is a proof-of-concept flask website, written mainly in Python.
The source code is tested and compatible with both Python 2 and 3, given certain relevant dependancies are correct.

The Flask microservice is aided by a collection of libraries (see requirements.txt) which allows usage of SQL options such as SQLite for a local service, or MySQL for a production website, as well as intelligent forms for secure password entry. Other microservice Jinja, bundled with FLask, allows for python written into .html files allowing variable comparison and other useful trickery.

The premise webauthv2 is built upon is that the full entry of a password for a login, even when one-time-authenication is supported, is not inherently secure. Many people re-use passwords and logins for multiple services for ease-of-use, and logging into a OTA-protected service on a compromised computer can still leave a user vulnerable on other services that are not OTA-protected.

To solve this, webauthv2 offers two login options after OTA: standard password login, and partial password login. The database stores a number of selections of 4-digit combinations derived from a users password, and the partial password login will require only certain digits. While these digits would still be made available to malicious parties on a compromised computer, the secure storing of the fully-hashed password will prevent a third-party from access to the full password.
This proof-of-concept is not designed with repeated compromised logins on the same computer, as our implementation stores 3 unique hashed copies of the 4 digit combinations of password digits, and making all these digits available to a third-party can leave users vulnerable to brute-force style attacks on other services utilising the same login and password that aren't also OTA protected.

The login process is handled in 3 steps: username verification, OTA code verification, password verification. OTA code is sent via email to the user, which when entered will allow the user to choose which password option to avail of. Standard password login is a simple hash comparison, while partial password login is a hash comparison of the relevant digits. To achieve a secure password storage in the database, password length is restricted to a minimum of 12 characters, and each of the three combinations of partial password characters are generated, hashed, and stored at registration. Every partial password login is also a hash comparison.

For simplicity, given a compromised system will most certainly have at minimum a keylogger and foreign access to the system, the required partial password digits are given in plain text both in the website url at the login stage, and on the page. Note that if there is no keylogger, as the password entry is secure visually and through transit (https only on the production server), there is no risk of vulnerability due to this implmentation.

/app/templates stores relevant html files, rendered in /app/routes.py.

/app/static hosts static assets such as the CSS and font file.

/app/models.py details the relevant models our SQL database is created from.

/app/forms.py handles the forms created by plugin WTForms, rendered in /app/routes.py.

/app/routes.py details the pages, routes between them, and other additional code such as the OTA email.

To install and run locally:

<pre><code>pip install -r requirements.txt
bash fixdb
flask run
</code></pre>

<pre><code>fixdb</code></pre> is a short bash script to generate an SQLite database and do an initial migration.

A .env file must also be created, with relevant information filled in to allow a production server, SQL support, and OTA by email support.
<pre><code>SECRET_KEY=
MAIL_SERVER=
MAIL_PORT=
MAIL_EMAIL=
MAIL_PASSWORD=
DB_URL=
ENVIRONMENT= (0 for local SQLite db, 1 for MySQL with DB_URL)
</code></pre>

This proof-of-concept was built for module CSU33BC1 at Trinity College Dublin, and inspired by similar concepts such as Bank of Ireland's 365online partial-code login.

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
