# First HTMA project

## Directory structure

Create a project folder (`first_project`), locate inside it and create a new folder (`myweb`). 

``` 
mkdir first_project
cd first_project
mkdir myweb
```

Next, copy the `htma.py` script into the root of the project. 

As a result, the directory tree should look like the following:

```
first_project
├── myweb/
└─── htma.py
```

> You need to keep the `htma.py` script out of the folders you are going to browse. 

## Edit input and target variables

Open `htma.py` and modify the following two variables:

- `input_path`: Path of the folder where the content of your project is located (`first_project/myweb`)
- `target_path`: Path of the folder where the `target` directory containing the generated project in HTML format will be generated (e.g. `first_project`).

It is recommended that you enter absolute paths in both variables. If you enter relative paths, they should point to the location of `htma.py`.

The variables should be: 

```
input_path = `/home/user/first_project/myweb`.
target_path = `/home/user/first_project/`
```

> Don't use the same path for `input_path` and `target_path`. 

## Create content in markdown

In `myweb`, create a `content` folder (any other name will do) and save some markdown documents in it, into which you will enter some sample text. 

For example, `doc1.md`, `doc2.md` and `doc3.md`:

````
# Page Title

This is how you write *italic text*.
This is how you write **bold text**.
This is how you write [a link](https://google.com).
This is how you write `code`.

```
This is a block of code
```

> This is a quote

- This is a list.
- This is a list.

1. This is a numbered list.
2. This is a numbered list.
````

## Create an index.htma file

In the root of your project, create an `index.htma` file, in which you will enter the following:

``` html
<html>
    <header>
        <title> My first page with HTMA </title>
    </header>

    <body>

        <p> This are the markdown documents in the <code> content </code> directory: </p> 

        <HTMA!>
            DIR:: content;
            REDIR::: MD;
            TEMPLATE:: {
                <li> <a href=`$LINK_FOR_FOR_EACH_FILE_IN_DIR$`> $MD_H1[0]$</a> 
            };
            MD_TEMPLATE {
                <html>
                    <header>
                        <title> $MD_H1[0]$ </title>
                    </header>
                    
                    <body>
                        $MARKDOWN_TO_HTML$
                    </body>
                </html>
            }
        </HTMA>

    </body> 

</html>
```

And run it from the root directory, using `python htma.py`.

The result will look something like the following:

```
├── myweb/
│   ├── content/
│   │   ├── doc1.md
│   │   ├── doc2.md
│   │   └── doc3.md
│   └── index.htma
├── target/
│   ├── content/
│   │   ├── doc1.html
│   │   ├── doc2.html
│   │   └── doc3.html
│   └── index.html
└── htma.py*
``` 


## Explanation of the file index.htma

From this basic exercise, it is understandable how the `<HTMA!>` tags work. Thanks to these, it will be possible to reference a directory (`DIR`) and insert its content into the web using templates (`TEMPLATE`, `MD_TEMPLATE`), which will use variables (`$VARIABLE$`) to link the content between both documents.

- **`DIR`**: This is the directory where the redirected files (in this case, the markdowns) are located.
-  REDIR`**: The extension of the file to be processed (since these are markdown files, their `REDIR` will be `MD`).
-  TEMPLATE`**: This is the format to be substituted in the generated `index.html` document. 
    - **`LINK_FOR_EACH_FILE_IN_DIR`**: This is the file path for each of the markdowns. 
    - **`MD_H1[0]`**: This is the array of first-level headers collected in the markdown, where the first element of the markdown `[0]` is specified.
- **`MD_TEMPLATE`**: The format in which the conversion from `.md` to `.html` will be generated.
    **`MARKDOWN_TO_HTML`**: The markdown file will be replaced by this tag, converted to HTML.

## Result

Executed the `htma.py` script, the result should look like this:

``` html

<html>
<header>
  <title> Page Title </title>
</header>

<body>
  <h1>Page Title</h1>.

  <p>This is how you write <em>italic text</em>.
    This is how you write <strong>bold text</strong>.
    This is how you write <a href=`https://google.com`>a link</a>.
    This is how you write <code>code</code>.

  <pre><code>This is a block of code
</code></pre>

  <blockquote>
    <p>This is a quote</p>
  </blockquote>

  <ul>
    <li>This is a list.
    <li>This is a list.
  </ul>

  <ol>
    <li>This is a numbered list.
    <li>This is a numbered list.
  </ol>
</body>

</html>

```


