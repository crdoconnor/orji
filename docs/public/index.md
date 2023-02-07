---
title: OrJi
---

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/crdoconnor/orji?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/orji">


OrJi is a command line tool to generate text files using [jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
and [orgmode](https://en.wikipedia.org/wiki/Org-mode) files. It can be used to generate LaTeX or HTML or any other kind
of text from an orgmode file.

## Why?

For me so I can write [letters](https://raw.githubusercontent.com/crdoconnor/orji/main/examples/letter.org) and stuff in [orgzly](https://orgzly.com/) or [plainorg](https://plainorg.com/) and run
a short script to create a nicely formatted PDF from an easily edited [template file](https://github.com/crdoconnor/orji/blob/main/examples/letter.jinja2).

You can do quite a lot more than that, though.

## Install

OrJi is a command line app that be installed with pip:

```bash
pipx install orji
```

Typically best installed by installing it through
[pipx](https://pypa.github.io/pipx/).

```bash
pipx install orji
```

## Example Usage

---
title: Quickstart
---
# Quickstart

Use all basic orji template features in one file.





simple.org
```
* TODO A todo note

About text

* DONE A done note with bullet points :tag1:

+ Bullet one
+ Bullet two

* A third note with checkboxes :tag2:tag3:

- [ ] Checkbox 1
- [X] Checkbox 2
- [ ] Checkbox 3

* Fourth note
:PROPERTIES:
:prop1: ABC
:prop2: CDE
:END:

Text

** Subnote B

*** Subnote C

Subnote C body.

```


simple.jinja2
```
{% for note in notes %}
-------------------------
Name: {{ note.name }}
Slug: {{ note.slug }}
State: {{ note.state }}
Tags: {% for tag in note.tags %}{{ tag }} {% endfor %}
ILookup : {{ note.indexlookup }}

Text:

{{ note.body }}
-------------------------
{% endfor %}

=========================
Lookup level A:

Text: {{ notes.at("Fourth note").body }}
Property 1: {{ notes.at("Fourth note").prop["prop1"] }}
ILookup : {{ notes.at("Fourth note").indexlookup }}
=========================
Lookup level C:

Text: {{ notes.at("Fourth note").at("Subnote B").at("Subnote C").body }}
ILookup : {{ notes.at("Fourth note").at("Subnote B").at("Subnote C").indexlookup }}
=========================

```




orji simple.org simple.jinja2


```

-------------------------
Name: A todo note
Slug: a-todo-note
State: TODO
Tags: 
ILookup : 0

Text:


About text

-------------------------

-------------------------
Name: A done note with bullet points
Slug: a-done-note-with-bullet-points
State: DONE
Tags: tag1 
ILookup : 1

Text:


+ Bullet one
+ Bullet two

-------------------------

-------------------------
Name: A third note with checkboxes
Slug: a-third-note-with-checkboxes
State: None
Tags: tag2 tag3 
ILookup : 2

Text:


- [ ] Checkbox 1
- [X] Checkbox 2
- [ ] Checkbox 3

-------------------------

-------------------------
Name: Fourth note
Slug: fourth-note
State: None
Tags: 
ILookup : 3

Text:


Text

-------------------------


=========================
Lookup level A:

Text: 
Text

Property 1: ABC
ILookup : 3
=========================
Lookup level C:

Text: 
Subnote C body.
ILookup : 3/0/0
=========================

```

