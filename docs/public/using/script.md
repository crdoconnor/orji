---
title: Run templated script to send email
---
# Run templated script to send email


Simple org mode file used with simple template.





org/simple.org
```org/simple.org
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

```


org/simple2.org
```org/simple2.org
* Another note

* Another irrelevant note.

```


orun/email.sh
```orun/email.sh
echo {{ note.at("body").body.oneline }}
cat {{ note.at("email").body.tempfile() }}

echo
echo {{ orgfile }}
echo {{ tmp }}
echo {{ out }}

```


tmp/_
```tmp/_

```




Running:
```bash
orji run org orun
```

Will output:
```
Windows sucks.
billg@microsoft.com
/gen/working/org/simple.org
/gen/working/tmp/11111.tmp
/gen/working

```
