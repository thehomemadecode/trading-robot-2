#include <Python.h>
#include <stdio.h>
#include <string.h>

#define TRUE 0b1
#define FALSE 0b0
#define GT '>'
#define LT '<'
#define ET '='

/* TA functions section begin */
double sma(double a[], int len) {
    double res = a[0]+len;
	return res;
}
double ema(double a[], int len) {
    double res = a[0]+len;
	return res;
}
double wma(double a[], int len) {
    double res = a[0]+len;
	return res;
}
double hma(double a[], int len) {
    double res = a[0]+len;
	return res;
}
/* TA functions section end */

/* function map section begin */
const char *functionsTAlist[4] = {"sma", "ema", "wma", "hma"};
double (*functionsTA[])(double[], int) = {sma, ema, wma, hma};
/* function map section end */

/* Reception function for incoming data: */
static PyObject *receptionC(PyObject *self, PyObject *args) {
    PyObject* data; // --> data_c[i][j]
    PyObject* cols; // --> cols_c[i]
    PyObject* analysisrule; // --> analysisrule 'atoms'
    if (!PyArg_ParseTuple(args, "OOO", &data, &cols, &analysisrule)) {
        return NULL;
    }
	
	// --> data_c[i][j]
    Py_ssize_t num_rows = PyList_Size(data);
    Py_ssize_t num_cols = 0;
    double **data_c = malloc(num_rows * sizeof(double *));
    for (Py_ssize_t i = 0; i < num_rows; ++i) {
        PyObject *row = PyList_GetItem(data, i);
        num_cols = PyList_Size(row);
        data_c[i] = malloc(num_cols * sizeof(double));
        for (Py_ssize_t j = 0; j < num_cols; ++j) {
            PyObject *item = PyList_GetItem(row, j);
            data_c[i][j] = PyFloat_AsDouble(item);
        }
    }
	
	// --> cols_c[i]
    Py_ssize_t len_cols = PyList_Size(cols);
    double *cols_c = malloc(len_cols * sizeof(double *));
    for (Py_ssize_t i=0; i<len_cols; i++) {
        PyObject *item = PyList_GetItem(cols, i);
        cols_c[i] = (int)PyLong_AsLong(item);
    }

	// --> analysisrule 'atoms'
	PyObject* analysisrulePy = PyUnicode_AsUTF8String(analysisrule);
	char* analysisruleC = PyBytes_AsString(analysisrulePy);
    char word1[20], word2[20], word3[20];
    char separator1, separator2;

	int matched = sscanf(analysisruleC, "%19[^<>=] %c %19[^<>=] %c %19[^<>=]", word1, &separator1, word2, &separator2, word3);
	//printf("matched: %d\n",matched);

    char word1f[20], word2f[20], word3f[20];
    int param1, param2, param3;
    double res1, res2, res3;
    int index;
    unsigned char result,result2;
    if (matched == 3) {
        int m1 = sscanf(word1, "%[^(](%d)", word1f, &param1);
        int m2 = sscanf(word2, "%[^(](%d)", word2f, &param2);
        //printf("%d %d %d\n",m1,m2);
        if (m1==2) {
            printf("word1: %s %d\n", word1f,param1);
			index = -1;
		    for (int i = 0; i < 4; ++i) {
		        if (strcmp(functionsTAlist[i], word1f) == 0) {
		            index = i;
		            res1 = functionsTA[i](data_c[0], param1);
		            printf("_res1: %f\n",res1);
		            break;
		        }
		    }
        } else {
            printf("word1: %s\n", word1);
        }
        if (m2==2) {
            printf("word2: %s %d\n", word2f,param2);
			index = -1;
		    for (int i = 0; i < 4; ++i) {
		        if (strcmp(functionsTAlist[i], word2f) == 0) {
		            index = i;
		            res2 = functionsTA[i](data_c[0], param2);
		            printf("_res2: %f\n",res2);
		            break;
		        }
		    }
        } else {
            printf("word2: %s\n", word2);
        }
        printf("separator1: %c\n", separator1);

        if      (separator1 == GT) {if(res1 > res2){result = TRUE;} else {result = FALSE;}}
        else if (separator1 == LT) {if(res1 < res2){result = TRUE;} else {result = FALSE;}}
        else if (separator1 == ET) {if(res1 == res2){result = TRUE;} else {result = FALSE;}}
        else {result = FALSE;}
        if (result==TRUE) {printf("TRUE\n");} else {printf("FALSE\n");}
        

    } else if (matched == 5) {
        int m1 = sscanf(word1, "%[^(](%d)", word1f, &param1);
        int m2 = sscanf(word2, "%[^(](%d)", word2f, &param2);
        int m3 = sscanf(word3, "%[^(](%d)", word3f, &param3);
        //printf("%d %d %d\n",m1,m2,m3);
        if (m1==2) {
            printf("word1: %s %d\n", word1f,param1);
			index = -1;
		    for (int i = 0; i < 4; ++i) {
		        if (strcmp(functionsTAlist[i], word1f) == 0) {
		            index = i;
		            res1 = functionsTA[i](data_c[0], param1);
		            printf("_res1: %f\n",res1);
		            break;
		        }
		    }
        } else {
            printf("word1: %s\n", word1);
        }
        if (m2==2) {
            printf("word2: %s %d\n", word2f,param2);
			index = -1;
		    for (int i = 0; i < 4; ++i) {
		        if (strcmp(functionsTAlist[i], word2f) == 0) {
		            index = i;
		            res2 = functionsTA[i](data_c[0], param2);
		            printf("_res2: %f\n",res2);
		            break;
		        }
		    }
        } else {
            printf("word2: %s\n", word2);
        }
        if (m3==2) {
            printf("word3: %s %d\n", word3f,param3);
			index = -1;
		    for (int i = 0; i < 4; ++i) {
		        if (strcmp(functionsTAlist[i], word3f) == 0) {
		            index = i;
		            res3 = functionsTA[i](data_c[0], param3);
		            printf("_res3: %f\n",res3);
		            break;
		        }
		    }
        } else {
            printf("word3: %s\n", word3);
        }
        printf("separator1: %c\n", separator1);
        printf("separator2: %c\n", separator2);

        if      (separator1 == GT) {if(res1 > res2){result = TRUE;} else {result = FALSE;}}
        else if (separator1 == LT) {if(res1 < res2){result = TRUE;} else {result = FALSE;}}
        else if (separator1 == ET) {if(res1 == res2){result = TRUE;} else {result = FALSE;}}
        else {result = FALSE;}

        if      (separator2 == GT) {if(res2 > res3){result2 = TRUE;} else {result2 = FALSE;}}
        else if (separator2 == LT) {if(res2 < res3){result2 = TRUE;} else {result2 = FALSE;}}
        else if (separator2 == ET) {if(res2 == res3){result2 = TRUE;} else {result2 = FALSE;}}
        else {result2 = FALSE;}
        
        result = result && result2;

        if (result==TRUE) {printf("TRUE\n");} else {printf("FALSE\n");}

    }
	/*
	int selected_functions[2];
	selected_functions[0] = 0;
	selected_functions[1] = 1;
	double res1 = functionsTA[selected_functions[0]](data_c[0], 2);
	double res2 = functionsTA[selected_functions[1]](data_c[0], 3);
	*/

	if (matched == 3) {
		return Py_BuildValue("dd", res1, res2);
	} else if (matched == 5) {
		return Py_BuildValue("ddd", res1, res2, res3);
	} else {
		return Py_BuildValue("i", -1);
	}
    
}
/* Reception function end */

/* Python.h definitions begin */
static PyMethodDef trobot2Methods[] = {
    {"receptionP", receptionC, METH_VARARGS, "Reception function for incoming data."},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef trobot2 = {
    PyModuleDef_HEAD_INIT,
    "trobot2",
    "Python interface for trobot2 C library functions",
    -1,
    trobot2Methods
};
PyMODINIT_FUNC PyInit_trobot2(void) {
    return PyModule_Create(&trobot2);
}
/* Python.h definitions end */
/* that's all folks -- the end of the code */
