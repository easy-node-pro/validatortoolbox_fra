import subprocess, re, bleach, secrets
from flask import Flask, redirect, url_for, session, render_template
from os import environ
from flask_httpauth import HTTPBasicAuth
from config import easy_env_fra
from library import load_var_file, ask_yes_no, set_var

load_var_file(easy_env_fra.dotenv_file)

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(32)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == environ.get("USERNAME") and password == environ.get("PASSWORD"):
        return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats")
@auth.login_required
def test():
    output = (
        subprocess.run(
            ["python3", f"{easy_env_fra.toolbox_location}/src/app.py", "-s"],
            capture_output=True,
        )
        .stdout.decode()
        .replace("\n", "<br>")
        .replace("\x1b[H\x1b[2J\x1b[3J\x1b[35m", "")
        .strip()
    )
    output = re.sub(r"\x1b[^m]*m", "", output)
    output = bleach.linkify(output)
    time_left = 60  # refresh interval in seconds
    return render_template("stats.html", output=output, time_left=time_left)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


def setupUserAccount():
    if environ.get("USERNAME") is None:
        username = input("No User Name found, please input a username: ")
        answer = ask_yes_no(f"* You picked {username}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dotenv_file, "USERNAME", username)
        else:
            raise SystemExit(0)

    if environ.get("PASSWORD") is None:
        password = input("No password found, please input a password now: ")
        answer = ask_yes_no(f"* You picked {password}, is that correct? (Y/N) ")
        if answer:
            set_var(easy_env_fra.dotenv_file, "PASSWORD", password)
        else:
            raise SystemExit(0)


if __name__ == "__main__":
    setupUserAccount()
    app.run(host="0.0.0.0", port=5555)
