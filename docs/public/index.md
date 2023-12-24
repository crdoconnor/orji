---
title: OrJi
---



<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/crdoconnor/orji?style=social"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/orji">

OrJi is a command line tool to generate text files using [jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
and [orgmode](https://en.wikipedia.org/wiki/Org-mode) files. It can be used to generate LaTeX, Markdown or HTML or any other kind of text from an orgmode file.

It is somewhat inspired by [j2cli](https://github.com/kolypto/j2cli).

## Quickstart



Simple org mode file used with simple template.





simple.org
```
* A normal note

Just a note

* TODO Wash car :morning:

Car wash.

* TODO File taxes :evening:

File taxes for wife too.

* DONE Watch TV

```


simple.jinja2
```
{% for note in root %}
{%- if note.state == "TODO" -%}
# {{ note.name }} ({% for tag in note.tags %}{{ tag }}{% endfor %})

{{ note.body }}
{% endif %}
{% endfor %}

```




Running:
```bash
orji out simple.org simple.jinja2
```

Will output:
```

# Wash car (morning)

Car wash.

# File taxes (evening)

File taxes for wife too.




```


## Why?

The practical itch I was scratching was editing and writing small blocks of content in [orgzly](https://orgzly.com/) on my phone and being able to kick off a small script that either turned it into a nice letter PDF or CV pdf or updated the markdown on my website.

It also lets me maintain [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) on personal documents by keeping content in org files and style in jinja2 templates.

## Install

OrJi can be installed with pip:

```bash
pip install orji
```

As a command line app, it is typically best installed via
[pipx](https://pypa.github.io/pipx/).

```bash
pipx install orji
```

### Using OrJi

- [Demonstration of all template features](using/all-template-features)
- [Deliberately trigger a template failure](using/deliberate-failure)
- [Insert file into org mode file](using/insert)
- [Example of Generated LaTeX A4 CV](using/latex-cv)
- [Example of Generated LaTeX A4 Letter](using/latex-letter)
- [Convert chunks of orgmode text into markdown](using/markdown)
- [Use a python module with template variables and methods](using/module)
- [Templated with more than one note](using/orji-run-multiple)
- [Run templated script to send email](using/orji-run)

