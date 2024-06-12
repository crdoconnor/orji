Use a python module:
  docs: module
  about: |
    This is useful if you want to use custom python logic to
    generate your output or inside your calculations.

    Don't be tempted to make it too complicated though.
  variations:
    With template variables and methods:
      given:
        files:
          note.org: |
            * Note 1

            * Note 2

          note.jinja2: |
            {% for note in root %}
            {{ to_upper(note.name) }}
            {% endfor %}
          note.py: |
            def to_upper(string):
                return string.upper()
      steps:
      - orji:
          cmd: out --module note.py note.org note.jinja2
          output: |2+

            NOTE 1

            NOTE 2

    With calculations:
      given:
        files:
          calc.org: |
            * Five squared = ?
            =squared(5)
          calc.py: |
            def squared(number):
                return number * number
      steps:
      - orji:
          cmd: calc --module calc.py calc.org
          output: |
            Written note(s) successfully

      - file contents:
          filename: calc.org
          contents: |
            * Five squared = 25
            =squared(5)
