Lookup in file:
  about: |
    Orji uses lookups to reference or grab specific notes using
    .at("") to grab a note or .has("") to check it is there.

    The lookup can be based upon index (if it is a number) or
    note name.
  given:
    files:
      simple.org: |
        * A normal note

        Just a note

        ** Subnote of first note

        A subnote of the top note.

        ** 0

        A subnote with the title zero

        * TODO Wash car :morning:

        Car wash.

        * TODO File taxes :evening:

        File taxes for wife too.

        * DONE Watch TV
      simple.jinja2: |
        TITLE: {{ note.name }}

        Different ways of grabbing first note:

        * {{ note.at("A normal note").name }}
  steps:
  - orji:
      cmd: out simple.org simple.jinja2
      output: |
        TITLE: ROOT

        Different ways of grabbing first note:

        * A normal note
