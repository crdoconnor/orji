# OrJi

## Install

OrJi is typically best installed by installing [pipx](https://pypa.github.io/pipx/)
through your system package manager and then installing orji using pipx.

```bash
pipx install orji
```

## QuickStart

orji myorg.org myjinja.jinja2

myorg.org:

```org
* Note 1

About text

* Note 2

About text

* Note 3

About text
```

myjinja2.jinja2:

```jinja2
{% for note in notes %}
{{ note.heading }}
{% endfor %}
```

output:

```
Note 1

Note 2

Note 3
```
