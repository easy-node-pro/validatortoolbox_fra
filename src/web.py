import subprocess, re, bleach
from os import environ
from flask_httpauth import HTTPBasicAuth
from flask import Flask, render_template
from config import easy_env_fra
from library import load_var_file, ask_yes_no, set_var

load_var_file(easy_env_fra.dotenv_file)

app = Flask(__name__)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == environ.get("USER") and password == environ.get("PASSWORD"):
        return True
    return False


@app.route("/")
def index():
    output = subprocess.run(
        ["python3", f"{easy_env_fra.toolbox_location}/src/app.py", "-s"], capture_output=True
    ).stdout.decode().replace("\n", "<br>").replace('\x1b[H\x1b[2J\x1b[3J\x1b[35m', '').strip()
    output = re.sub(r'\x1b[^m]*m', '', output)
    output = bleach.linkify(output)
    return render_template("index.html", output=output)


@app.route("/test")
@auth.login_required
def test():
    output = "Hello world!"
    return render_template("index.html", output=output)


def setupUserAccount():
    if environ.get("USER") == False:
        user = input("No User Name found, please input a username: ")
        answer = ask_yes_no(f"* You picked {user}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dotenv_file, "USER", user)
        else:
            raise SystemExit(0)
    if environ.get("PASSWORD") == False:
        password = input("No password found, please input a password now: ")
        answer = ask_yes_no(f"* You picked {password}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dotenv_file, "PASSWORD", password)
        else:
            raise SystemExit(0)
    return


if __name__ == "__main__":
    setupUserAccount()
    app.run(host='0.0.0.0', port=5555)
