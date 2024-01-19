from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
# from stories import stories

class Story:
    """To  make story,pass a code,a title,a list of prompts,and text of template
        >>> s = Story(
        ...     "simple",
        ...     "A Simple Tale",
        ...     ["noun", "verb"],
        ...     "I love to {verb} a good {noun}")
    To generate text from a story, pass in a dictionary-like object of {prompt: answer, promp:answer):
        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat a good mango'
    """

    def __init__(self, code, title, words, text):
        self.code = code
        self.title = title
        self.prompts = words
        self.template = text
    def generate(self, answers):
        """Substitute answers into text"""
        text = self.template
        for (key, val) in answers.items():
            text = text.replace("{" + key + "}", val)
        return text
story1 = Story("history","A History Tale",["place", "noun","verb","adjective","plural_noun"],'Once upon a time in a long-ago {place},there lived a large {adjective} {noun}.It loved to {verb} {plural_noun}')
story2 = Story("omg","An Excited Adventure",["noun", "verb"],'OMG!! OMG!! I love to {verb} a {noun}')

stories = {s.code: s for s in [story1, story2]}# Make dict of {code:story, code:story,...}

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route("/")
def ask_story():
    return render_template("select-story.html",stories=stories.values())
@app.route("/questions")
def ask_questions():
    story_id = request.args["story_id"]
    story = stories[story_id]
    prompts = story.prompts
    return render_template("questions.html",story_id=story_id,title=story.title,P=prompts)
@app.route("/story")
def generate_story():
    story_id = request.args["story_id"]
    story = stories[story_id]
    text = story.generate(request.args)
    return render_template("story.html",title=story.title,T=text)
