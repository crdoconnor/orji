---
title: Run templated script to send email
---
# Run templated script to send email


With script mode, you can "orji run" with a directory of templated scripts
and a directory or org files.

It will look through all of them for a TODO note with a tag matching a templated script.

You can use this to trigger templated bash scripts which can execute
pre-defined tasks from notes.

This example runs a bash script to send an email.

If there are zero or two notes matching scripts then it will raise an error.





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
