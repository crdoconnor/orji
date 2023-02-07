{{{{ intro.txt }}}}

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

{{{{ quickstart.txt }}}}
