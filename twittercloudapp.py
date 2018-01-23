##This is an app that gets a twitter username from user input,
#and pulls that twitter timeline from the twitter api, and then
#builds a wordcloud from the relative word frequencies.
######################################################
# In order to run:
# -- must have python installed
# -- pip install python-twitter
# -- pip install WordCloud
# run in terminal using python twittercloudapp.py
#######################################################


import Tkinter as tk
from Tkinter import *
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
        self.e1 = tk.Entry(self.f, textvariable=v)

        #input additional stopwords
        label2 = tk.Label(self.f, text="Enter additional stopwords (separated by commas)", font = LARGE_FONT)
        v2 = tk.StringVar()
        self.e2 = tk.Entry(self.f, textvariable=v2)

        #make a colorscheme choice from dropdown menu
        self.colorvar = StringVar()
        self.colorvar.set('rainbow')
        popupMenu = OptionMenu(self.f, self.colorvar, "rainbow", "Blues", "Greens", "Reds", 'coolwarm')
        label3 = tk.Label(self.f, text="Choose a Colorscheme") #.grid(row = 1, column = 1)

        buttonA = tk.Button(self.f, text="Make a Cloud", activeforeground = 'blue', bd = 4 , font = LARGE_FONT, command=self.makeacloudbutton)

        label.pack()
        self.e1.pack()
        label2.pack()
        self.e2.pack()
        label3.pack()
        popupMenu.pack()
        buttonA.pack()
        self.f.pack()

    ## connect to the twitter api searching for given twitter handle and creates word corpus
    ## from twitter timeline
    def get_twitter_timeline(self):
            user_name = self.e1.get()
            api = twitter.Api(consumer_key='',
                            consumer_secret='',
                            access_token_key='',
                            access_token_secret='')

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
        color_choice = self.colorvar.get()

        #set stopwords, including those given through user input
        stopwords = set(STOPWORDS)
        addl_stopwords = self.addl_stopwords()

        if addl_stopwords is not None:
            [stopwords.add(word) for word in addl_stopwords]

        #build wordcloud
        wordcloud = WordCloud(width = 1000, height = 600, colormap = color_choice, stopwords = stopwords).generate(text)
        image = wordcloud.to_image()
        img = ImageTk.PhotoImage(image)

        self.canvas.create_image (0,0, image = img, anchor = 'nw')
        self.canvas.image = img
        self.f.pack()

    def addl_stopwords(self):
        addl_stopwords = self.e2.get()
        addl_words = addl_stopwords.split(',')
        return addl_words


def main():
    root = tk.Tk()
    root.title('Make a Twitter WordCloud!')
    root.resizable(width=tk.NO, height=tk.NO)
    root.geometry("1080x800")
    app = twittercloudapp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
