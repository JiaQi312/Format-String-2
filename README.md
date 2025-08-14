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

## My Answer
Provided format string: 

**b'%102c%20$llnc%21$hhn%5c%22$hhn%245c%23$hhnaaaaba`@@\x00\x00\x00\x00\x00c@@\x00\x00\x00\x00\x00a@@\x00\x00\x00\x00\x00b@@\x00\x00\x00\x00\x00'**

- My offset was 14
- Address of sus: 0x404060
- Value to write: 0x67616c66

  Breakdown:
&nbsp;The payload order: 1)66 2)67 3)6c 4)61

1. Payload writes 102 characters with %102c
2. Writes the # of characters to the address found at the 20th stack position, %20$lln writes the whole number as a hex, I believe the %lln is used instead of %n for padding (mentioned earlier). 102 characters have been printed, translating to 66 in hex. (sus = 0x 21 73 75 66)
3. the c after the n increments the character count by 1 (66 -> 67)
4. Writes the 67 using %21$hhn, the 21st position refers to the address c@@\x00\x00\x00\x00\x00, which is the position of the first two digits of sus (sus = 0x 67 73 75 66)
5. %5c writes 5 more characters, count is now at 108 (6c in hex)
6. 6c is written to the address of the 22nd position using %22$hhn (address is a@@\x00\x00\x00\x00\x00) (sus = 0x 67 73 6c 66)
7. %245c writes 245 characters, count is now 353 (in hex is 161)
8. %23$hhn writes the first two hex digits of the character count (61) into the address found at the 23rd position (address = b@@\x00\x00\x00\x00\x00) (sus = 0x 67 61 6c 66)
9. aaaaba is more padding
10. Addresses are now found here at the end
