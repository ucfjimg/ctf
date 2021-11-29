#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <openssl/sha.h>

int main()
{
    char pw[] = "SaltyMcSaltFaceAAAAAAAAAAA";
    size_t len = strlen(pw);

    uint8_t buf[32];

    long n = 0;

    while (true) {
        SHA256_CTX ctx;
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, pw, len);
        SHA256_Final(buf, &ctx);

        if (buf[0] == '#' && buf[1] == '!' && buf[2] == 'x' && buf[3] == 0x0a) {
            printf("%s\n", pw);
            break;
        }

        n++;
        if (n == 10000000) {
            printf(".");
            fflush(stdout);
            n = 0;
        }

        int i = len - 1;

        while (i >= 0) {
            pw[i]++;
            if (pw[i] <= 'Z') {
                break;
            } else {
                pw[i] = 'A';
                i--;
            }
        }

        if (i < 0) {
            break;
        }
    }
}

