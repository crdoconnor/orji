Delete:
  docs: rm
  about: |
    Delete 
  given:
    files:
      org/simple.org: |
        * Top note
        ** Subnote 1
        ** Subnote 2
        * DONE Done item     
  variations:
    Single note:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: rm org/simple.org//0
          output: |
            Deleted note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * DONE Done item

    Children:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: rm org/simple.org//0 --children
          output: |
            Deleted note(s) successfully

      - file contents:
          filename: org/simple.org
          contents: |
            * Top note
            * DONE Done item
