Calculation:
  docs: calculation
  about: |
    Run a calculation from within a note.
  variations:
    Basic addition:
      given:
        files:
          org/calc.org: |
            * Number of chairs = ?
            =300+500+600
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
            * Number of chairs = 1400
            =300+500+600

    Rerun basic addition:
      given:
        files:
          org/calc.org: |
            * Number of chairs = 1500
            =300+500+600
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
            * Number of chairs = 1400
            =300+500+600

    Error in calculation:
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
