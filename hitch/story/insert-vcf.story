Insert vcf file:
  docs: insert-vcf
  about: |
    Insert ical file as a note.
  given:
    files:
      org/contacts.org: |
        * From phone
      direct.jinja2: |
        {{ contact.to_org() }}
      fromphone.ical: |
        BEGIN:VCARD
        VERSION:4.0
        FN:John
        N:John;;;;
        TEL:+447777777774
        END:VCARD

  variations:
    Insert contacts in header:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in direct.jinja2 under org/contacts.org//0 contact:vcf:fromphone.ical
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/contacts.org
          contents: |
            * From phone
            ** John
            tel:+447777777774
