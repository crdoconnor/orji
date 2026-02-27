Subcalculations:
  docs: basic-calculation
  about: |
    Run a series of calculations inside a note.
  variations:
    First run:
      given:
        files:
          org/calc.org: |
            * Number of chairs = ?
            =300+500+600
            * Subcalculation :subcalc:
            ** Number of tables = ?
            = number_of_chairs / 4
            ** Anticipated weight = ?
            = number_of_chairs * 20.0 + number_of_tables * 50.0
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
            * Subcalculation    :subcalc:
            ** Number of tables = 350.0
            = number_of_chairs / 4
            ** Anticipated weight = 45500.0
            = number_of_chairs * 20.0 + number_of_tables * 50.0
