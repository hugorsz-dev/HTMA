# Redirects of all file types

So far, only use cases where `.htma` and `.md` extensions were redirected have been exposed. When, for example, it is necessary to list alternative files, such as `.mp3` or `.pdf`, the `REDIR: extension` should be examined. 

Unlike `REDIR:MD` and `REDIR:HTMA`, it lacks _special variables_. Only _global variables_ may be used.

## Insert content in any format

In the `first_project`, inside the `content` folder, we will insert three images, `img1.gif`, `img2.png` and `img3.jpg`. The folder structure will be as follows:

```
myweb/
├── content/
│   ├── doc1.md
│   ├── doc2.md
│   ├── doc3.md
│   ├── htmadoc1.htma
│   ├── htmadoc2.htma
│   ├── htmadoc3.htma
│   ├── img1.gif
│   ├── img2.jpg
│   └── img3.png
└── index.htma
```

## Edit `index.htma`

And in the `index.htma` file, we will introduce a loop with a `REDIR` that collects the extensions of the previous files.

```
<HTMA!>
    DIR:: myweb/content;
    REDIR::: png, jpg, gif;
    TEMPLATE:: {
        <h2> $FILE_NAME_FOR_EACH_FILE_FILE_IN_DIR$ </h2>
        <img src="$LINK_FOR_EACH_FILE_IN_DIR$’>
        <p> <em> $CREATION_TIME_FOR_EACH_FILE_IN_DIR$ </em> </p> </p>
    };
</HTMA>
```

## Result

Executed the `htma.py` script, the result should look like this:

```
<h2> img2 </h2>
<img src="/home/user/first_project/target/content/img2.jpg">
<p> <em> 2024-10-12</em> </p> <p>
<h2> img1 </h2>
<img src="/home/user/first_project/target/content/img1.gif">
<p> <em> 2024-10-12</em> </p> <p>
<h2> img3 </h2>
<img src="/home/user/first_project/target/content/img3.png">
<p> <em>2024-10-12</em> </p> </p>
``` 
