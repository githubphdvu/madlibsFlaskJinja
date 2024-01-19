from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

class Story:
    """To make a story,pass list of prompts['place',...],text of template 'Once upon...'
        >>> s = Story(["noun", "verb"],
        ...     "I love to {verb} {noun}")
    To generate text from a story, pass in a dictionary-like object of {prompt: answer, promp:answer):
        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat mango'
    """
    def __init__(self, words, text):
        self.prompts = words
        self.template = text
    def generate(self, D):#dict-like object
        text = self.template
        for (k, v) in D.items():
            text = text.replace('{'+k+'}',v)
        return text
story=Story(["place","noun","verb","adjective","plural_noun"],'Once upon a time in a long-ago {place},there lived a {adjective} {noun}.It loved to {verb} {plural_noun}')

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

@app.route("/")
def ask_questions():
    prompts = story.prompts
    return render_template("questions.html",P=prompts)

@app.route("/story")
def generate_story():
    text = story.generate(request.args)
    return render_template("story.html",T=text)

if __name__ == '__main__': app.run(debug=True)
