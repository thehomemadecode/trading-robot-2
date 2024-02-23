#include <Python.h>

static PyObject *ma(PyObject *self, PyObject *args) {
    PyObject* py_list;
	PyObject* py_list2;
	PyObject* item;
	int ohlc = 0;
	int period = 0;
	double sonuc = 0;
	double value = 0;
    if (!PyArg_ParseTuple(args, "Oii", &py_list, &ohlc, &period)) {
        return NULL;
    }
	Py_ssize_t size = PyList_Size(py_list);
	for (Py_ssize_t i = size-1; i > size-period-1; i--) {
		py_list2 = PyList_GetItem(py_list, i);
		item = PyList_GetItem(py_list2, ohlc);
		value = PyFloat_AsDouble(item);
		sonuc = sonuc + value;
	}
	sonuc = sonuc / period;
	return Py_BuildValue("d", sonuc);
}

static PyObject *topla(PyObject *self, PyObject *args) {
    int a, b;
    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }
	int sonuc = a + b;
	return Py_BuildValue("i", sonuc);
}

static PyObject *fark(PyObject *self, PyObject *args) {
    int a, b;
    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }
	int sonuc = a - b;
	return Py_BuildValue("i", sonuc);
}

static PyMethodDef trobotMethods[] = {
    {"topla", topla, METH_VARARGS, "Python interface for trobot C library functions"},
    {"fark", fark, METH_VARARGS, "Python interface for trobot C library functions"},
    {"ma", ma, METH_VARARGS, "Python interface for trobot C library functions"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef trobot = {
    PyModuleDef_HEAD_INIT,
    "trobot",
    "Python interface for trobot C library functions",
    -1,
    trobotMethods
};

PyMODINIT_FUNC PyInit_trobot(void) {
    return PyModule_Create(&trobot);
}
