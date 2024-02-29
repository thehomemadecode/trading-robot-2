#include <Python.h>
#include <stdio.h>

static PyObject *cryptocurrencyGate(PyObject *self, PyObject *args) {
	PyObject* selecteddata;
	int col;
	PyObject* allrules;
	if (!PyArg_ParseTuple(args, "OiO", &selecteddata, &col, &allrules)) {
		return NULL;
	}
	Py_ssize_t selecteddatasize = PyList_Size(selecteddata);
	PyObject* rowdata;
	PyObject* datagroup;
	PyObject* data;
	PyObject* datacell;
	PyObject* datalist = PyList_New(0);
	for (int i=0; i<selecteddatasize; i++) {
		rowdata = PyList_GetItem(selecteddata, i);
		Py_ssize_t rowdatasize = PyList_Size(rowdata);
		for (int j=3; j<rowdatasize; j++) {
			datagroup = PyList_GetItem(rowdata, j);
			Py_ssize_t datagroupsize = PyList_Size(datagroup);
			for (int k=0; k<datagroupsize; k++) {
				data = PyList_GetItem(datagroup, k);
				datacell = PyList_GetItem(data, col);
				PyList_Append(datalist, datacell);
			}
		}
	}
	PyObject *returnvalues = Py_BuildValue("O", datalist);
	return returnvalues;
}

static PyObject *check(PyObject *self, PyObject *args) {
	PyObject* data;
	if (!PyArg_ParseTuple(args, "i", &data)) {
		return NULL;
	}
	data = subcheck(data);
	return Py_BuildValue("i", data);
}

int subcheck(int x) {
	x++;
  return x;
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
    {"cryptocurrencyGate", cryptocurrencyGate, METH_VARARGS, "cryptocurrencyGate"},
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
