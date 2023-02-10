FROM ubuntu:22.04

MAINTAINER jozo <hi@jozo.io>

ENV DEBIAN_FRONTEND=noninteractive
ENV QT_DEBUG_PLUGINS=1
ENV DISPLAY=:0.0
# Add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip
RUN pip install --upgrade pip
ENV QT_QUICK_BACKEND=software

# Install additional PyQt5 packages
RUN apt-get update && apt-get install -y \
    libxcb-xinerama0\
    python3-pyqt5.qtopengl \
    python3-pyqt5.qtquick \
    python3-pyqt5.qtmultimedia \
    # Install Qml
    qmlscene \
    qml-module-qtqml* \
    qml-module-qtquick* \
    qml-module-qmltermwidget \
    qml-module-qt-websockets \
    qml-module-qt3d \
    qml-module-qtaudioengine \
    qml-module-qtav \
    qml-module-qtbluetooth \
    qml-module-qtcharts \
    qml-module-qtdatavisualization \
    qml-module-qtgraphicaleffects \
    qml-module-qtgstreamer \
    qml-module-qtlocation \
    qml-module-qtmultimedia \
    qml-module-qtpositioning \
    # Libraries for multimedia
    libqt5multimedia5-plugins \
    gstreamer1.0-libav \
    gstreamer1.0-alsa \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    alsa-base \
    alsa-utils
# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5

COPY mnelab /tmp/src
RUN pip install -r /tmp/src/requirements.txt