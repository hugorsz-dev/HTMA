# Using only markdown

## Insert markdown directly, without iterations
In some cases, there's no need to perform iterations, because only one markdown file exists to be embedded directly into the document.
The `REDIR:: ONLY_MD` redirection allows embedding or referencing a single markdown file, to facilitate the creation of HTML documents without the need to use tedious native tags.

## Usage example

The `DIR` attribute will not proceed, given that there is no folder in which to iterate the files, and it will only be necessary to introduce in the `ONLY_MD` variable the content or path of the markdown, and in `MD_TEMPLATE` the formatted content with the **special MD variables**,

```
<HTMA!>
 REDIR::ONLY_MD;
 ONLY_MD:: {
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
 };
 MD_TEMPLATE:: {
 $MARKDOWN_TO_HTML$
 };
</HTMA>
```

The result of this block will be:

```
<h1>Page Title</h1>
<p>This is how you write <em>italic text</em>.
This is how you write <strong>bold text</strong>.
This is how you write <a href="https://google.com">a link</a>.
This is how you write <code>code</code>.</p>
<pre><code>This is a block of code
</code></pre>
<blockquote>
<p>This is a quote</p>
</blockquote>
<ul>
<li>This is a list.</li>
<li>This is a list.</li>
</ul>
<ol>
<li>This is a numbered list.</li>
<li>This is a numbered list.</li>
</ol>
```