# Linux Booting

[!] CS:IP does not apply at reboot

# assembly example
```nasm
section .data
    msg db 'Hello, World!', 0xA   ; Message to print with newline
    msg_len equ $ - msg           ; Calculate length of the message

section .text
    global _start

_start:
    ; Write message to stdout (system call: write)
    mov eax, 4                    ; syscall number for write
    mov ebx, 1                    ; file descriptor (stdout)
    mov ecx, msg                  ; pointer to the message
    mov edx, msg_len              ; length of the message
    int 0x80                      ; make the syscall

    ; Exit the program (system call: exit)
    mov eax, 1                    ; syscall number for exit
    xor ebx, ebx                  ; exit code 0
    int 0x80                      ; make the syscall
```

[e] pay attention to browser elements

[ ] checkbox emtpy
[x] checkbox crossed
