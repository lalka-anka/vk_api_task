from urllib.request import Request, urlopen
import json
import webbrowser
import os
import argparse


def get_friends(user_id, token, version):
    if not user_id.isdigit():
        try:
            user_id = get_right_id(user_id, token, version)
        except KeyError:
            raise ValueError("user does not exist")

    friends = f"https://api.vk.com/method/friends.get?user_id={user_id}" + f"&order=name&fields=nickname,domain&access_token={token}&v={version}"
    try:
        return request(friends)['response']
    except KeyError:
        raise KeyError(f"{request(friends)['error']['error_msg']}")


def request(req_message):
    req_obj = Request(req_message,
                      headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req_obj)
    return json.loads(page.read())


def get_right_id(screen_name, token, version):
    id = f"https://api.vk.com/method/users.get?user_ids={screen_name}" + f"&access_token={token}&v={version}"
    response = request(id)
    return response["response"][0]["id"]


def build_page(st, name):
    html = """<!DOCTYPE html>
                        <html lang="ru">
                        <head>
                        <title>friends</title>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                        body {
                          font-family: Times New Roman;
                          margin: 0;
                        }
                        .header {
                          padding: 30px;
                          text-align: center;
                          background: #0066CC;
                          color: white;
                          font-size: 30px;
                        }
                        .content {
                        padding:20px;
                        text-align: center;
                        background: #EEEEEE;
                        }
                        </style>
                        </head>
                        <body>
                        <div class="header">
                          <p>The result of the program for finding friends by vk's API:</p>
                        </div>
                        <div class="content">
                          <h1>friends of vk id: """ + name + """</h1>
                          %s
                        </div>
                        </body>
                        </html>
                        """ % st
    with open("friends.html", 'w', encoding="utf-8") as f:
        f.write(html)


if __name__ == '__main__':
    version = "5.103"
    parser = argparse.ArgumentParser()
    parser.add_argument("-uid", required=True,
                        help="id or domain screen name of user\nexample: -id 77745017 OR -id 77745017 OR -id lalka_anka")
    parser.add_argument("-tkn", required=True, help="access token of vk application")
    args = parser.parse_args()
    tkn = args.tkn
    user_id = args.uid
    rep = get_friends(user_id, tkn, version)['items']
    res = "\n".join(["<p>" + f'<a href="https://vk.com/id{r["id"]}">'
                     + r['first_name'] + " " + r['last_name']
                     + "</a>" + "</p>" for r in rep])
    build_page(res, user_id)
    url = os.getcwd() + "friends.html"
    webbrowser.open(url, new=1)
