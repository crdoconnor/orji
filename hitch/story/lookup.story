Lookup:
  about: |
    Use index based lookups to grab specific notes.
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
        TITLE: {{ root.name }}

        {{ root.body}}
  steps:
  - orji:
      cmd: out simple.org//0 simple.jinja2
      output: |
        TITLE: A normal note

        Just a note
