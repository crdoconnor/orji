Insert multiple snippets of text:
  docs: insert-multiple-things
  about: |
    Insert two snippets of text.
  given:
    files:
      org/notes.org: |
        * Ideas
      direct.jinja2: |
        * {{ new_idea }}
        ** Who had it?

        {{ who_had_it }}


  steps:
  - orji:
      env:
        ORJITMP: ./tmp
      cmd: in direct.jinja2 under org/notes.org//0 new_idea:snippet:"Tinder for cats"
        who_had_it:snippet:"Me"
      output: |
        Written note(s) successfully

  - file contents:
      filename: org/notes.org
      contents: |
        * Ideas
        ** Tinder for cats
        ** Who had it?
        Me
