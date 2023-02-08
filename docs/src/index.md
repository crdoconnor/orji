{{{{ intro.txt }}}}

OrJi is a command line tool to generate text files using [jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
and [orgmode](https://en.wikipedia.org/wiki/Org-mode) files. It can be used to generate LaTeX, Markdown or HTML or any other kind of text from an orgmode file.

It is somewhat inspired by [j2cli](https://github.com/kolypto/j2cli).

## Quickstart

{{{{ quickstart.txt }}}}

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

{{{{ using-contents.txt }}}}
