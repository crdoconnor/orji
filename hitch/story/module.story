Use a python module with template variables and methods:
  docs: module
  about: |
    This is useful if you want to use custom python logic to
    generate your output.
    
    Don't be tempted to make it too complicated though.
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
      cmd: cat --module note.py note.org note.jinja2
      output: |2+

        NOTE 1

        NOTE 2
        
