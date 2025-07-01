# The parameters `ORDER_BY` and `REDIR_LIMIT`.

The file iterations can be ordered according to various criteria, if the `ORDER_BY` parameter is entered inside the HTMA block.

In addition, loops can also be limited to a limit number of files, using `REDIR_LIMIT`.

Both parameters can be used at the same time to, for example, only display _the last five published articles_. 

## Usage example

In this example, the image files in the previous section will be organised based on the date they were created. And instead of there being three, we will only show the two most recent ones.

```
<HTMA!>
    DIR:: myweb/content;
    REDIR:: png, jpg, gif;
    ORDER_BY:: DATE
    REDIR_LIMIT::2
    TEMPLATE:: {
        <h2> $FILE_NAME_FOR_EACH_FILE_FILE_IN_DIR$ </h2>
        <img src="$LINK_FOR_EACH_FILE_IN_DIR$">
        <p> <em> $CREATION_TIME_FOR_EACH_FILE_IN_DIR$ </em> </p> </p>
    };
</HTMA>
```

> Remember that you can use `REDIR_LIMIT` and `ORDER_BY` independently.

## Sort criteria

### `ALPHABETICAL`

Files will be sorted in alphabetical order, relative to their original name. 

### `ALPHABETICAL_REVERSE`

Files will be arranged in reverse alphabetical order, relative to their original name. 

### `DATE`

Files will be arranged based on the date they were created. 

### `DATE_REVERSE`

Files will be reverse-arranged based on the date they were created. 

### `SYSTEM`

This is the default behaviour, it sorts files in the same way the operating system displays them. 

### `SYSTEM_REVERSE`

Files will be reverse-arranged based on the default behaviour.
