#include <Python.h>
#include <stdio.h>
#include <string.h>

/* TA functions section begin */
double sma(double *data) {
    double total = 0;
    int len = 2;
    for (int i=0; i<len; i++) {
        total += data[i];
    }
    total = total / len;
    return total;
}

double ema(double *data) {
    double total = 0;
    int len = 2;
    for (int i=0; i<len; i++) {
        total += data[i];
    }
    total = total / len;
    return total;
}
/* TA functions section end */

/* function map section begin */
typedef double (*func_ptr_double)(double*);
typedef struct {
    const char *name;
    func_ptr_double func;
} FunctionMap;
FunctionMap functions[] = {
    {"sma", (func_ptr_double)sma}, // Yeniden dönüştürme yapılır
    {"ema", (func_ptr_double)ema}, // Yeniden dönüştürme yapılır
};
func_ptr_double get_function(const char *name) {
    for (size_t i = 0; i < sizeof(functions) / sizeof(functions[0]); ++i) {
        if (strcmp(name, functions[i].name) == 0) {
            return functions[i].func;
        }
    }
    return NULL; // Eşleşme yoksa NULL döndür
}
/* function map section end */

/* Reception function for incoming data: */
static PyObject *receptionC(PyObject *self, PyObject *args) {
    PyObject* data;
    PyObject* cols;
    PyObject* analysisrules;
    if (!PyArg_ParseTuple(args, "OOO", &data, &cols, &analysisrules)) {
        return NULL;
    }

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

    Py_ssize_t len_cols = PyList_Size(cols);
    int cols_c[len_cols];
    for (Py_ssize_t i = 0; i < len_cols; ++i) {
        PyObject *item = PyList_GetItem(cols, i);
        cols_c[i] = (int)PyLong_AsLong(item);
    }

    Py_ssize_t len = PyList_Size(analysisrules);
    const char *function_names[len];
    for (Py_ssize_t i = 0; i < len; ++i) {
        PyObject *item = PyList_GetItem(analysisrules, i);
        const char *name = PyUnicode_AsUTF8(item);
        function_names[i] = name;
    }
    
    for (size_t i = 0; i < sizeof(function_names) / sizeof(function_names[0]); ++i) {
        const char *name = function_names[i];
        func_ptr_double func = get_function(name);
        for (Py_ssize_t j=0; j<num_rows; j++) {
            printf("%s = %lf\n", name, func(data_c[j]));
        }
    }





    double signal = 0;
    double signal2 = 0;
    return Py_BuildValue("dd", signal, signal2);
}
/* Reception function end */

/* for Python.h to the end of code */
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
/* end of code */