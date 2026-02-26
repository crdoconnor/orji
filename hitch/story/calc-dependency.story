Calculation with dependency:
  docs: calculation-with-dependency
  about: |
    Run a calculation from within a note.
  variations:
    First run:
      given:
        files:
          org/calc.org: |
            * Number of chairs in section b = ?
            =150+150
            * Number of chairs in section c = 400
            * Number of chairs total = ?
            =100+200+number_of_chairs_in_section_b+number_of_chairs_in_section_c
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
            * Number of chairs in section b = 300
            =150+150
            * Number of chairs in section c = 400
            * Number of chairs total = 1000.0
            =100+200+number_of_chairs_in_section_b+number_of_chairs_in_section_c
