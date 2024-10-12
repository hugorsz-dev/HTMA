# Redirects between templates

Up to this point, the documentation has only addressed the use of `REDIR: MD`. However, we cannot make a complex web page using a single node between HTMA and markdown files: if you need to have more than one page, you will need to have the tools to interconnect several HTMA documents with each other. 

**`REDIR:HTMA`** allows iteration as in the previous examples, but over HTMA files instead of markdown. 

## Create HTMA content

In the `first_project` project, inside the `content` folder, we will create three documents, `htmadoc1.htma`, `htmadoc2.htma` and `htmadoc3.htma`. The folder structure will be as follows:

```
└── myweb/
    ├── content/
    │ ├─── doc1.md
    │ ├─── doc2.md
    │ ├─── doc3.md
    │ ├─── htmadoc1.htma
    │ ├─── htmadoc2.htma
    │ └─── htmadoc3.htma
    └── index.htma
```

Within the `htma` files, we can insert some simple HTML document. And although iterations could be used, in this case the example will not contain them in order to make the example easier to understand.

``` html
<html>
   <head>
      <title> 
         First sample HTMA document
      </title>
   </head>
   <body>
      <header>
         <h2 id=‘title’> This is the first sample HTMA document </h1>.
         <p id=‘description’> This is a description <p>
         <img id=‘image’ src=‘https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg’> 
         <a id=‘url’ href=‘http://google.es’> Link </a>
      </header>
</html>
```

## Edit the file `index.htma`.

And in the `index.htma` file, you will need to add the following code snippet: 

````html
<HTMA!>
    DIR:: myweb/content;
    REDIR:: HTMA;
    TEMPLATE:: {
        <a href=‘$url$’> Link </a>
        <img src=‘$image$’>
        <li> <a href=‘$LINK_FOR_FOR_EACH_FILE_IN_DIR$’> $title$ </a> 
        <p> $description$ </p>
    };
</HTMA>
```
## Explanation of the `index.htma` file

- **`DIR`**: As already seen, this field collects all files in a given directory.
- **`REDIR`**: Now, the collected directory extension will be `.htma`.

## Special variables

The special variables for `REDIR:HTMA` correspond to those referenced by the user in the `id` attributes of the source document. For example, `id=description` in an HTML tag will mean that a `$description$` variable will automatically be created and referenced in the HTMA. 

If the `id` is pointed to in tags that use the `src` or `href` field, the content between tags will not be captured, only the link. 

## Result

Executed the `htma.py` script, the result should look like this:

````html
<html>
    <header>
        <title>My first page with HTMA</title>
    </header>
    <body>
        <p>This are the markdown documents in the <code> content </code> directory:</p>
        <li><a href=‘/home/user/first_project/target/content/doc1.html’> Page Title</a></li>
        <li><a href=‘/home/user/first_project/target/content/doc2.html’> Page Title</a></li>
        <li>
            <a href=‘/home/user/first_project/target/content/doc3.html’> Page Title</a>
            <p>This are the HTMA documents in the <code> content </code> directory:</p>
            <a href=‘Link’> Link </a> <img src=‘https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg’ />
        </li>

        <li>
            <a href=‘/home/user/first_project/target/content/htmadoc1.html’> This is the first sample HTMA document </a>
            <p>This is a description</p>
            <a href=‘Link’> Link </a> <img src=‘https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg’ />
        </li>

        <li>
            <a href=‘/home/user/first_project/target/content/htmadoc2.html’> This is the second sample HTMA document </a>
            <p>This is a description</p>
            <a href=‘Link’> Link </a> <img src=‘https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg’ />
        </li>

        <li>
            <a href=‘/home/user/first_project/target/content/htmadoc3.html’> This is the third sample HTMA document </a>
            <p>This is a description</p>
        </li>
    </body>
</html>
``` 


