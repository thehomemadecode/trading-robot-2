#include <stdio.h>
#include <string.h>
#include <Python.h>

double sma(double a) {
    a++;
    return a;
}
double ema(double a) {
    --a;
    return a;
}
double wma(double a) {
    a = a + 2;
    return a;
}
double hma(double a) {
    a = a + 3;
    return a;
}



/* function map section begin */
typedef double (*func_ptr_double)(double*, int);
typedef struct {
    const char *name;
    func_ptr_double func;
} FunctionMap;
FunctionMap functions[] = {
    {"sma", (func_ptr_double)sma},
    {"ema", (func_ptr_double)ema},
    {"wma", (func_ptr_double)wma},
    {"hma", (func_ptr_double)hma}
};
func_ptr_double get_function(const char *name) {
    for (size_t i = 0; i < sizeof(functions) / sizeof(functions[0]); ++i) {
        if (strcmp(name, functions[i].name) == 0) {
            return functions[i].func;
        }
    }
    return NULL;
}
/* function map section end */



int main() {
	//const char *functionsTAlist[4] = {"sma", "ema", "wma", "hma"};
const double close = 0;
const double open = 1;

    char input[] = "hma(9)<ema(22)>wma(1)";
    char word1[20], word2[20], word3[20];
    char separator1, separator2;

    int matched = sscanf(input, "%19[^<>=] %c %19[^<>=] %c %19[^<>=]", word1, &separator1, word2, &separator2, word3);

    if (matched == 3) {
        printf("word1: %s\n", word1);
        printf("separator: %c\n", separator1);
        printf("word2: %s\n", word2);

    } else if (matched == 5) {
        char word1f[20], word2f[20], word3f[20];
        int param1, param2, param3;
        int m1 = sscanf(word1, "%[^(](%d)", word1f, &param1);
        int m2 = sscanf(word2, "%[^(](%d)", word2f, &param2);
        int m3 = sscanf(word3, "%[^(](%d)", word3f, &param3);



    for (size_t i = 0; i < sizeof(function_names) / sizeof(function_names[0]); ++i) {
        const char *name = function_names[i];
        func_ptr_double func = get_function(name);
        for (Py_ssize_t j=0; j<4; j++) {
            printf("%s = %0.4lf\n", name, func(1,function_names_len[i]));
        }
    }




        //printf("%d %d %d\n",m1,m2,m3);
        if (m1==2) {
            printf("word1: %s %d\n", word1f,param1);
        } else {
            printf("word1: %s\n", word1);
        }
        if (m2==2) {
            printf("word2: %s %d\n", word2f,param2);
        } else {
            printf("word2: %s\n", word2);
        }
        if (m3==2) {
            printf("word3: %s %d\n", word3f,param3);
        } else {
            printf("word3: %s\n", word3);
        }

        printf("separator1: %c\n", separator1);
        printf("separator2: %c\n", separator2);

    }

/*
    int i;
    for (i = 0; i < sizeof(functions) / sizeof(functions[0]); i++) {
        if (strcmp(functions[i], "sma") == 0) {
            double result = sma(2);
            printf("sma(2) = %.2f\n", result);
        } else if (strcmp(functions[i], "ema") == 0) {
            double result = ema(2);
            printf("ema(2) = %.2f\n", result);
        } else if (strcmp(functions[i], "wma") == 0) {
            double result = wma(2);
            printf("wma(2) = %.2f\n", result);
        } else if (strcmp(functions[i], "hma") == 0) {
            double result = hma(2);
            printf("hma(2) = %.2f\n", result);
        } else {
            printf("Invalid function: %s\n", functions[i]);
        }
    }
*/


    return 0;
}
