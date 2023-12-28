Insert file:
  docs: insert
  about: |
    Insert a file as a note.
  given:
    files:
      org/simple.org: |
        * Top note

        ** Subnote

        ** TODO Insert above, under or below, replace this  

        * DONE Done item
      speech.txt: This is a note generated by speech to text.
      notetemplate.jinja2: |
        * TODO New note

        {{ text }}

  variations:
    Above:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 above org/simple.org//0/1 --text speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO Insert above, under or below, replace this
            * TODO New note
            This is a note generated by speech to text.
            * DONE Done item

    Below:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 below org/simple.org//0/1 --text speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO Insert above, under or below, replace this
            * TODO New note
            This is a note generated by speech to text.
            * DONE Done item

