Individual links from within notes:
  docs: walk
  about: |
    Example of grabbing a single:

    * Telephone number
    * SMS
    * Mailto
    * File
  given:
    files:
      links.org: |
        * Telephone number :tel:

        tel:+447777777771

        * SMS :sms:

        sms:+447777777771

        * Email :mailto:

        mailto:billg@microsoft.com

        * File :file:

        file:filename.png

      links.jinja2: |
        {% for note in root %}
        {{ note.name }}: 
        {%- if "tel" in note.tags %} {{ note.links.tel }}{%- endif -%}
        {%- if "sms" in note.tags %} {{ note.links.sms }}{%- endif -%}
        {%- if "file" in note.tags %} {{ note.links.file }}{%- endif -%}
        {%- if "mailto" in note.tags %} {{ note.links.mailto }}{%- endif -%}
        {% endfor %}


  steps:
  - orji:
      cmd: out links.org links.jinja2
      output: |2

        Telephone number: +447777777771
        SMS: +447777777771
        Email: billg@microsoft.com
        File: filename.png
