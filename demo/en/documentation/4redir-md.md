
# Markdown redirects

## What is a *special variable*?

As seen in [previous topic](3first_project.md), the `REDIR` field biases the reading of an extension: If it is `MD`, it will only read `.md` files from the directory pointed to by the `DIR` field.  

But the `REDIR` field is of radical importance in the interpretation of the `TEMPLATE`, in the use of so-called **special variables**. The **special variables** are those variables (`$VARIABLE$`) associated with a specific extension.

For example, for `REDIR: MD`, the script will have access to the special variable `MARKDOWN_TO_HTML`.

## The special variables of `REDIR:MD`.

Earlier, a simple use of the `<HTMA!>` tag in conjunction with `REDIR: MD`, oriented to markdown file redirects, was also exemplified.

Well, **this was not a simple example**, but actually encompasses the entire syntax that exists in `HTMA`, and its possibilities with respect to markdown file redirects. To understand it means to be aware of all the functions that this tool offers to present markdown documents converted to HTML format.

On this point, it will only be necessary to learn what are the *special variables* for this type of `REDIR`.

### **`MARKDOWN_TO_HTML`**.

This variable will insert the iterated `.md` file, but in HTML format. The previous page introduces its simple operation,

### **`MD_H1...MD_H6`**

The markdown headings are referenced using the `MD_Hn[i]` variable. 

For example, to display the seventh third-level header appearing in a document, `MD_H3[6]` would be called.

Headers in particular have the ability to be iterated, as seen in the example on the previous page, using the `MD_Hn` tag

### **`MD_IMG`**

The images in the markdown are referenced using the `MD_IMG[i]` variable. 

This will return the absolute link to the image in question or, if it is an external page, its corresponding link. 

### **`MD_URL`**

Markdown links are referenced using the `MD_URL[i]` variable. 

This will return the absolute link of the link in question or, if it is an external page, its corresponding link. 

### **`MD_QUOTE`**

Markdown quotes are referenced using the `MD_QUOTE[i]` variable. 

### **`MD_TEXT`**

The remainder of the markdown text that is not deposited in the above variables - paragraphs - is entered in `MD_TEXT[i]`.

## `MD_TEMPLATE` in separate files.

As this is a template, the content of `MD_TEMPLATE` may need to be the same on several occasions. 

``` html
<html>
    <header>
        <title> $MD_H1[0]$ </title>
    </header>
    
    <body>
        $MARKDOWN_TO_HTML$
    </body>
</html>
```

To avoid repeating the content of the same template, it is advisable to save `MD_TEMPLATE` in a file with the extension `.htma.template`, such as `example.md.template`, and reference the file instead.

```
MD_TEMPLATE: {path/to/example.md.template}
```
