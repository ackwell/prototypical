Prototypical
============

***This README is incomplete!***

**Note:** This is a work in progress, and will be subject to change without notice. Probably without updated docs too, knowing myself.

Prototypical (working name) is a dynamically typed, interpreted language. I plan to keep the language and it's syntax as simple as possible, while allowing a great deal of ~~hackery~~ flexibility for the coder.

Syntax
------

The syntax borrows heavily from existing languages, so most constructs should seem familiar.

Rather than trying to explain each part one at a time, here's a code snippet which goes over most of the basic usage:

```
# Assign `num` the value 10.0 (all numbers are floats)
num = 10;

# Assign `str` a string value
str = 'hello world';

# out()/in() are the IO functions. Same arguments as python's print()/input()
out('hello, world');
# > hello, world

# Mathematical operations are inherited from python (at least currently)
out(5 - 4);
# > 1.0
out('hello, ' + 'world');
# > hello, world
```
