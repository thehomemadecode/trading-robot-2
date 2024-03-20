#include <Python.h>
//#include <stdio.h>

static PyObject *cryptocurrencyGateA(PyObject *self, PyObject *args) {
	PyObject* data;
	int col;
	if (!PyArg_ParseTuple(args, "Oi", &data, &col)) {
		return NULL;
	}
	PyObject* data4 = PyList_GetItem(data, 4);
	//Py_ssize_t data4s = PyList_Size(data4);
	PyObject* datarow;
	PyObject* datacell;
	PyObject* datalist = PyList_New(0);
	PyObject* valuef;
	double value = 0;
	double price = 0;
	for (int i=0; i<9; i++) {
		datarow = PyList_GetItem(data4, i);
		datacell = PyList_GetItem(datarow, col);
		PyList_Append(datalist, datacell);
		valuef = PyFloat_FromString(datacell);
		value = value + PyFloat_AsDouble(valuef);
	}
	value = value / 9;

	datarow = PyList_GetItem(data4, 0);
	datacell = PyList_GetItem(datarow, 3);
	valuef = PyFloat_FromString(datacell);
	price = PyFloat_AsDouble(valuef);
	
	double signal = 0;
	if (price > value) {
		signal = 1;
	}
	return Py_BuildValue("dd", signal, value);
}
	// 0:assetname 1:timeperiod 2:timedata 3:prefix 4:data
	/*
	char* assetname = "";
	PyObject* py_string_object = PyList_GetItem(data, 0);
	PyObject* py_bytes_object = PyUnicode_AsUTF8String(py_string_object);
	assetname = PyBytes_AsString(py_bytes_object);
	Py_DECREF(py_bytes_object);
	*/
	//PyObject *returnvalues = Py_BuildValue("d",value);	
	//PyObject *returnvalues = Py_BuildValue("O", datalist);
	//int result = datasize + col;
	//return Py_BuildValue("s", assetname);
	////////////////return returnvalues;
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
/*
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
	// test3
  return x;
}
*/
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
	{"cryptocurrencyGateA", cryptocurrencyGateA, METH_VARARGS, "cryptocurrencyGateA"},
    //{"check", check, METH_VARARGS, "check"},	
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
