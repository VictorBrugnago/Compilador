# The *FooLanguage* Compiler

The Foo Language Compiler is a small and simple compiler created by a Computer Engineering Student.

  - Simple and easy to remember the commands.
  - Made in Python (lol)
  - This is just the start...

You can:
  - Declare integer variables, only (yet)
  - Using WHILE statement as loop command
  - Can run each step (Lexical, Syntactic and Semantic) separately

## Using

You can write a simple code using these commands (with examples):
### Start and Ending your code

To start writing your program, you need to write *startCode {*
To end your program, just type *} endCode*
```
startCode {
    [...]
} endCode
```
*Note*: To start and end a block of identation, you need to use *{* symbol and *}* symbol (Curly brackets)

### Variable Declaration

You can only declare **integer** variables. Other types will be implemented in future updates.
```
startCode {
    int var1;
    int var2;
    [...]
}
```
The variables **HAS TO BE** declared **AFTER** *startCode* statement and **BEFORE** any command.
Unfortunately, you can't declare variable and assign a value, you need to declare the variable and then, on another line, assign it a value.

### Variable Assignment

To assign a value to a variable you need to use the *<<* symbol.
```
startCode {
    int var1;
    int var2;

    var2 << var1 + 2;
    [...]
}endCode
```

### Input and Output

To perform a input and output, use: *inputKey()* and *outputKey()*
```
startCode {
    int var1;

    inputKey(var1);
    outputKey(var2);
}endCode
```

### Logical Operators

The following is a list of available logical operators:

| Symbol | Action          |
|--------|-----------------|
| +      | Addition                       |
| -      | Subtraction                    |
| *      | Multiplication                 |
| /      | Division                       |
| <      | Is less than                   |
| <=     | Is less than or equal to       |
| >      | Is greater than                |
| >=     | Is greater than or equal to    |
| <>     | Is not equal to                |
| ==     | Is equals to                   |

### Strings

You can print some message in your program using *Strings*.

*Note*: The type *String* doesn't exists yet.

To print some message, just write within *" "* inside a *outputKey()*
```
startCode {
    outputKey("Amazing message");
    [...]
}endCode
```

### IF and IF ELSE

To do a if statement, just type *if ([SOME LOGIC HERE]) { [SOME COMMAND HERE] };*
```
[...]
    int var1;
    int var2;
    if (var1 == var2) {
        outputKey("Some Message: ");
        outputKey(var1);
    };
    [...]
```
To do a *if else* statement, just type *if ([SOME LOGIC HERE]) { [SOME COMMAND HERE] } else { [SOME COMMAND HERE] };*
```
[...]
    int var1;
    int var2;
    if (var1 == var2) {
        outputKey("Some Message: ");
        outputKey(var1);
    } else {
        outputKey(var2);
        outputKey("Some Message");
    }
    [...]
```

### Loop (While)

An Do-Until statement -> *do { [SOME COMMAND HERE] } until { [SOME LOGIC HERE] };*
```
[...]
    int var1;
    int var2;
    int num << 2;
    while (num > 0) {
        var1 << var2 * num;
        num << num - 1;
    };
    [...]
```

## Installation

The Foo Compiler requires at least **python3.5** and **colorama** package to run.

Install the dependencies and and run the compiler.

```sh
$ pip3 install colorama
$ python3 FooCompiler.py [SOURCE_CODE.foo] [FILENAME_OUTPUT or PATH\FILENAME_OUTPUT] [parameters]
```

Also, the compiler has some parameters:

| Parameter | Action                                                             |
|-----------|--------------------------------------------------------------------|
|    -lt    | Display a list of generated tokens (**lexical**)                   |
|    -lp    | Display a list of productions performed (**syntactic**)            |
|    -ls    | Display all steps performed on detected variables (**semantic**)   |
|    -oi    | Create the Intermediate Code file (**Code Generation**)   |
|    -tudo  | Displays a detailed output of the compiler                         |
|    -vlex  | Displays a detailed output of the lexicon analyzer                 |
|    -vsyn  | Displays a detailed output of the syntactic analyzer               |
|    -vsem  | Displays a detailed output of the syntactic analyzer               |
|    -BR    | Change the language of the outputs for Brazilian Portuguese        |

## To-Do's

 - Add more types
 - Add new statements
 - Improve compiler performance
 - Create a simple IDE or spellchecker

License
----

GNU General Public License v3.0