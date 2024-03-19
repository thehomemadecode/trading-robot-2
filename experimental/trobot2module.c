#include <Python.h>
#include <stdio.h>
#include <string.h>

/* TA functions section begin */
double sma(double *data, int len) {
    double total = 0;
    for (int i=0; i<len; i++) {
        total += data[i];
    }
    total = total / len;
    return total;
}

double ema(double *data, int len) {
    double total = 0;
    for (int i=0; i<len; i++) {
        total += data[i];
    }
    total = total / len;
    return total;
}
/* TA functions section end */

/* function map section begin */
double (*functionsTA[])(double[], int) = {sma, ema};
/* function map section end */

/* Reception function for incoming data: */
static PyObject *receptionC(PyObject *self, PyObject *args) {
    PyObject* data; // --> data_c[i][j]
    PyObject* cols; // --> cols_c[i]
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
    double *cols_c = malloc(len_cols * sizeof(double *));
    for (Py_ssize_t i=0; i<len_cols; i++) {
        PyObject *item = PyList_GetItem(cols, i);
        cols_c[i] = (int)PyLong_AsLong(item);
    }

	int selected_functions[2];
	selected_functions[0] = 0;
	selected_functions[1] = 1;
	double res1 = functionsTA[selected_functions[0]](data_c[0], 2);
	double res2 = functionsTA[selected_functions[1]](data_c[0], 3);

	printf("testtest\n");

    //double signal = data_c[0][0];
    //double signal2 = cols_c[3];
    //return Py_BuildValue("dd", signal, signal2);
    return Py_BuildValue("dd", res1, res2);
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
