Standard Library
================

The prototypical language itself is very bare. To provide functionality, it ships with a standard library.

It is perfectly possible to overrite the definition of the names registered by the standard library, however large sections of it are not possible to reproduce with pure prototypical code (such as `if`), so this is generally not a good idea.

Control Flow
------------

The language does not have any constructs or keywords such as loops or conditionals. Instead, these are implemented with standard library functions.

### if(condition, callback)

If the `condition` is truthy, the callback will be executed. The callback should expect no arguments. The `result` field in the object returned will be `true` if the callback was run, and `false` otherwise.

```
if(true, {
	# Will be executed
});
```

### else(callback)

If the `scope`s `result` is falsey, the callback will be executed. This provides expected behaviour when chaining with `if`:

```
if(false, {
	# Will not be executed
}).else({
	# Will be executed
});
```

However it can also be chained onto *any* function that has a `result` that can be interpreted as a boolean:

```
function = {
	result = false;
};

function().else({
	# Will be executed
});
```

Input/Output
------------

### in(prompt...)

### out(values...)
