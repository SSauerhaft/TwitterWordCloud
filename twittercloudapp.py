##This is an app that gets a twitter username from user input,
#and pulls that twitter timeline from the twitter api, and then
#builds a wordcloud from the relative word frequencies.
######################################################
# In order to run:
# -- must have python installed
# -- pip install pyi_rth__tkinter
# -- pip install python-twitter
# -- pip install WordCloud
# run in terminal using python twittercloudapp.py
#######################################################


import tkinter as tk
from tkinter import *
import twitter
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageTk



LARGE_FONT = ("Verdana", 14)

class twittercloudapp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.display_wordcloud(master)

    ## format what the app windiw is going to look like
    def setup_window(self, master):
        self.f = tk.Frame(master, height=1000, width=600, padx=10, pady=12)
        self.label = tk.Label(master)
        self.canvas = tk.Canvas(master, width=1000, height=600, bg='black')
        self.canvas.pack()
        self.f.pack_propagate(0)

    ## add input field and button functionality that when pushed will build text cloud
    def display_wordcloud(self, master):
        self.setup_window(master)
        label = tk.Label(master, text="Enter a Twitter Handle", font = LARGE_FONT)
        v = tk.StringVar()
        self.e = tk.Entry(self.f, textvariable=v)
        buttonA = tk.Button(self.f, text="Make a Cloud", activeforeground = 'blue', bd = 4 , font = LARGE_FONT, command=self.makeacloudbutton)
        self.e.pack()
        buttonA.pack()
        label.pack()
        self.f.pack()

    ## connect to the twitter api searching for given twitter handle and creates word corpus
    ## from twitter timeline
    def get_twitter_timeline(self):
            user_name = self.e.get()
            api = twitter.Api(consumer_key='ELcMTiBTTyQpHiiKUe46chiHo',
                            consumer_secret='nWB7WxUuKJRTy8QpejoH9bAnqcKOLTXOlxpZmZ8JykMlBaLMGD',
                            access_token_key='632857901-QiNnyoNzbwiOoAEVwP7NGuKCEeKtqBJm34aVusFO',
                            access_token_secret='5oGI6JVozWFrtMDEscrOs0SFg5B5Du2Ll7VT4VnhjkmQX')

            t = api.GetUserTimeline(screen_name= user_name, count=200)
            tweets = [i.AsDict() for i in t]
            tweet_text = []
            for t in tweets:
                tweet_text.append( t['text'])

            text = ' '.join(tweet_text).lower()
            #df = pd.DataFrame(tweet_text)

            return text

    ## what happens when the button is actually pushed:
    ## corpus (text) is turned into wordcloud and displayed in the
    ## canvas created in setup_window function
    def makeacloudbutton(self):

        text = self.get_twitter_timeline()
        stopwords = set(STOPWORDS)
        stopwords.add('https')

        wordcloud = WordCloud(width = 1000, height = 600, stopwords = stopwords).generate(text)
        image = wordcloud.to_image()
        img = ImageTk.PhotoImage(image)

        self.canvas.create_image (0,0, image = img, anchor = 'nw')
        self.canvas.image = img
        self.f.pack()


def main():
    root = tk.Tk()
    root.title('Make a Twitter WordCloud!')
    root.resizable(width=tk.NO, height=tk.NO)
    root.geometry("1080x800")
    app = twittercloudapp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
