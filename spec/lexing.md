Lexing
======

The prototypical parser expects a stream of tokens that it will then use to generate the abstract syntax tree.

This file documents the process in which a source file is broken into these tokens. For more information on how these tokens are then parsed, check the [parser documentation](https://github.com/ackwell/prototypical/blob/master/spec/parsing.md).

Tokens
------

Each token represents three pieces of information: The type of the token, the value the token represents, and the position within the source file the token was encountered.

In most cases, the type and value of the token are equal. This can be assumed to be the case unless the contrary is explicitly stated.

Whitespace
----------

Unless removing whitespace would allow two tokens to be regarded as a single one (`==` as opposed to `'= ='`), all whitespace is optional. However, newline characters have special meaning in places where it is deemed safe to place an automaic semicolon, see next section.

Within string literals and similar constructs, whitespace is preserved as-is.

There are no tokens that represent whitespace characters.

Automatic Semicolons
--------------------

***This is a planned feature.***

Each expression in prototypical sourcecode is expected to end with a semicolon by the parser. To avoid cluttering up source code, the lexer will therefore insert semicolons in places it deems safe and appropriate.

This feature should be able to be disabled in some manner on a per-file basis. Todo.

Comments
--------

Comments are handled by the lexer, and are never exposed to the parser.

A comment is initiated by a `#` that is not enclosed in a string, and extends until the end of the current line.

Punctuation
-----------

Punctuation characters are translated into tokens representing that character by itself. They are as follows:

```
(  )  {  }  [  ]
+  -  *  /  %  =
!  |  .  ,  ;
```

Compound Assignment
-------------------

Compound assignment (also known as in-place operations) **all share the same token type**. The reference implementation creativley sets this as `compound assignment`. The possible values held by the token are:

```
+=  -=  *=  /=  %=
```

Further compound assignments may be added at a later date.

Comparison
----------

Like the compound assignments, all comparison tokens share the token type `comparison`. The recognised values are:

```
<   >
<=  >=  !=  ==
```

Insert
------

The insertion arrow, `->`, is represented by a token with type `insert` and value `->`, however the value is currently not inspected.

Keywords
--------

The prototypical language uses very few keywords, however the following are treated specially and cannot be used as an identifier:

```
true
false
null
```

Identifiers
-----------

An identifier tokens' type is always set to `identifier`, with the value representing the name from the source code.

An identifier may start with any alphabetical character, or an underscore. Following characters may include numeric characters.

Additionally, either of the characters `@` or `^` may prefix the identifier. The reference implementation includes these prefixes as part of the identifier value, however this is not enforced.

Literals
--------

In addition to the boolean and null keywords above, there are a few other literal tokens which should be recognised.

### Strings

Strings are opened by either of the quote characters (`'` or `"`), and closed by a matching character.

String tokens are defined by the type `string`, and have a value equal to the text enclosed by the quotes (not including the quotes themselves).

***Not implemented:*** Quote characters may be included within a string by escaping them with a backslash `\`. Any further escape characters are handled by the parser.

### Numbers

Numbers are identified by the type `number`, and their value corresponds to the represented characters from the source file. Each token represents an unbroken sequence of numeric characters, not including whitespace or characters such as `.`.

Sequences such as `3.14` should be split into three tokens `(number 3) (. .) (number 14)`, and left to the parser to handle.

End Of File
-----------

When the end of a source file is reached, the token `eof` should be emitted. Any further requests for the next token should continue to be replied to with the `eof` token.

Unknown Characters
------------------

If a character does not fall within any of the above rules, it should be returned to the parser as token of type `unknown`, with value equal to the character found.
