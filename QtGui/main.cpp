#include <QGuiApplication>
#include <QQuickView>
//#include "elipseitem.h"

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    //qmlRegisterType<ElipseItem>("Shapes", 1, 0, "Ellipse");

    QQuickView view;

    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.setSource(QUrl("qrc:main.qml"));
    view.show();

    return app.exec();
}
