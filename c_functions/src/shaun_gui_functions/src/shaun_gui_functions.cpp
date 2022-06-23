#include <stdio.h>
#include <Python.h>
#include <math.h>

const double radians = 3.141592653589793238 / 180;
// def _move(self, quad, x, y, width, height, rotation):
    // index = self.quads.index(quad)

    // self.vertices[index * 28 : index * 28 + 2] = array("f", [x, y])
    // self.vertices[index * 28 + 7 : index * 28 + 9] = array("f", [x + width, y])
    // self.vertices[index * 28 + 14: index * 28 + 16] = array("f", [x + width, y + height])
    // self.vertices[index * 28 + 21 : index * 28 + 23] = array("f", [x, y + height])
    // self.vertices[index * 28 : index * 28 + 30] = array("f", _quad_rotate_around(rotation, list(self.vertices[index * 28 : index * 28 + 30]), quad.x / 2, quad.y / 2))

static PyObject* _quad_rotate_around(PyObject* self, PyObject* args) {
    const double theta = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 0)) * radians;
    PyObject* vertices = PyTuple_GET_ITEM(args, 1);
    const double pivot_x = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 2));
    const double pivot_y = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 3));

    const double dc = cos(theta);
    const double ds = sin(theta);

    for (int i = 0; i < 4; i++) {
        double x_minus_pivot = PyFloat_AsDouble(PyList_GetItem (vertices, i * 7)) - pivot_x;
        PyList_SetItem(vertices, i * 7, PyFloat_FromDouble(x_minus_pivot));

        double y_minus_pivot = PyFloat_AsDouble(PyList_GetItem (vertices, i * 7 + 1)) - pivot_y;
        PyList_SetItem(vertices, i * 7 + 1, PyFloat_FromDouble(y_minus_pivot));
        
        double y = PyFloat_AsDouble(PyList_GetItem (vertices, i * 7 + 1));
        double x = PyFloat_AsDouble(PyList_GetItem (vertices, i * 7));

        PyList_SetItem(vertices, i * 7, Py_BuildValue("d", (dc * x - ds * y) + pivot_x));
        PyList_SetItem(vertices, i * 7 + 1, Py_BuildValue("d", (ds * x + dc * y) + pivot_y));
    };
    Py_INCREF(vertices);
    return vertices;
};

static PyObject* _quad_move(PyObject* self, PyObject* args) {
    const double x = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 0));
    const double y = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 1));
    const double width = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 2));
    const double height = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 3));
    PyObject* vertices = PyTuple_GET_ITEM(args, 4);
    const double rotation = PyFloat_AsDouble(PyTuple_GET_ITEM(args, 5));

    PyList_SetItem(vertices, 0, PyFloat_FromDouble(x));
    PyList_SetItem(vertices, 1, PyFloat_FromDouble(y));
    PyList_SetItem(vertices, 7, PyFloat_FromDouble(x + width));
    PyList_SetItem(vertices, 8, PyFloat_FromDouble(y));
    PyList_SetItem(vertices, 14, PyFloat_FromDouble(x + width));
    PyList_SetItem(vertices, 15, PyFloat_FromDouble(y + height));
    PyList_SetItem(vertices, 21, PyFloat_FromDouble(x));
    PyList_SetItem(vertices, 22, PyFloat_FromDouble(y + height));

    PyObject *rotate_args = Py_BuildValue("(dOdd)", 
        rotation,
        vertices,
        x + (width * 0.5),
        y + (height * 0.5));

    vertices = _quad_rotate_around(self, rotate_args);
    Py_DECREF(rotate_args);

    return vertices;
};

// Method definition objectPyTuple_Pack(4, Py_BuildValue("d", rotation), vertices, Py_BuildValue("d",width/2), Py_BuildValue("d",height/2)) for this extension, these argumens mean:
static PyMethodDef hello_methods[] = {  
    {
        "_quad_rotate_around", _quad_rotate_around, METH_VARARGS,
        "Rotation around a point for the quad"
    },
    {
        "_quad_move", _quad_move, METH_VARARGS,
        "Moves quad" 
    },
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef hello_definition = {
    PyModuleDef_HEAD_INIT,
    "hello",
    "A Python module that prints 'hello world' from C code.",
    -1,
    hello_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_shaun_gui_functions(void) {
    Py_Initialize();
    return PyModule_Create(&hello_definition);
}