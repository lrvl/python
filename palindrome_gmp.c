#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <gmp.h>

bool is_palindrome(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len/2; i++) {
        if (str[i] != str[len-i-1]) {
            return false;
        }
    }
    return true;
}

void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len/2; i++) {
        char tmp = str[i];
        str[i] = str[len-i-1];
        str[len-i-1] = tmp;
    }
}

int main(int argc, char **argv) {
    if (argc != 3) {
        printf("Usage: %s <start_num> <max_iter>\n", argv[0]);
        return 1;
    }

    mpz_t start_num, last_num, last_num_inv;
    mpz_init(start_num);
    mpz_init(last_num);
    mpz_init(last_num_inv);

    if (mpz_set_str(start_num, argv[1], 10) != 0) {
        printf("Invalid input value: %s\n", argv[1]);
        return 1;
    }

    int max_iter = atoi(argv[2]);
    if (max_iter < 0) {
        printf("Input value must be non-negative\n");
        return 1;
    }

    mpz_set(last_num, start_num);

    for (int i = 0; i < max_iter; i++) {
        char *last_num_str = mpz_get_str(NULL, 10, last_num);
        reverse_string(last_num_str);
        mpz_set_str(last_num_inv, last_num_str, 10);
        mpz_add(last_num, last_num, last_num_inv);
        free(last_num_str);

        char *last_num_palindrome_str = mpz_get_str(NULL, 10, last_num);
        if (is_palindrome(last_num_palindrome_str)) {
            printf("%s is a palindrome of %s (Found after %d iterations)\n", last_num_palindrome_str, argv[1], i+1);
            free(last_num_palindrome_str);
            return 0;
        }
        free(last_num_palindrome_str);
    }

    printf("Maximum iterations (%d) reached without finding a palindrome for %s.\n", max_iter, argv[1]);

    mpz_clear(start_num);
    mpz_clear(last_num);
    mpz_clear(last_num_inv);
    return 0;
}
