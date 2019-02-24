import io
import os
from dataclasses import dataclass
import random
from enum import Enum

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from bs4 import BeautifulSoup
from fetch import Fetcher
import tkinter as tk


class Department(Enum):
    ENGINEERING = 1
    OTHER = 0


@dataclass
class Friend:
    name: str
    title: str
    img: str
    department: Department


fetcher = Fetcher()


def load_users():

    users = []
    soup = BeautifulSoup(fetcher.fetch("https://reciprocitylabs.com/team/"), 'html5lib')
    for parent in soup.find_all('ul', attrs={'class': 'team-list'}):
        for li in parent.find_all('li', recursive=False):
            img = li.find('img')['src']
            name = li.find_all('span')[0].string
            title = li.find_all('span')[1].string
            dept = Department.ENGINEERING if 'engineering' in li['class'] else Department.OTHER
            users.append(Friend(name, title, img, dept))
    return users


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.all_friends = load_users()
        self.reset_friends()
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.panel = tk.Label()
        self.panel.pack(fill=tk.X, expand=1)
        self.name = tk.Label()
        self.name.pack()
        self.title = tk.Label()
        self.title.pack()
        self.next = tk.Button(self)
        self.next.pack()
        self.next_friend()

    def guess(self):
        self.name['text'] = self.friend.name
        self.title['text'] = self.friend.title
        self.next['command'] = self.next_friend
        self.next['text'] = "Next"

    def reset_friends(self):
        self.friends = [x for x in self.all_friends if x.department == Department.ENGINEERING]
        random.shuffle(self.friends)

    def next_friend(self):
        self.name['text'] = ''
        self.title['text'] = ''
        self.friend = self.friends.pop()

        if not self.friends:
            self.reset_friends()

        image_bytes = fetcher.fetch(self.friend.img)
        img = PhotoImage(file=io.BytesIO(image_bytes))
        self.panel.configure(image=img)
        self.panel.image = img
        self.next['text'] = "Guess"
        self.next['command'] = self.guess


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Work 2 Friends")
    app = Application(master=root)
    app.mainloop()
