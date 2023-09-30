Quickstart:
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      simple.org: |
        * A normal note

        Just a note

        * TODO Wash car :morning:

        Car wash.

        * TODO File taxes :evening:

        File taxes for wife too.

        * DONE Watch TV
      simple.jinja2: |
        {% for note in root %}
        {%- if note.state == "TODO" -%}
        # {{ note.name }} ({% for tag in note.tags %}{{ tag }}{% endfor %})

        {{ note.body }}
        {% endif %}
        {% endfor %}
  steps:
  - orji:
      cmd: cat simple.org simple.jinja2
      output: |2+

        # Wash car (morning)

        Car wash.

        # File taxes (evening)

        File taxes for wife too.



...
