import subprocess
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
@auth.login_required
def index():
    output = subprocess.run(
        ["python3", "~/validatortoolbox_fra/src/app.py", "-s"], capture_output=True
    ).stdout
    return render_template("index.html", output=output)


def setupUserAccount():
    if not environ.get("USER"):
        user = input("No User Name found, please input a username: ")
        answer = ask_yes_no(f"* You picked {user}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dot_env, "USER", user)
        else:
            raise SystemExit(0)
    if not environ.get("PASSWORD"):
        password = input("No password found, please input a password now: ")
        answer = ask_yes_no(f"* You picked {password}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dot_env, "PASSWORD", password)
        else:
            raise SystemExit(0)


if __name__ == "__main__":
    setupUserAccount()
    app.run(port=5555)
