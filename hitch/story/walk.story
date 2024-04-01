Walk through org notes recursively:
  docs: walk
  about: |
    Example demonstrating walking through org mode notes
    to pull out specific notes with the label "contact" in
    order to generate a vcf file with telephone numbers of
    all notes in the file.
  given:
    files:
      contacts.org: |
        * Note 1

        * Note 2

        * James :contact:

        tel:+447777777771

        * Work

        ** Thomas :contact:

        tel:+447777777772

        ** Fred :contact:

        tel:+447777777773

      vcf.jinja2: |
        {%- for note in root.walk() -%}
        {%- if "contact" in note.tags -%}
        BEGIN:VCARD
        VERSION:4.0
        FN:{{ note.name }}
        N:{{ note.name }};;;;
        TEL:{{ note.links.tel }}
        END:VCARD
        {% endif -%}
        {% endfor -%}


  steps:
  - orji:
      cmd: out contacts.org vcf.jinja2
      output: |+
        BEGIN:VCARD
        VERSION:4.0
        FN:James
        N:James;;;;
        TEL:+447777777771
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:Thomas
        N:Thomas;;;;
        TEL:+447777777772
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:Fred
        N:Fred;;;;
        TEL:+447777777773
        END:VCARD

...
