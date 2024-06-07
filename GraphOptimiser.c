#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <stdio.h>
#include <Python.h>
#include <../Lib/site-packages/numpy/core/include/numpy/arrayobject.h>


int8_t CONSISTENT_ADJACENCY_ARRAY[44][6] = {
    {-1, -1, -1, -1, -1, -1},  // Empty list for territory ID 0 (assuming territory IDs start from 1)
    {43,  3,  5,  4, -1, -1},
    {-1, -1, -1, -1, -1, -1},  // Empty list for territory ID 2
    {14,  6,  5,  1, -1, -1},
    {43,  1,  5,  7, -1, -1},
    { 1,  3,  6,  7,  8,  4},
    { 3,  5,  8, -1, -1, -1},
    { 8,  5,  4,  9, -1, -1},
    { 5,  6,  7,  9, -1, -1},
    { 7,  8, 10, -1, -1, -1},
    { 9, 11, 12, -1, -1, -1},
    {10, 12, 13, 21, -1, -1},
    {10, 11, 13, -1, -1, -1},
    {11, 12, -1, -1, -1, -1},
    { 3, 15, 16, -1, -1, -1},
    {14, 16, 17, 20, -1, -1},
    {14, 15, 17, 18, -1, -1},
    {16, 15, 20, 19, 18, -1},
    {16, 17, 19, 21, -1, -1},
    {17, 18, 20, 21, 22, 35},
    {15, 17, 19, 27, 31, 35},
    {18, 19, 22, 23, 24, 11},
    {19, 21, 35, 23, -1, -1},
    {21, 22, 35, 24, 25, 26},
    {21, 23, 25, -1, -1, -1},
    {24, 23, 26, -1, -1, -1},
    {23, 25, -1, -1, -1, -1},
    {20, 31, 37, 28, -1, -1},
    {27, 37, 33, 32, 29, -1},
    {28, 32, 30, -1, -1, -1},
    {29, 32, 34, 43, -1, -1},
    {27, 37, 36, 35, 20,  0},
    {29, 30, 34, 33, 28,  0},
    {28, 32, 34, 37, -1, -1},
    {33, 32, 30, -1, -1, -1},
    {31, 36, 22, 23, 19, 20},
    {35, 38, 37, 31, -1, -1},
    {38, 36, 33, 31, 27, 28},
    {37, 36, 39, -1, -1, -1},
    {40, 41, 38, -1, -1, -1},
    {39, 41, 42, -1, -1, -1},
    {39, 42, 40, -1, -1, -1},
    {41, 40, -1, -1, -1, -1},
    {30,  1,  4, -1, -1, -1}
};

// for territory in player_territories:
    //     adjacent_territories = adjacent_array[territory]
    //     enemy_adjacent_territories = []
    //     for adjacent_territory in adjacent_territories:
    //         if adjacent_territory not in player_territories:
    //             enemy_adjacent_territories.append(adjacent_territory)
    //     adjacent_array[territory] = enemy_adjacent_territories

PyObject* get_enemy_adjacent_territories(int* personal_territory_arr, int num_personal_territories) {
    PyObject* result = PyDict_New();
    
    for (int i = 0; i < num_personal_territories; i = i + 1) {
        int territoryID = personal_territory_arr[i];
        int8_t* adjacent_territories = CONSISTENT_ADJACENCY_ARRAY[territoryID];
        
        PyObject* enemy_adjacent_list = PyList_New(0);
        
        for (int j = 0; j < 6; j = j + 1) {
            int adjacent_territory = adjacent_territories[j];
            if (adjacent_territory != -1) {
                int is_enemy = 1;
                for (int k = 0; k < num_personal_territories; k = k + 1) {
                    if (adjacent_territory == personal_territory_arr[k]) {
                        is_enemy = 0;
                        break;
                    }
                }
                if (is_enemy) {
                    PyObject* adjacent_territory_obj = PyLong_FromLong(adjacent_territory);
                    PyList_Append(enemy_adjacent_list, adjacent_territory_obj);
                    Py_DECREF(adjacent_territory_obj);
                }
            }
        }
        
        PyObject* territory_obj = PyLong_FromLong(territoryID);
        PyDict_SetItem(result, territory_obj, enemy_adjacent_list);
        Py_DECREF(territory_obj);
        Py_DECREF(enemy_adjacent_list);
    }
    
    return result;
}


PyObject *get_enemy_adj(PyObject *self, PyObject *args){
    PyArrayObject *player_territories_obj;
    PyArg_ParseTuple(args, "O", &player_territories_obj);
    int* personal_territory_arr;
    int64_t num_personal_territories = PyArray_SIZE(player_territories_obj);
    npy_intp player_territories_dims[] = { [0] = num_personal_territories};
    // Using the PyArray_AsCArray to convert a 1D np_array into a C Array
    // -> I tried using it for a 2D array but it bugged out and I couldn't get it to work
    // -> Worked better than the other Load_data function. 
    PyArray_AsCArray((PyObject**) &player_territories_obj, &personal_territory_arr, player_territories_dims, 1 , PyArray_DescrFromType(NPY_LONG));    
    PyObject* adjacent_territories = get_enemy_adjacent_territories(personal_territory_arr,num_personal_territories);
    return adjacent_territories;
        

}



// gcc add.c -shared -o graphoptimiser.pyd -I"C:\Users\liver\AppData\Local\Programs\Python\Python310\include" -L"C:\Users\liver\AppData\Local\Programs\Python\Python310\libs" -lpython310


static PyMethodDef methods[] = {
    {"get_enemy_adj", get_enemy_adj, METH_VARARGS, "Get all territories adjacent"},
    { NULL, NULL, 0, NULL}
};

static struct PyModuleDef graphoptimiser = {
    PyModuleDef_HEAD_INIT,
    "graphoptimiser",
    "This is a module named graphoptimiser, designed for optimising the graph calculations in the risk module",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_graphoptimiser(){
    printf("Connected - Diarmuid");
    
    PyObject *module = PyModule_Create(&graphoptimiser); 
    import_array();
    return module;

}
