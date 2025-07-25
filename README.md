# Format-String-2
This covers the picoCTF challenge: Format String 2

## Overview:
I won't explain what a format string attack is (that is a google search away). But in this challenge, you need to change the value of the global variable sus to a particular value to win. The value is 0x67616c66, which can be found within the source code. This requires memory overwriting with the %n format specifier. 

## How to Use the Script: 
Running the script asks for 3 things:
 - Offset: This is where the format string appears on the stack. You can determine this by doing AAAAAAAA, which writes 4141414141414141 onto the stack. Then, you look for these numbers by repeating .%lx a bunch of times, searching within your output for these numbers. When you find it, count how many sections it took to reach the format string (in my practice, it was 14).
 - Address of sus: Write in 0x#### format. This address can be found in a variety of ways, including GDB and objdump.
 - Value to write to sus: Given by the problem: 0x67616c66

## How the payload works (generally)
%n takes in an address, and writes in memory the current amount of characters printed. 
%14$n means to write the number to the address found at the 14th position on the stack
%hhn writes 1 bytes instead of the normal 4 bytes (so we can write the number chunk by chunk)

The number of characters can be controlled by using %#c, where # is some number. %252c will print 252 characters, 1 characters and 251 spaces. This is how we get to specific numbers. 

The addresses are located at the end of the payload. For some reason, if you include the addresses at the front, the format specifiers won't be read properly. My guess is the null character (\x00) is the culprit for this. 

The general format will be: 
 - print a certain amount of characters (with %c)
 - write into memory (with %n, referencing an address at the end)
 - this is repeated as many times as needed
 - memory addresses sit in the back
 - *%hhn takes a byte of the total number of characters printed (in hex form) and writes it into memory (1 bytes, two hex digits)
 - *padding characters could be included right before the addresses. Since each address takes exactly 8 bytes, and the stack goes in 8 byte chunks at a time, the rest of the payload needs to be a multipe of 8, so that the addresses are not misaligned
 - Some parts of the address can be represented by printable characters (ex: @, `, e) while others are unprintable and so are written in a special hex notation (\x00 - null character)
