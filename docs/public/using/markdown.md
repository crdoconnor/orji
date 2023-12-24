---
title: Convert chunks of orgmode text into markdown
---
# Convert chunks of orgmode text into markdown


Convert chunks of orgmode text into markdown using .body.markdown.





markdown.org
```markdown.org
* Note title

Text with /emphasis/ and *bold* and a [[https://www.google][link]].

+ Bullet one
+ Bullet two

```


markdown.jinja2
```markdown.jinja2
{{ root.at("Note title").body.markdown }}

```




Running:
```bash
orji out markdown.org markdown.jinja2
```

Will output:
```
Text with /emphasis/ and *bold* and a [link](https://www.google).

* Bullet one
* Bullet two

```
