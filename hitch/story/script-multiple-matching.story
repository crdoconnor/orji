Templated with more than one note:
  docs: orji-run-multiple
  about: |
    With script mode, you can "orji run" with a directory of templated scripts
    and a directory or org files.
    
    It will look through all of them for a TODO note with a tag matching a templated script.
    
    You can use this to trigger templated bash scripts which can execute
    pre-defined tasks from notes.
    
    This example runs a bash script to send an email.
    
    With --multiple then multiple matching scripts will be run.
  given:
    files:
      org/simple.org: |
        * TODO Wash car :email-reminder:

        Car wash.

        * DONE Watch TV
      org/simple2.org: |
        * Another note

        * TODO File taxes :email-reminder:

        File taxes for wife too.

        * Another irrelevant note.
      orun/email-reminder.sh: |
        echo {{ note.body.oneline }}
  variations:
    Run --multiple:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: run --multiple org orun
          error: yes
          output: |
            Car wash.
            File taxes for wife too.

    Fails if multiple matching scripts:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: run org orun
          error: yes
          output: |
            Multiple matching notes use --multiple to run all of them

            /gen/working/org/simple.org: 0: Wash car
            /gen/working/org/simple2.org: 1: File taxes
