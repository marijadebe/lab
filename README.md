# LAB Programming language

LAB is a programming language - only a current prototype is interpreted, but I plan to write an ASM compiler in the future.

## Syntax

```c
//LAB example programs

//Hello world
x = "Hello"
out x "world!"

//sum of two digits
x = arg[0]
y = arg[1]
sum = x + y
out sum

//Is integer even or odd?
x = arg[0]
result = x % 2 == 0 ? "even" : "odd"
out result

//Area of a triangle
height = arg[0]
base = arg[1]
area = base * height / 2.0
out "Area:" area

//Factorial
x = arg[0]
vysledek = 1
while x > 1
vysledek = x * vysledek
x = x - 1
elihw
out vysledek

//FizzBuzz
x = 5
vysledek = 3
while x < 101
vysledek = x % 3 == 0 ? "Fizz" : x
vysledek = x % 5 == 0 ? "Buzz" : vysledek
vysledek = x % 3 == 0 && x % 5 == 0 ? "Fizz Buzz" : vysledek
out vysledek
x = x + 1
elihw
```

### Types

Integers
Floats
Strings


## License
[MIT](https://choosealicense.com/licenses/mit/)