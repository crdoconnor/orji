# OrJi

OrJi is a command line tool to generate text files using [jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
and [orgmode](https://en.wikipedia.org/wiki/Org-mode) files. It can be used to generate LaTeX or HTML or any other kind
of text from an orgmode file.

## Why?

For me so I can write [letters](https://raw.githubusercontent.com/crdoconnor/orji/main/examples/letter.org) and stuff in [orgzly](https://orgzly.com/) or [plainorg](https://plainorg.com/) and run
a short script to create a nicely formatted PDF from an easily edited [template file](https://github.com/crdoconnor/orji/blob/main/examples/letter.jinja2).

```bash
cd orji/examples
orji --latexmode letter.org letter.jinja2 > output.tex
cd output/
pdflatex output.tex
```

You can do quite a lot more than that, though.

## Install

OrJi is typically best installed by installing [pipx](https://pypa.github.io/pipx/)
and then installing orji using pipx.

```bash
pipx install orji
```

## Example Usage

```bash
orji myorg.org myjinja.jinja2
```

With myorg.org:

```org
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
```

And myjinja2.jinja2:

```jinja2
{% for note in root %}
-------------------------
Name: {{ note.name }}
Slug: {{ note.slug }}
State: {{ note.state }}
Tags: {% for tag in note.tags %}{{ tag }} {% endfor %}

Text:

{{ note.body }}

Rich:

{% for line in note.body.lines %}
{{ line }}
{%- endfor %}
-------------------------
{% endfor %}

=========================
Lookup:

Text: {{ root.at("Fourth note").body }}
Property 1: {{ root.at("Fourth note").prop["prop1"] }}
```

output:

```text
-------------------------
Name: A todo note
Slug: a-todo-note
State: TODO
Tags: 

Text:


About text


Rich:



About text

-------------------------

-------------------------
Name: A done note with bullet points
Slug: a-done-note-with-bullet-points
State: DONE
Tags: tag1 

Text:


+ Bullet one
+ Bullet two


Rich:



+ Bullet one
+ Bullet two

-------------------------

-------------------------
Name: A third note with checkboxes
Slug: a-third-note-with-checkboxes
State: None
Tags: tag2 tag3 

Text:


- [ ] Checkbox 1
- [X] Checkbox 2
- [ ] Checkbox 3


Rich:



- [ ] Checkbox 1
- [X] Checkbox 2
- [ ] Checkbox 3

-------------------------

-------------------------
Name: Fourth note
Slug: fourth-note
State: None
Tags: 

Text:


Text

Rich:



Text
-------------------------


=========================
Lookup:

Text: 
Text
Property 1: ABC
```
