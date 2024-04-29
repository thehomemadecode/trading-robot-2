#include <Python.h>
#include <stdio.h>
#include <string.h>

#define TRUE 0b1
#define FALSE 0b0
#define GT '>'
#define LT '<'
#define ET '='

/* TA functions section begin */
double sma(double **a, int col, int len) {
	double sma = 0;
	for (int e=0;e<len;e++) {
		//printf("%d %d %f\n",e,len,a[e][3]);
		sma += a[e][col];
	}
	sma = sma/len;
	return sma;
}
//EMA = alpha * source + (1 - alpha) * EMA[1], ;; alpha = 2 / (length + 1).
double ema(double **a, int col, int len) {
	double multiplier = 2.0 / (len + 1);
	double ema = a[len][col];
	for (int e=len-1;e>=0;--e) {
		ema = (a[e][col] * multiplier) + (ema * (1-multiplier));
	}
	return ema;
}
double rsi(double **a, int col, int len) {
	double rsi = 0;
	double gain = 0;
	double loss = 0;
	int g = 0, l = 0;
	for (int e=0;e<len;e++) {
		if (a[e][col] > a[e+1][col]) {
			gain += a[e][col] - a[e+1][col];
			g++;
		}
		else {
			loss += a[e+1][col] - a[e][col];
			l++;
		}
	}	
	gain /= len;
	loss /= len;
	//printf("%d %d \n",g,l);
	rsi = 100 - (100/(1+(gain/loss)));
	return rsi;
}
double *macd(double **a, int col, int macd12len, int macd26len, int smoothing_signal_length) {
	double macd = 0;
	double macd12 = 0;
	double macd26 = 0;
	double macdsignal = 0;

	macd12 = ema(a,col,macd12len);
	macd26 = ema(a,col,macd26len);
	macd = macd12-macd26;

	for (int i=0; i<smoothing_signal_length; i++) {
		macd12 = ema(a,col,macd12len);
		macd26 = ema(a,col,macd26len);
		macdsignal += macd12-macd26;
		//printf("%i macd: %f \n",i,macdsignal);

		for (int i=0;i<macd26len+smoothing_signal_length;i++) {
			for (int j=0;j<6;j++) {
				a[i][j] = a[i+1][j];
			}
		}
	}
	double macdseries[4] = {macd,macd12,macd26,macdsignal/smoothing_signal_length};
	printf("%f %f %f %f \n",macd,macd12,macd26,macdsignal/smoothing_signal_length);
	return macdseries;
	//return macd;
}
/* TA functions section end */

/* function map section begin */
const char *functionsTAlist[4] = {"sma", "ema", "rsi", "macd"};
double (*functionsTA[])(double**, int, int) = {sma, ema, rsi};
double *(*functionsTA2[])(double**, int, int, int, int) = {macd};
/* function map section end */

/* Reception function for incoming data: */
static PyObject *receptionC(PyObject *self, PyObject *args) {
	PyObject* data; // --> data_c[i][j]
	int col; // --> col
	PyObject* analysisrule; // --> analysisrule 'atoms'
	if (!PyArg_ParseTuple(args, "OiO", &data, &col, &analysisrule)) {
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
			item = PyFloat_FromString(item); // comment it while working with work.py !!!!!!!!!
			data_c[i][j] = PyFloat_AsDouble(item);
		}
	}

	// --> analysisrule 'atoms'
	PyObject* analysisrulePy = PyUnicode_AsUTF8String(analysisrule);
	char* analysisruleC = PyBytes_AsString(analysisrulePy);
	char word1[20], word2[20], word3[20];
	char operator1, operator2;

	int matched = sscanf(analysisruleC, "%19[^<>=] %c %19[^<>=] %c %19[^<>=]", word1, &operator1, word2, &operator2, word3);
	//printf("matched: %d\n",matched);

	char word1f[20], word2f[20], word3f[20];
	int param1, param12, param13;
	int param2, param22, param23;
	int param3;
	double res1, res2, res3;
	const char *ohlclist[6] = {"open", "high", "low", "close", "volume", "qvolume"};
	unsigned char result,result2;
	if (matched == 3) {
		int m1 = sscanf(word1, "%[^(](%d,%d,%d)", word1f, &param1, &param12, &param13);
		int m2 = sscanf(word2, "%[^(](%d,%d,%d)", word2f, &param2, &param22, &param23);
		//printf("%d %d\n",m1,m2);
		if (m1==4) {
			double* arr;
			arr = macd(data_c, col, param1, param12, param13);
			/*
			printf("arr0: %f\n",arr[0]);
			printf("arr1: %f\n",arr[1]);
			printf("arr2: %f\n",arr[2]);
			printf("arr3: %f\n",arr[3]);
			*/
			res1 = 0;
		}
		if (m1==2) {
			//printf("word1: %s %d\n", word1f,param1);
			for (int i = 0; i < 4; ++i) {
				if (strcmp(functionsTAlist[i], word1f) == 0) {
					res1 = functionsTA[i](data_c, col, param1);
					//printf("_res1: %f\n",res1);
					break;
				}
			}
		} else {
			//printf("word1: %s\n", word1);
			char numberv = 1;
			for (int i = 0; i < 6; ++i) {
				if (strcmp(ohlclist[i], word1) == 0) {
					res1 = data_c[0][i];
					//printf("_%s: %f\n",word1,res1);
					numberv = 0;
					break;
				}
			}
			if (numberv) {sscanf(word1, "%lf", &res1);//printf("numberv res1: %f\n",res1);
			}
		}
		if (m2==2) {
			//printf("word2: %s %d\n", word2f,param2);
			for (int i = 0; i < 4; ++i) {
				if (strcmp(functionsTAlist[i], word2f) == 0) {
					res2 = functionsTA[i](data_c, col, param2);
					//printf("_res2: %f\n",res2);
					break;
				}
			}
		} else {
			//printf("word2: %s\n", word2);
			char numberv = 1;
			for (int i = 0; i < 6; ++i) {
				if (strcmp(ohlclist[i], word2) == 0) {
					res2 = data_c[0][i];
					//printf("_%s: %f\n",word2,res2);
					numberv = 0;
					break;
				}
			}
			if (numberv) {sscanf(word2, "%lf", &res2);//printf("numberv res2: %f\n",res2);
			}
		}
		//printf("operator1: %c\n", operator1);

		if	  (operator1 == GT) {if(res1 > res2){result = TRUE;} else {result = FALSE;}}
		else if (operator1 == LT) {if(res1 < res2){result = TRUE;} else {result = FALSE;}}
		else if (operator1 == ET) {if(res1 == res2){result = TRUE;} else {result = FALSE;}}
		else {result = FALSE;}
		//if (result==TRUE) {printf("TRUE\n");} else {printf("FALSE\n");}

	} 
	else if (matched == 5) {
		int m1 = sscanf(word1, "%[^(](%d)", word1f, &param1);
		int m2 = sscanf(word2, "%[^(](%d)", word2f, &param2);
		int m3 = sscanf(word3, "%[^(](%d)", word3f, &param3);
		//printf("%d %d %d\n",m1,m2,m3);
		if (m1==2) {
			//printf("word1: %s %d\n", word1f,param1);
			for (int i = 0; i < 4; ++i) {
				if (strcmp(functionsTAlist[i], word1f) == 0) {
					res1 = functionsTA[i](data_c, col, param1);
					//printf("_res1: %f\n",res1);
					break;
				}
			}
		} else {
			//printf("word1: %s\n", word1);
			char numberv = 1;
			for (int i = 0; i < 6; ++i) {
				if (strcmp(ohlclist[i], word1) == 0) {
					res1 = data_c[0][i];
					//printf("_%s: %f\n",word1,res1);
					numberv = 0;
					break;
				}
			}
			if (numberv) {sscanf(word1, "%lf", &res1);//printf("numberv res1: %f\n",res1);
			}
		}
		if (m2==2) {
			//printf("word2: %s %d\n", word2f,param2);
			for (int i = 0; i < 4; ++i) {
				if (strcmp(functionsTAlist[i], word2f) == 0) {
					res2 = functionsTA[i](data_c, col, param2);
					//printf("_res2: %f\n",res2);
					break;
				}
			}
		} else {
			//printf("word2: %s\n", word2);
			char numberv = 1;
			for (int i = 0; i < 6; ++i) {
				if (strcmp(ohlclist[i], word2) == 0) {
					res2 = data_c[0][i];
					//printf("_%s: %f\n",word2,res2);
					numberv = 0;
					break;
				}
			}
			if (numberv) {sscanf(word2, "%lf", &res2);//printf("numberv res2: %f\n",res2);
			}
		}
		if (m3==2) {
			//printf("word3: %s %d\n", word3f,param3);
			for (int i = 0; i < 4; ++i) {
				if (strcmp(functionsTAlist[i], word3f) == 0) {
					res3 = functionsTA[i](data_c, col, param3);
					//printf("_res3: %f\n",res3);
					break;
				}
			}
		} else {
			//printf("word3: %s\n", word3);
			char numberv = 1;
			for (int i = 0; i < 6; ++i) {
				if (strcmp(ohlclist[i], word3) == 0) {
					res3 = data_c[0][i];
					//printf("_%s: %f\n",word3,res3);
					numberv = 0;
					break;
				}
			}
			if (numberv) {sscanf(word3, "%lf", &res3);//printf("numberv res3: %f\n",res3);
			}
		}
		//printf("operator1: %c\n", operator1);
		//printf("operator2: %c\n", operator2);

		if	  (operator1 == GT) {if(res1 > res2){result = TRUE;} else {result = FALSE;}}
		else if (operator1 == LT) {if(res1 < res2){result = TRUE;} else {result = FALSE;}}
		else if (operator1 == ET) {if(res1 == res2){result = TRUE;} else {result = FALSE;}}
		else {result = FALSE;}

		if	  (operator2 == GT) {if(res2 > res3){result2 = TRUE;} else {result2 = FALSE;}}
		else if (operator2 == LT) {if(res2 < res3){result2 = TRUE;} else {result2 = FALSE;}}
		else if (operator2 == ET) {if(res2 == res3){result2 = TRUE;} else {result2 = FALSE;}}
		else {result2 = FALSE;}

		result = result && result2;
		//if (result==TRUE) {printf("TRUE\n");} else {printf("FALSE\n");}
	}

	if (matched == 3) {
		return Py_BuildValue("bdd", result, res1, res2);
	} else if (matched == 5) {
		return Py_BuildValue("bddd", result, res1, res2, res3);
	} else {
		return Py_BuildValue("i", -1);
	}
	/*
	if (matched == 3 || matched == 5) {
		return Py_BuildValue("b", result);
	} else {
		return Py_BuildValue("i", -1);
	}
	*/
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
