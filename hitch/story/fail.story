Deliberately trigger a template failure:
  docs: deliberate-failure
  about: |
    When your template has an error condition caused by 
    something in the content, you can use fail("error message")
    to raise the error with a relevant message.
    
    This lets you create templates which [fail fast](https://en.wikipedia.org/wiki/Fail-fast).

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
      cmd: cat example.org example.jinja2
      error: yes
      output: |
        Failure on line 3 of example.jinja2: this shouldn't happen


