# webauthv2
login service with support for partial password entry

## About the Project

<a href="https://webauthv2.ml">webauthv2</a> is a proof-of-concept flask website, written mainly in Python.
The source code is tested and compatible with both Python 2 and 3, given certain relevant dependancies are correct.

The Flask microservice is aided by a collection of libraries (see <code>requirements.txt</code>) which allows usage of SQL options such as SQLite for a local service, or MySQL for a production website, as well as intelligent forms for secure password entry. Other microservice Jinja, bundled with Flask, allows for python written into HTML files allowing variable comparison and other useful trickery.

The premise webauthv2 is built upon is that the full entry of a password for a login, even when one-time-authenication is supported, is not inherently secure. Many people re-use passwords and logins for multiple services for ease-of-use, and logging into a OTA-protected service on a compromised computer can still leave a user vulnerable on other services that are not OTA-protected.

To solve this, webauthv2 offers two login options after OTA: standard password login, and partial password login. The database stores a number of selections of 4-digit combinations derived from a users password, and the partial password login will require only certain digits. While these digits would still be made available to malicious parties on a compromised computer, the secure storing of the fully-hashed password will prevent a third-party from access to the full password.
This proof-of-concept is not designed with repeated compromised logins on the same computer, as our implementation stores 3 unique hashed copies of the 4 digit combinations of password digits, and making all these digits available to a third-party can leave users vulnerable to brute-force style attacks on other services utilising the same login and password that aren't also OTA protected.

The login process is handled in 3 steps: username verification, OTA code verification, password verification. OTA code is sent via email to the user, which when entered will allow the user to choose which password option to avail of. Standard password login is a simple hash comparison, while partial password login is a hash comparison of the relevant digits. To achieve a secure password storage in the database, password length is restricted to a minimum of 12 characters, and each of the three combinations of partial password characters are generated, hashed, and stored at registration. Every partial password login is also a hash comparison.

For simplicity, given a compromised system will most certainly have at minimum a keylogger and foreign access to the system, the required partial password digits are given in plain text both in the website url at the login stage, and on the page. Note that if there is no keylogger, as the password entry method is secure there is no risk of vulnerability due to this implementation.

## HTML files
<code>/app/templates/</code> stores relevant html files, rendered in <code>/app/routes.py</code>.

Using Jinja, a templating language implemented by Flask, we can use multiple html files on a single page, and support insertion of html files into other files.

Jinja also allows for use of logic statements in html files, and passthrough of python variables, which is how we can show user preference CSS and other personalised information / messages.

## CSS files

<code>/app/static/</code> hosts static assets such as the CSS and font files.

The CSS is similarly structured to the html; supported with a base file, extended by similar extension files, but also with an animations files "wild.css". The HTML elements declared in our files are rendered as flex boxes to correctly format our page for any size browser window. At this time the mobile interface is a functional one, but customer sizing and other mobile-centric features are not supported.

## Models and Database

<code>/app/models.py</code> details the relevant models our SQL database is created from.

SQLalchemy is the Flask plugin we use to populate our database, whether the local SQLite option of a MySQL hosted database. It provides Object-relational Mapping features that allow python objects (our <code>User</code> class) to be mapped into our database.

<code>models.py</code> also employs several functions to compute our partial-password and relevant hashes (supported by FlaskLogin). SQLalchemy sanitises database inputs.

## User Input via Forms

<code>/app/forms.py</code> handles the forms created by plugin WTForms, rendered in <code>/app/routes.py</code>.

This extension provides form validation, custom error messages, and other useful functionality to ensure minimum password length, password matching login etc.

## Error Handling

<code>/app/errors.py</code> handles user navigation to non-existent pages.

This file could be expanded to support other errors, such as database errors etc, but if the project is correctly setup the only error page the user should experience is the included "Error 404".

## Routes

<code>/app/routes.py</code> details the pages, routes between them, and other additional code such as the OTA services.

This is where the bulk of the code and logic is located. All other files are employed here, where routing handled by Flask itself serves relevant HTML files to the user, handles database queries, insertions, and updates. It also provides the OTA services and GeoIP service for the home page.

Due to current limitations in our knowledge of server-side sessions, we pass a <code>user_hash</code> variable through the url in the login process to avoid premature login, and allow the multi-step process to function as a single process. This isn't inherently more insecure than using an encrypted session, as a login attempt must still go through every login step to authenticate a user. However in an improved system we acknowledge that this information would not be contained within the url.

## Local Installation

The following commands inside the working directory will launch the project with all installed dependencies. it is recommended to set up a virtual environment before using <code>pip install</code>.

<pre><code>pip install -r requirements.txt
bash fixdb
flask run
</code></pre>

<code>fixdb</code> is a short bash script to generate an SQLite database and do an initial migration, it can be discarded if you wish to run these commands yourself.

A .env file must also be created, with relevant information filled in to allow a production server, SQL support, etc:
<pre><code>SECRET_KEY=		// for secure public hosting, can be anything
MAIL_SERVER=		// relative to the email address used
MAIL_PORT=		// server dependent
MAIL_EMAIL=		// owner email address, configured correctly for insecure login
MAIL_PASSWORD=		// relevant password
DB_URL=			// used for a web-hosted SQL database
ENVIRONMENT=		// 0 for local SQLite db, 1 for MySQL with DB_URL
ACCOUNT_SID=		// twilio account
AUTH_TOKEN=		// twilio auth token
USER_PHONE_NUMBER=	// this would be removed upon proper implementation of user phone number in the database
PHONE_NUMBER=		// twilio host phone number
CAPTCHA_PRIVATE=	// provided by Google for ReCaptcha v2 support
CAPTCHA_PUBLIC=		// provided by Google for ReCaptcha v2 support
</code></pre>

## Final Notes

Due to maintaining this project as 'free to run' the OTA via text functionality is implemented using Twilio's free offer. The database would need to be expanded to include a user phone number, and relevant methods in routes.py would need to be modified to support sending a text to a number other than the listed <code>PHONE_NUMBER</code> environment variable.

This proof-of-concept was built for module CSU33BC1 at Trinity College Dublin, and inspired by similar concepts such as Bank of Ireland's 365online partial-code login.

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
