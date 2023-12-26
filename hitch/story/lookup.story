Lookup from CLI:
  about: |
    Orji uses lookups to reference or grab specific notes.

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
        TITLE: {{ root.name }}

        {{ root.body }}
  variations:
    First note:
      steps:
      - orji:
          cmd: out simple.org//0 simple.jinja2
          output: |
            TITLE: A normal note

            Just a note

    Sub note by index:
      steps:
      - orji:
          cmd: out simple.org//0/0 simple.jinja2
          output: |
            TITLE: Subnote of first note

            A subnote of the top note.

    Sub note by name:
      steps:
      - orji:
          cmd: out "simple.org//0/Subnote of first note" simple.jinja2
          output: |
            TITLE: Subnote of first note

            A subnote of the top note.

    Sub note look up note with title zero:
      steps:
      - orji:
          cmd: out "simple.org//0/'0'" simple.jinja2
          output: |
            TITLE: 0

            A subnote with the title zero
