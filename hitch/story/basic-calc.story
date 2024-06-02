Basic calculation:
  docs: basic-calculation
  about: |
    Run a calculation from within a note.
  variations:
    First run:
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

    Second run:
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
