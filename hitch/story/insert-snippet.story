Insert snippet of text:
  docs: insert-snippet
  about: |
    Insert snippet of text on the command line.
  given:
    files:
      org/notes.org: |
        * Ideas
      direct.jinja2: |
        * New idea

        {{ new_idea }}


  steps:
  - orji:
      env:
        ORJITMP: ./tmp
      cmd: in direct.jinja2 under org/notes.org//0 new_idea:snippet:"Tinder for cats"
      output: |
        Written note(s) successfully

  - file contents:
      filename: org/notes.org
      contents: |
        * Ideas
        ** New idea
        Tinder for cats
