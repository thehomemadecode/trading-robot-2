#include <Python.h>

static PyObject *check(PyObject *self, PyObject *args) {
	PyObject* data;
	if (!PyArg_ParseTuple(args, "i", &data)) {
        return NULL;
    }
	return Py_BuildValue("i", data);
}

static PyObject *sma(PyObject *self, PyObject *args) {
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

static PyMethodDef trobot2Methods[] = {
    {"check", check, METH_VARARGS, "check"},
    {"sma", sma, METH_VARARGS, "Simple moving average"},
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
