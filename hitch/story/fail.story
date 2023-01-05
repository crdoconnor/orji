Deliberately fail:
  about: |
    When your template has an error condition that
    you need to raise, use fail("error message")
    to raise the error.

  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        This is some text

        {{ fail("this shouldn't happen") }}

        This is some more text.

  steps:
  - orji:
      cmd: example.org example.jinja2
      error: yes
      output: |
        Failure on line 3 of example.jinja2: this shouldn't happen


