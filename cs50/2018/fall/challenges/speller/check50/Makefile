speller: dictionary.c dictionary.h speller.c Makefile
    clang -fsanitize=signed-integer-overflow -fsanitize=undefined -ggdb3 -O0 -Qunused-arguments -std=c11 -Wall -Werror -Wextra -Wno-sign-compare -Wshadow  -Wno-unused-variable -Wno-unused-parameter -c -o dictionary.o dictionary.c
    clang -fsanitize=signed-integer-overflow -fsanitize=undefined -ggdb3 -O0 -Qunused-arguments -std=c11 -Wall -Werror -Wextra -Wno-sign-compare -Wshadow -Wno-unused-variable -Wno-unused-parameter -c -o speller.o speller.c
    clang -fsanitize=signed-integer-overflow -fsanitize=undefined -ggdb3 -O0 -Qunused-arguments -std=c11 -Wall -Werror -Wextra -Wno-sign-compare -Wshadow -Wno-unused-variable -Wno-unused-parameter -o speller speller.o dictionary.o
