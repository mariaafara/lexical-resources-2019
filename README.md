
# Lexical-Resources-2019 code repository

This repository contains the canvas for the practical sessions of the "Lexical Ressources" class of the NLP Masters of Science @ Université de Lorraine.
For questions pertaining to the lecture, you can contact either [Christophe Cerisara](mailto:christophe.cerisara@loria.fr "christophe.cerisara@loria.fr") or [Timothee Mickus](mailto:tmickus@loria.fr "tmickus@loria.fr"). Code was developped by Timothee Mickus.

## Installation
Create a virtual environment & download the necessary libraries
```sh
python3 -m venv .lexres
source .lexres/bin/activate
pip3 install -r requirements.txt
```
Go to the main directory of the website and start the app using the Django script:
```sh
cd lexres-site
python3 manage.py runserver
```
Once the server is started, go to the URL where the project is running, which should be http://127.0.0.1:8000/editor/ (any URL starting with http://127.0.0.1:8000/ should redirect you to the correct page). From this editor, you can test what you'll be coding.

## Working with the repository
The repository contains two (almost empty) python script files: `lexres/editor/nlp/services/edits.py` and `lexres-site/editor/nlp/services/preds.py`. All code done during practical sessions can be added to these two files, and will be detected automatically by the web application.

Functions listed in `lexres-site/editor/nlp/services/preds.py` are intended to predict the next word, given what was already written by the user. Functions listed in `lexres-site/editor/nlp/services/edits.py` are meant to propose edits & changes to the text, eg. by highlighting spelling mistakes.

**These files should contain functions which must have a specific signature.** For now, these files contain one example each.
Namely, all functions in `lexres-site/editor/nlp/services/preds.py` should have a keyword argument "text", and should yield a list of strings. Here's an example:
```python
def pred_foo_function(text=""):
    return ["a", "list", "of", "possible", "next", "words"]
```
Likewise, all functions in `lexres-site/editor/nlp/services/edits.py` should have a keyword argument "text", and should yield a list of `SpanEdit` objects. Here's an example:
```python
def edit_bar_function(text=""):
    return [
        SpanEdit(
            beg_idx=10,
            end_idx=42,
            edit="You should replace `text[10:42]` with this string."),
    ]
```
FYI, the SpanEdit constructor is defined in `lexres-site/editor/utils/nlp.py`.

## How does the code work?
*Reading this section is not required, but it's recommended (it's always good to know more when programming).*

The code is more or less a basic [Django](https://www.djangoproject.com/ "Django Homepage") project. It defines a site called "`lexres`", which contains a single app called "`editor`". The porject closely follows the general documentation of Django, and you are invited to read the tutorials for a more thorough understanding of how Django works.
Here is a list of the specific settings and hacks:
+ databases engines have been removed, as we won't be using them.
+ static files are handled via template inclusion (static files are in `lexres-site/editor/templates/editor/definitely_not_static/`), rather than collect & serve
+ jQuery has been added for AJAX functionalities, cf. `lexres-site/editor/templates/editor/ajax_funcs.html`; adapted from [this tutorial blogpost](https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html).
+ except for the default view in the `editor` app (cf. `lexres-site/editor/views.py:editor()`), all other views are endpoints for ajax services.
+ the AJAX endpoints use introspection to call each function in a specific `nlp/service` module, and create a dictionary mapping function names to lists of suggested outputs.
