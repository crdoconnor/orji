# OrJi

## Install

OrJi is typically best installed by installing [pipx](https://pypa.github.io/pipx/)
through your system package manager and then installing orji using pipx.

```bash
pipx install orji
```

## QuickStart

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
{% for note in notes %}
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

Text: {{ notes.at("Fourth note").body }}
Property 1: {{ notes.at("Fourth note").prop["prop1"] }}
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
