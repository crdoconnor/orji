At nonexistent node:
  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        {{ root.at("nonexistent") }}
  steps:
  - orji:
      cmd: cat example.org example.jinja2
      error: yes
      output: |
        Failure on line 1 of example.jinja2: No notes found in ROOT with name nonexistent

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
      cmd: cat example.org example.jinja2
      error: yes
      output: |
        Template syntax error on line 5 of example.jinja2: expected token 'end of print statement', got 'be'


Template runtime error:
  given:
    files:
      example.org: |
        * existent
      example.jinja2: |
        Brackets 

        {% if 4 is divisiblebyy 3 %}
        {% endif %}

        Should be closed
  steps:
  - orji:
      cmd: cat example.org example.jinja2
      error: yes
      output: |
        Template runtime error on line 3 of example.jinja2: No test named 'divisiblebyy' found.


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
      cmd: cat example.org example.jinja2
      error: yes
      output: |
        Template error on line 3 of example.jinja2: 'doesntexistonline3' is undefined


