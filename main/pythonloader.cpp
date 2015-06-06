/*
 * This is based on qmlscene/pluginloader.cpp from PyQt (Copyright (c) 2014 Riverbank Computing Limited <info@riverbankcomputing.com>)
 *
 * This file may be used under the terms of the GNU General Public License
 * version 3.0 as published by the Free Software Foundation and appearing in
 * the file LICENSE included in the packaging of this file.  Please review the
 * following information to ensure the GNU General Public License version 3.0
 * requirements will be met: http://www.gnu.org/copyleft/gpl.html.
 *
 * This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
 * WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 */


#include <stdlib.h>

#include <Python.h>

#include <QCoreApplication>
#include <QDir>
#include <QLibraryInfo>
#include <QVector>
#include <QQmlEngine>
#include <QDebug>

#include "pythonloader.h"

PythonLoader::PythonLoader(QObject *parent) : QObject(parent)
{

    if (!Py_IsInitialized())
    {
        QString sysPath = QCoreApplication::applicationDirPath();
        QString programPath = sysPath + "/thirdparty/Python/bin/python3";
        wchar_t* programName = new wchar_t[programPath.length() + 1];
        programPath.toWCharArray(programName);
        programName[programPath.length()] = 0;

        Py_SetProgramName(programName);
        wprintf(L"python prefix path: %S\n", Py_GetPrefix());
        wprintf(L"python full path: %S\n", Py_GetProgramFullPath());
        Py_Initialize();
        QStringList paths = {sysPath+"/thirdparty/Python/lib/python3.4", sysPath+"/thirdparty/Python/lib/python3.4/plat-linux",
                             sysPath+"/thirdparty/Python/lib/python3.4/lib-dynload", sysPath+"/thirdparty/Python/lib/python3.4/site-packages",
                            sysPath, sysPath+"/thirdparty/Python/lib", sysPath+"/thirdparty/Python/bin"};
        QString wholePath = paths.join(":");
        PySys_SetPath(wholePath.toStdWString().c_str());

        getSipAPI();
        PyEval_InitThreads();
        PyEval_SaveThread();
    }
}


PythonLoader::~PythonLoader()
{
    if (Py_IsInitialized())
    {
        PyGILState_STATE gil = PyGILState_Ensure();

        Py_XDECREF(py_object);

        PyGILState_Release(gil);
    }
}

QObject *PythonLoader::getObject(QString package, QString name)
{
    PyGILState_STATE gil = PyGILState_Ensure();

    PyObject* package_mod = PyImport_ImportModule(package.toLatin1().data());
    if (!package_mod) {
        PyGILState_Release(gil);
        return nullptr;
    }

    PyObject* class_object = PyObject_GetAttrString(package_mod, name.toLatin1().data());
    if (!class_object) {
        Py_DecRef(package_mod);
        PyGILState_Release(gil);
        return nullptr;
    }

    const sipTypeDef *td = sip->api_find_type("QObject");
    PyObject *qSelf = sip->api_convert_from_type(this, td, 0);
    PyObject* argTuple = PyTuple_New(1);
    PyTuple_SetItem(argTuple, 0, qSelf);

    py_object = PyObject_CallObject(class_object, argTuple);
    Q_ASSERT(py_object != nullptr);

    sipSimpleWrapper* wrapper = reinterpret_cast<sipSimpleWrapper*>(py_object);
    QObject* qObject = (QObject*)(wrapper->data);

    Py_DecRef(class_object);
    Py_DecRef(package_mod);
    PyGILState_Release(gil);
    return qObject;
}

void PythonLoader::getSipAPI()
{
    sip = (const sipAPIDef *)PyCapsule_Import("sip._C_API", 0);

    if (!sip)
        PyErr_Print();
}
