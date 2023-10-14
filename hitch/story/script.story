Run templated script to send email:
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      org/simple.org: |
        * TODO An email I want to send :email:

        ** email

        billg@microsoft.com

        ** body

        Windows sucks.

        * TODO Wash car :morning:

        Car wash.

        * TODO File taxes :evening:

        File taxes for wife too.

        * DONE Watch TV
      org/simple2.org: |
        * Another note

        * Another irrelevant note.
      orun/email.sh: |
        echo {{ note.at("body").body.oneline }}
        cat {{ note.at("email").body.tempfile() }}
  steps:
  - orji:
      cmd: run org orun
      output: |
        Windows sucks.

        billg@microsoft.com
