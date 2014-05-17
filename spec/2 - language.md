Language
========

Objects
-------

***NOTE:*** The current implementation does not follow much of this at all, and instead defers to python. This is purely for convenience, and will not be the case when the final implementation is written.

All data processed by prototypical is stored as a form of object. Objects are comprised of a collection of named fields, and a list of parent objects. Either or both may be empty.

To access the value of a field, 'dot notation' can be used (`object.field`). Additionally, values can also be looked up with a string using array-style access (`object['field']`). Both methods yield the same result.

When objects are nested, additional fields may be appended to the end to access the children: `grandparent.parent.child` or `grandparent['parent']['child']`.

### Special Fields

Some field names are special, in that they are used for specific purposes, or carry specific meaning within idomatic code. (Pythonistas may recognise this behaviour from 'magic' methods).

Field Name | Expected Value
---------- | --------------
`result`   | The final result of a function's computation (if any).

*(More to be added)*

### Primitive Objects

Primitive objects are those specified by the core language. The only difference is that they have additional components, containing their values or so on. How this is handled is an implementation detail.

The reference implementation defines the following primitive objects:

* Number (`1`, `3.14`)
* String (`'hello, world'`, `"This was a triumph!"`)
* Boolean (`true`, `false`)
* Null (`null`)
* Function (see section in expression docs)
* List (`[1, 'a string', (arg){ }]`) *(todo)*

Functions
---------

Functions are a particularly special type of object. Their primary purpose is to generate further objects. Before they can be used, functions must first be defined by assigning a function literal to a field.

```
aFunction = (argument, anotherArgument) {
	# function body
};

# While empty parenthesis are valid, it is more idiomatic to completely omit them if the function
# accepts no arguments
noArgsFunction = {
	# function body
};
```

The function body may consist of any number of expressions, just like the root file context.

To call a function, reference its location, followed by parameters enclosed with parenthesis. 

```
aFunction('hello', 'world');

# Parameters are not optional when calling.
noArgsFunction();
```

### Return value

An important thing to note is that a function ***will always*** return an object. To this end, there is no `return` keyword or equivalent.

If your function calculates a specific value, it *should* be stored in the `result` field as documented above (though no-one is going to force you).

When setting variables within a function body, the object the function is generating will be used as context. See the next section for more detail on context and scope.

Scoping
-------

Scoping in prototypical is rather... fluid, for want of a better word. Throught this section, a 'context' is an object.

When a function is defined, it inherits the scope in which it was defined as a **parent**.

When requesting a variable, first the current context is checked to see if it exists. If it is not found, its parents will be checked in order. Because the parents are also objects, potentially with parents, this lookup is **depth first**. If all parents are exausted and the variable has not been found, the primative `null` object will be returned.

Likewise, when setting a variable, first the local context, then the parents are checked for existence, and the value is set when it is found. If it does not already exist, it will be set *on the current context* (as you may expect).

This lookup behaviour may be overwritten with identifier prefixes, `@` and `^`. If an identifier is prefixed with `@`, lookups will not check parents, restricting them to only the local context. Conversely, when prefixed with `^`, lookups will not check the local context, instead only the parents. Due to the possibility of many parents, if an assignment to an indentifier prefixed with `^` fails to find an existing field, it will throw an error.

### Function call scope

When a function is called, the local context of the *caller* is also accessible from within the function via the `scope` namespace. That is, if the caller's scope contains `a = 1;`, then the function body can access the value of `a` with `scope.a`.

Leading on from that, because functions return objects, function chains also inject scope in this manner. Given the chain:

`function().anotherFunction().yetAnotherFunction()`

each successive function call's `scope` will be equal to the object returned by the previous function. The first call recieves the scope the chain is within.

Error Handling
--------------

*(currently handled with python, needs work)*
