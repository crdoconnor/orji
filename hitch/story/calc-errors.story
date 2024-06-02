Calculation errors:
  docs: calculation-errors
  about: |
    Run a calculation from within a note.
  variations:
    Error occurred calculation:
      given:
        files:
          org/calc.org: |
            * Destroy the universe = ?
            =1/0
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc org/calc.org//0
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Destroy the universe = ?
            =1/0
            ** ZeroDivisionError    :calcerror:
            division by zero

    Error removed from calculation:
      given:
        files:
          org/calc.org: |
            * Destroy the universe = ?
            =1+1
            ** ZeroDivisionError    :calcerror:
            division by zero
            ** Unrelated subnote
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc org/calc.org//0
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Destroy the universe = 2
            =1+1
            ** Unrelated subnote
