---
title: OrJi
---

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/crdoconnor/orji?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/orji">


OrJi is a command line tool to generate text files using [jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
and [orgmode](https://en.wikipedia.org/wiki/Org-mode) files. It can be used to generate LaTeX or HTML or any other kind of text from an orgmode file.

## Why?

For me so I can write letters and documents in [orgzly](https://orgzly.com/) or [plainorg](https://plainorg.com/) and run
a short script to create a nicely formatted PDF from a separate template file.
You can do quite a lot more than that, though.

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

- [All template features](using/all-template-features)
- [Deliberately fail](using/deliberate-failure)
- [LaTeX Curriculum Vitae](using/latex-cv)
- [LaTeX Letter](using/latex-letter)
- [Markdown](using/markdown)
- [Module](using/module)


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
{%- endif -%}
{% endfor %}

```




Running:
```
orji simple.org simple.jinja2
```

Will output:
```
# Wash car (morning)


Car wash.
# File taxes (evening)


File taxes for wife too.


```

