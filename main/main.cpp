#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QWindow>
#include <QIcon>
#include <QLocale>
#include <QtWebEngine/qtwebengineglobal.h>
#include <QDebug>
#include <QLibraryInfo>

#include "pythonloader.h"

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    qDebug() << "library paths" << app.libraryPaths();
    QQmlApplicationEngine engine;
    engine.addImportPath("libview");

    // We must set the locale always to C as some tools won't work correctly without it.
    // e.g. decimal points will always be "." this way.
    QLocale::setDefault(QLocale::c());

    qDebug() << "QLibrary" << QLibraryInfo::location(QLibraryInfo::LibraryExecutablesPath);
    qDebug() << "QLibraryPrefix" << QLibraryInfo::location(QLibraryInfo::PrefixPath);
    qDebug() << "QLibraryLocation" << QLibraryInfo::location(QLibraryInfo::LibrariesPath);
    QtWebEngine::initialize();

    PythonLoader pythonLoader{&app};
    QObject* dice = pythonLoader.getObject("dice.main", "Dice");
    if (!dice) {
        qDebug() << "Could not initialize the python core!";
        return -1;
    }

    QQmlContext* context = engine.rootContext();

    QVariant vEngine, vContext;
    vEngine.setValue(&engine);
    vContext.setValue(context);
    dice->setProperty("qmlEngine", vEngine);
    dice->setProperty("qmlContext", vContext);

    context->setContextProperty("dice", dice);
    engine.load(QUrl("libview/Window/main.qml"));
    app.topLevelWindows().first()->setIcon(QIcon("libview/Window/images/dice_logo_grey.svg"));
    return app.exec();
}
