import tkinter as tk
from tkinter import filedialog
import requests
import json
import bs4
import re
from urllib.parse import quote
import random


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("gmoj gui")

        self.leftframe = tk.Frame(self, background="#aaaaaa")
        self.leftframe.pack(side="left", expand=False, fill="y")

        self.titlelabel = tk.Label(self, text="gmoj gui by Aaron", background="#cccccc")
        self.titlelabel.pack(side="top", fill="x")

        self.rightframe = tk.Frame(self, background="#eeeeee")
        self.rightframe.pack(side="right", expand=True, fill="both")

        self.userbtn = tk.Button(
            self.leftframe, text="userinfo", width=10, command=self.userinfo
        )
        self.userbtn.grid(row=0, column=0, padx=10, pady=5)

        self.veiwbtn = tk.Button(
            self.leftframe, text="download", width=10, command=self.download
        )
        self.veiwbtn.grid(row=1, column=0, padx=10, pady=5)

        self.searchbtn = tk.Button(
            self.leftframe, text="search", width=10, command=self.search
        )
        self.searchbtn.grid(row=2, column=0, padx=10, pady=5)

        self.helpbtn = tk.Button(
            self.leftframe, text="help", width=10, command=self.help
        )
        self.helpbtn.grid(row=3, column=0, padx=10, pady=5)

        self.headers = {
            "authority": "gmoj.net",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://gmoj.net",
            "pragma": "no-cache",
            "referer": "https://gmoj.net/senior/",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "x-requested-with": "XMLHttpRequest",
        }
        self.cookies = {}
        self.username = ""
        self.password = ""

    def clear_right_frame(self):
        for widget in self.rightframe.winfo_children():
            widget.destroy()

    def turn(self, fun):
        def __fun():
            self.set("gmoj gui")
            self.clear_right_frame()
            fun()

        return __fun

    def set(self, str="gmoj gui by Aaron"):
        self.titlelabel.config(text=str)
        self.clear_right_frame()

    def error(self, code):
        __level = tk.Toplevel()
        __level.title("Error")

        tk.Label(__level, text=f"Error: {code}", width=len(str(code)) + 10).grid(
            row=0, column=0, padx=10, pady=5
        )
        tk.Button(__level, text="OK", width=10, command=__level.destroy).grid(
            row=1, column=0, padx=10, pady=5
        )

    def log(self, code):
        __level = tk.Toplevel()
        __level.title("Log")

        tk.Label(__level, text=f"{code}", width=len(str(code)) + 10).grid(
            row=0, column=0, padx=10, pady=5
        )
        tk.Button(__level, text="OK", width=10, command=__level.destroy).grid(
            row=1, column=0, padx=10, pady=5
        )

    def userinfo(self):
        self.set("userinfo")

        tk.Button(self.rightframe, text="login", width=10, command=self.login).grid(
            row=0, column=0, padx=10, pady=5
        )

        tk.Button(self.rightframe, text="export", width=10, command=self.export).grid(
            row=1, column=0, padx=10, pady=5
        )

        tk.Button(self.rightframe, text="load", width=10, command=self.load).grid(
            row=2, column=0, padx=10, pady=5
        )

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.set,
        ).grid(row=3, column=0, padx=10, pady=5)

    def download(self):
        self.set("download")

        if not self.cookies:
            self.error("Please login")
            return

        tk.Button(
            self.rightframe, text="problem", width=10, command=self.downloadproblem
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe, text="contest", width=10, command=self.downloadcontest
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.set,
        ).grid(row=2, column=0, padx=10, pady=5)

    def search(self):
        self.set("search")

        if not self.cookies:
            self.error("Please login")
            return

        tk.Button(self.rightframe, text="user", width=10, command=self.searchuser).grid(
            row=0, column=0, padx=10, pady=5
        )

        tk.Button(
            self.rightframe, text="problem", width=10, command=self.searchproblem
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe, text="public code", width=10, command=self.searchpubliccode
        ).grid(row=2, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.set,
        ).grid(row=3, column=0, padx=10, pady=5)

    def help(self):
        self.set("help")

        tk.Label(
            self.rightframe,
            text="""help : show this page
unserinfo:
 - login  : by inputting username and password to login
 - export : if you have loginned, you can export the loginned information to file(json)
 - load   : you can load a loginned information json to login (Recommended)
 - return : return the home page
download :
 - download contest : if you have loginned, you can download the contest to file(html)
 - download problem : if you have loginned, you can download the problem to file(html)
 - return : return the home page
search   :
 - search user        : if you have loginned, you can get information of name what you searched
 - search problem     : if you have loginned, you can get problem id what you searched
 - search public code : if you have loginned, you can get the std what you searched problem
 - return : return the home page
""",
            width=100,
            height=10,
            justify="left",
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.set,
        ).grid(row=1, column=0, padx=10, pady=5)

    def login(self):
        self.set("login")

        tk.Label(self.rightframe, text="username: ").grid(row=0, column=0, pady=5)
        tk.Label(self.rightframe, text="password: ").grid(row=1, column=0, pady=5)

        usernameentry = tk.Entry(self.rightframe, width=30)
        usernameentry.grid(row=0, column=1, pady=5)
        passwordenrty = tk.Entry(self.rightframe, show="*", width=30)
        passwordenrty.grid(row=1, column=1, pady=5)

        def __login():
            self.username = usernameentry.get()
            self.password = passwordenrty.get()
            try:
                response = requests.post(
                    "https://gmoj.net/senior/index.php/main/login",
                    headers=self.headers,
                    data={
                        "username": self.username,
                        "password": self.password,
                    },
                    timeout=1,
                )
                response.raise_for_status()
                assert response.text == "success"

                for items in response.cookies:
                    self.cookies.setdefault(items.name, items.value)

                self.log("Login success")

            except TimeoutError:
                self.error("Timeout")
            except Exception as e:
                self.error(e)

        tk.Button(self.rightframe, text="ok", width=10, command=__login).grid(
            row=3, column=0, padx=10, pady=5
        )

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.turn(self.userinfo),
        ).grid(row=4, column=0, padx=10, pady=5)

    def export(self):
        file_path = filedialog.asksaveasfilename(
            title="Save as json",
            defaultextension=".json",
            filetypes=[("JSON", ".json")],
        )

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(
                    json.dumps({"cookies": self.cookies, "username": self.username})
                )
            self.log("OK")
        except Exception as e:
            self.error(e)

    def load(self):
        file_path = filedialog.askopenfilename(
            title="load json",
            defaultextension=".json",
            filetypes=[("JSON", ".json")],
        )

        try:
            __json = json.loads(open(file_path, encoding="utf-8").read())
            self.username = __json["username"]
            self.cookies = __json["cookies"]
            self.log(f"OK, username is {self.username}")
        except Exception as e:
            self.error(e)

    def downloadcontest(self):
        self.set("download contest")

        tk.Label(self.rightframe, text="contest: ").grid(row=0, column=0, pady=5)
        contestentry = tk.Entry(self.rightframe, width=10)
        contestentry.grid(row=0, column=1, padx=10, pady=5)
        contest = ""

        def __getcontest():
            contest = contestentry.get()

            try:
                file_path = filedialog.askdirectory(title="Save path")

                response = requests.get(
                    f"https://gmoj.net/senior/index.php/contest/problems/{contest}",
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=1,
                )
                response.raise_for_status()
                content = response.content.decode(encoding="utf-8", errors="igore")

                soup = bs4.BeautifulSoup(content, "html.parser")
                problemnum = len(soup.find_all("td")) // 2

                for i in range(problemnum):
                    response = requests.get(
                        f"https://gmoj.net/senior/index.php/contest/show/{contest}/{i}",
                        cookies=self.cookies,
                        headers=self.headers,
                        timeout=1,
                    )
                    response.raise_for_status()

                    with open(file_path + f"/{i}", "wb") as f:
                        f.write(response.content)

                self.log("OK")
            except TimeoutError:
                self.error("Timeout")
            except Exception as e:
                self.error(e)

        tk.Button(
            self.rightframe, text="download", width=10, command=__getcontest
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.turn(self.download),
        ).grid(row=2, column=0, padx=10, pady=5)

    def downloadproblem(self):
        self.set("download problem")

        tk.Label(self.rightframe, text="problem: ").grid(row=0, column=0, pady=5)
        problementry = tk.Entry(self.rightframe, width=10)
        problementry.grid(row=0, column=1, padx=10, pady=5)
        problem = ""

        def __getproblem():
            problem = problementry.get()

            try:
                file_path = filedialog.asksaveasfilename(
                    title="Save as html",
                    defaultextension=".html",
                    filetypes=[("HTML", ".html")],
                )

                response = requests.get(
                    f"https://gmoj.net/senior/index.php/main/show/{problem}",
                    cookies=self.cookies,
                    headers=self.headers,
                    timeout=1,
                )
                response.raise_for_status()

                with open(file_path, "wb") as f:
                    f.write(response.content)
                self.log("OK")
            except TimeoutError:
                self.error("Timeout")
            except Exception as e:
                self.error(e)

        tk.Button(
            self.rightframe, text="download", width=10, command=__getproblem
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            self.rightframe,
            text="return",
            width=10,
            command=self.turn(self.download),
        ).grid(row=2, column=0, padx=10, pady=5)

    def searchuser(self):
        self.set("search user")

        tk.Label(self.rightframe, text="username: ", width=10).grid(
            row=0, column=0, pady=5
        )

        usernameentry = tk.Entry(self.rightframe, width=30)
        usernameentry.grid(row=0, column=1, pady=5)

        __frame = tk.Frame(self.rightframe)
        __frame.grid(row=1, column=0, padx=10, pady=5)

        codelabel = tk.Label(self.rightframe, text="Please search", width=50, height=10)
        codelabel.grid(row=1, column=1, padx=10, pady=5)

        def __searchuser():
            try:
                response = requests.post(
                    f"https://gmoj.net/senior/index.php/users/{quote(usernameentry.get())}",
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=1,
                )
                response.raise_for_status()

                file = response.text

                soup = bs4.BeautifulSoup(file, "html.parser")

                hrefs = soup.find_all("a")
                blog = None

                for href in hrefs:
                    if href.text.find("Blog") != -1:
                        blog = href.get("href")
                        break

                text = re.sub("<[^>]+>", "", file)
                item = text.split()
                while item and item[0] != "uid":
                    item.pop(0)
                k1, k2 = 0, 0

                for i in range(len(item)):
                    if item[i][0] == "$":
                        k1 = i
                        break
                    if item[i] == "AC":
                        k2 = i

                while len(item) > k1:
                    item.pop(k1)

                item[k2] += " " + item[k2 + 1]
                item.pop(k2)

                labeltext = f"blog: {blog}\n"
                for i in range(0, len(item), 2):
                    labeltext += f"{item[i]}: {item[i + 1]}\n"

                codelabel.config(text=labeltext)

            except TimeoutError:
                self.error("Timeout")
            except Exception as e:
                self.error(e)

        tk.Button(__frame, text="search", width=10, command=__searchuser).grid(
            row=0, column=0, padx=10, pady=5
        )

        tk.Button(
            __frame,
            text="return",
            width=10,
            command=self.turn(self.search),
        ).grid(row=1, column=0, padx=10, pady=5)

    def searchproblem(self):
        self.set("search problem")

        tk.Label(self.rightframe, text="problem: ", width=10).grid(
            row=0, column=0, pady=5
        )
        problementry = tk.Entry(self.rightframe, width=30)
        problementry.grid(row=0, column=1, padx=10, pady=5)

        __frame = tk.Frame(self.rightframe)
        __frame.grid(row=1, column=0, padx=10, pady=5)

        problemlabel = tk.Label(
            self.rightframe,
            text="Please search, and author try to format but still messy\nif you have better formatter, please call me at github`-`",
            width=100,
            height=25,
            justify="left",
        )
        problemlabel.grid(row=1, column=1, padx=10, pady=5)

        def __searchproblem():
            try:
                params = {
                    "search": quote(problementry.get()),
                }

                response = requests.get(
                    "https://gmoj.net/senior/index.php/main/problemset",
                    params=params,
                    cookies=self.cookies,
                    headers=self.headers,
                )

                response.raise_for_status()

                soup = bs4.BeautifulSoup(response.text, "html.parser")

                labeltext = "%-7s %-50s %-6s %-7s %s\n" % (
                    "Problem",
                    "Title",
                    "Solved",
                    "Submit",
                    "Average",
                )
                cnt = 0

                for item in soup.find_all("a"):
                    if item.get("href"):
                        id = str(item.text)
                        cnt += 1
                        if cnt == 1:
                            labeltext += "%-7s " % id.strip()
                        elif cnt == 2:
                            labeltext += "%-50s " % id.strip()
                        elif cnt == 3:
                            labeltext += "%-6s " % id.strip()
                        elif cnt == 4:
                            labeltext += "%-7s " % id.strip()
                        else:
                            cnt = 0
                            labeltext += id.strip() + "\n"

                problemlabel.config(text=labeltext)

            except TimeoutError:
                self.error("Timeout")
            except Exception as e:
                self.error(e)

        tk.Button(__frame, text="search", width=10, command=__searchproblem).grid(
            row=0, column=0, padx=10, pady=5
        )

        def __random():
            problemlabel.config(text=str(random.randrange(1000, 6667)))

        tk.Button(__frame, text="random", width=10, command=__random).grid(
            row=1, column=0, padx=10, pady=5
        )

        tk.Button(
            __frame,
            text="return",
            width=10,
            command=self.turn(self.search),
        ).grid(row=2, column=0, padx=10, pady=5)

    def searchpubliccode(self):
        self.set("search public code")

        tk.Label(self.rightframe, text="problem: ", width=10).grid(
            row=0, column=0, pady=5
        )

        problementry = tk.Entry(self.rightframe, width=30)
        problementry.grid(row=0, column=1, pady=5)

        __frame = tk.Frame(self.rightframe)
        __frame.grid(row=1, column=0, padx=10, pady=5)

        codelabel = tk.Label(self.rightframe, text="Please search", width=50, height=10)
        codelabel.grid(row=1, column=1, padx=10, pady=5)

        def __searchcode():
            labeltext = ""

            for i in range(10):
                try:
                    response = requests.post(
                        f"https://gmoj.net/senior/index.php/main/status/{i}?problems[]={problementry.get()}&status[]=0",
                        headers=self.headers,
                        cookies=self.cookies,
                        timeout=1,
                    )
                    response.raise_for_status()
                    soup = bs4.BeautifulSoup(response.text, "html.parser")

                    for item in soup.find_all("tr"):
                        if str(item).find("icon-globe") != -1:
                            labeltext += (
                                f"https://gmoj.net/senior/#main/code/{item.td.text}\n"
                            )
                    codelabel.config(text=labeltext)

                except TimeoutError:
                    self.error("Timeout")
                except Exception as e:
                    self.error(e)

        tk.Button(__frame, text="search", width=10, command=__searchcode).grid(
            row=0, column=0, padx=10, pady=5
        )

        tk.Button(
            __frame,
            text="return",
            width=10,
            command=self.turn(self.search),
        ).grid(row=1, column=0, padx=10, pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
