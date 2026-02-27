Basic calculation:
  docs: basic-calculation
  about: |
    Run calculations from within a note and see the results appear within the note.
  variations:
    First run:
      given:
        files:
          org/calc.org: |
            * Number of chairs = ?
            =300+500+600
            * Weight = ?
            =34.5+34.2
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc org/calc.org
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Number of chairs = 1400
            =300+500+600
            * Weight = 68.7
            =34.5+34.2

    Second run:
      given:
        files:
          org/calc.org: |
            * Number of chairs = 1500
            =300+500+600
            * Weight = 68.7
            =34.5+34.2
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc org/calc.org
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Number of chairs = 1400
            =300+500+600
            * Weight = 68.7
            =34.5+34.2

    Skip archived and DONE notes:
      given:
        files:
          org/calc.org: |
            * Number of chairs = ?
            =300+500+600
            * Weight = ?
            =34.5+34.2
            * DONE calc = 3
            =1+1

      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc org/calc.org
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Number of chairs = 1400
            =300+500+600
            * Weight = 68.7
            =34.5+34.2
            * DONE calc = 3
            =1+1
