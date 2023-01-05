At nonexistent node:
  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        {{ root.at("nonexistent") }}
  steps:
  - orji:
      cmd: example.org example.jinja2
      error: yes
      output: |
        Failure on line 1 of example.jinja2: No notes found in  with name nonexistent

Template syntax error:
  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        Brackets 

        {{

        Should be closed
  steps:
  - orji:
      cmd: example.org example.jinja2
      error: yes
      output: |
        Template syntax error on line 5 of example.jinja2: expected token 'end of print statement', got 'be'

Missing variable:
  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        This is some text

        {{ doesntexistonline3 }}

        This is some more text.
  steps:
  - orji:
      cmd: example.org example.jinja2
      error: yes
      output: |
        Template error on line 3 of example.jinja2: 'doesntexistonline3' is undefined


