#Calculation with dependency:
  #docs: basic-calculation
  #about: |
    #Run a calculation from within a note.
  #variations:
    #First run:
      #given:
        #files:
          #org/calc.org: |
            #* Number of chairs = ?
            #=100+200+number_of_chairs_in_section_b+number_of_chairs_in_section_c
            #** Number of chairs in section b = ?
            #150+150
            #** Number of chairs in section c = 400
      #steps:
      #- orji:
          #env:
            #ORJITMP: ./tmp
          #cmd: calc org/calc.org//0
          #output: |
            #Written note(s) successfully

      #- file contents:
          #filename: org/calc.org
          #contents: |
            #* Number of chairs = ?
            #=100+200+number_of_chairs_in_section_b+number_of_chairs_in_section_c
            #** Number of chairs in section b = ?
            #150+150
            #** Number of chairs in section c = 400
