Insert file:
  docs: insert
  about: |
    Insert a text file as a note.
  given:
    files:
      org/simple.org: |
        * Top note
        ** Subnote
        ** TODO Insert above, under or below, replace this  
        * DONE Done item
      speech.txt: This is a note generated by speech to text.
      notetemplate.jinja2: |
        * TODO File this note

        {{ words }}

        * Speech to text note

        {{ words }}

  variations:
    Above:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 above org/simple.org//0/1 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            ** TODO Insert above, under or below, replace this
            * DONE Done item

      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 above org/simple.org//0 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * TODO File this note
            This is a note generated by speech to text.
            * Speech to text note
            This is a note generated by speech to text.
            * Top note
            ** Subnote
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            ** TODO Insert above, under or below, replace this
            * DONE Done item

    Below:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 below org/simple.org//0/1 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO Insert above, under or below, replace this
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            * DONE Done item

      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 below org/simple.org//0 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            * TODO File this note
            This is a note generated by speech to text.
            * Speech to text note
            This is a note generated by speech to text.
            ** Subnote
            ** TODO Insert above, under or below, replace this
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            * DONE Done item


    Under:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 under org/simple.org//0/1 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO Insert above, under or below, replace this
            *** TODO File this note
            This is a note generated by speech to text.
            *** Speech to text note
            This is a note generated by speech to text.
            * DONE Done item

      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 under org/simple.org//0 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO Insert above, under or below, replace this
            *** TODO File this note
            This is a note generated by speech to text.
            *** Speech to text note
            This is a note generated by speech to text.
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            * DONE Done item


    Replace:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in notetemplate.jinja2 replace org/simple.org//0/1 words:text:speech.txt
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            ** Subnote
            ** TODO File this note
            This is a note generated by speech to text.
            ** Speech to text note
            This is a note generated by speech to text.
            * DONE Done item
