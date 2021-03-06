"""Basic wizard for setting up microblog.pub configuration files."""
import os
import binascii
from pathlib import Path

import bcrypt
from prompt_toolkit import prompt
from markdown import markdown


def main():
    print("Welcome to microblog.pub setup wizard\n")

    dat = {}
    print("Your identity will be @{username}@{domain}")
    dat["domain"] = prompt("domain: ")
    dat["username"] = prompt("username: ")
    dat["password"] = bcrypt.hashpw(
        prompt("password: ", is_password=True).encode(), bcrypt.gensalt()
    ).decode()
    dat["name"] = prompt("name (e.g. John Doe): ")
    dat["summary"] = markdown(
        prompt(
            "summary (short description, in markdown, press [ESC] then [ENTER] to submit):\n",
            multiline=True,
        )
    )
    dat["https"] = True
    proto = "https"
    yn = ""
    while yn not in ["y", "n"]:
        yn = prompt("will the site be served via https? (y/n): ", default="y").lower()
    if yn == "n":
        dat["https"] = False
        proto = "http"

    dat["icon_url"] = prompt(
        "icon URL: ", default=f'{proto}://{dat["domain"]}/static/nopic.png'
    )

    out = ""
    for k, v in dat.items():
        out += f"{k}: {v!r}\n"
    print(out)
    print()

    env_file = {
        "WEB_PORT": 5005,
        "CONFIG_DIR": "./config",
        "DATA_DIR": "./data",
        "POUSSETACHES_AUTH_KEY": binascii.hexlify(os.urandom(32)).decode(),
        "COMPOSE_PROJECT_NAME": Path.cwd().name.replace(".", ""),
    }

    out2 = ""
    for k, v in env_file.items():
        out2 += f"{k}={v}\n"

    print(out2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
