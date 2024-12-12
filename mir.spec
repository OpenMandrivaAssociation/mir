# Force out of source build
%undefine __cmake_in_source_build

# Disable ctest run by default
# They take a long time and are generally broken in the build environment
%bcond_with run_tests

%define libname %mklibname mir
%define liblomiriname %mklibname mir-lomiri
%define libservername %mklibname mir-server
%define devname %mklibname -d mir

Name:           mir
Version:        2.19.2
Release:        4
Summary:        Next generation display server

# mircommon is LGPL-2.1-only/LGPL-3.0-only, everything else is GPL-2.0-only/GPL-3.0-only
License:        (GPL-2.0-only or GPL-3.0-only) and (LGPL-2.1-only or LGPL-3.0-only)
URL:            https://mir-server.io/
Source0:        https://github.com/MirServer/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  git-core
BuildRequires:  cmake, ninja, doxygen, graphviz, lcov
#gcovr
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  boost-devel
BuildRequires:  python
BuildRequires:  glm-devel
BuildRequires:  pkgconfig(libglog)
BuildRequires:  pkgconfig(lttng-ust)
BuildRequires:  systemtap-devel
BuildRequires:  pkgconfig(gflags)
BuildRequires:  python-pillow
BuildRequires:	pkgconfig(gmpxx)
# Everything detected via pkgconfig
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gbm) >= 9.0.0
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock) >= 1.8.0
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtest) >= 1.8.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml++-2.6)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(umockdev-1.0) >= 0.6
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-eglstream)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(yaml-cpp)
BuildRequires:  pkgconfig(wlcs)

# pkgconfig(egl) is now from glvnd, so we need to manually pull this in for the Mesa specific bits...
BuildRequires:  egl-devel

# For some reason, this doesn't get pulled in automatically into the buildroot
BuildRequires:  atomic-devel

# For detecting the font for CMake
BuildRequires:  fonts-ttf-freefont

# For validating the desktop file for mir-demos
BuildRequires:  %{_bindir}/desktop-file-validate

# Add architectures as verified to work
%ifarch %{ix86} x86_64 %{arm} aarch64
BuildRequires:  valgrind
%endif

%description
Mir is a display server running on linux systems,
with a focus on efficiency, robust operation,
and a well-defined driver model.

%package -n %{devname}
Summary:       Development files for Mir
Requires:      %{libname} = %{EVRD}
Requires:      %{libservername} = %{EVRD}
Requires:      %{liblomiriname} = %{EVRD}
Requires:      %{name}-test-libs-static%{?_isa} = %{EVRD}
Provides:	mir-devel = %{EVRD}

%description -n %{devname}
This package provides the development files to create
applications that can run on Mir.

%package -n %{libname}
Summary:       Common libraries for Mir
License:       LGPL-2.1-only or LGPL-3.0-only
Provides:	mir = %{EVRD}

%description -n %{libname}
This package provides the libraries common to be used
by Mir clients or Mir servers.

%package -n %{liblomiriname}
Summary:       Lomiri compatibility libraries for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{libname} = %{EVRD}
Requires:      %{libservername} = %{EVRD}

%description -n %{liblomiriname}
This package provides the libraries for Lomiri to use Mir
as a Wayland compositor.

%package -n %{libservername}
Summary:       Server libraries for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{libname} = %{EVRD}

%description -n %{libservername}
This package provides the libraries for applications
that use the Mir server.

%package test-tools
Summary:       Testing tools for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{libservername} = %{EVRD}
Recommends:    %{name}-demos
Recommends:    glmark2
Recommends:    xwayland
Requires:      wlcs

%description test-tools
This package provides tools for testing Mir.

%package demos
Summary:       Demonstration applications using Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{libservername} = %{EVRD}
Requires:      hicolor-icon-theme
Recommends:    xwayland
# For some of the demos
Requires:      fonts-ttf-freefont

%description demos
This package provides applications for demonstrating
the capabilities of the Mir display server.

%package test-libs-static
Summary:       Testing framework library for Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{devname} = %{EVRD}

%description test-libs-static
This package provides the static library for building
Mir unit and integration tests.

%package kiosk
Summary:       Kiosk Mir
License:       GPL-2.0-only or GPL-3.0-only
Requires:      %{libservername} = %{EVRD}
Recommends:    %{name}-demos
Recommends:    glmark2
Recommends:    xwayland
Requires:      wlcs

%description kiosk
This package provides tools for testing Mir.


%prep
%autosetup -S git_am

# Drop -Werror
sed -e "s/-Werror//g" -i CMakeLists.txt

%build
%cmake	DMIR_LINK_TIME_OPTIMIZATION=ON} \
	-DMIR_USE_PRECOMPILED_HEADERS=OFF \
	-DCMAKE_INSTALL_LIBEXECDIR="usr/libexec/mir" \
	-DMIR_PLATFORM="gbm-kms;x11;wayland;eglstream-kms"

%make_build

%install
%make_install -C build

%files -n %{devname}
%license COPYING.*
%{_bindir}/mir_wayland_generator
%{_libdir}/libmir*.so
%{_libdir}/pkgconfig/mir*.pc
%{_includedir}/mir*

%files -n %{libname}
%license COPYING.LGPL*
%doc README.md
%{_libdir}/libmircore.so.*
%{_libdir}/libmircommon.so.*
%{_libdir}/libmirplatform.so.*
%dir %{_libdir}/mir

%files -n %{liblomiriname}
%license COPYING.GPL*
%doc README.md
%{_libdir}/libmiroil.so.*

%files -n %{libservername}
%license COPYING.GPL*
%doc README.md
%{_libdir}/libmiral.so.*
%{_libdir}/libmirserver.so.*
%{_libdir}/libmirwayland.so.*
%dir %{_libdir}/mir/server-platform
%{_libdir}/mir/server-platform/graphics-eglstream-kms.so.*
%{_libdir}/mir/server-platform/graphics-gbm-kms.so.*
%{_libdir}/mir/server-platform/graphics-wayland.so.*
%{_libdir}/mir/server-platform/input-evdev.so.*
%{_libdir}/mir/server-platform/renderer-egl-generic.so.*
%{_libdir}/mir/server-platform/server-virtual.so.*
%{_libdir}/mir/server-platform/server-x11.so.*

%files test-tools
%license COPYING.GPL*
%{_bindir}/mir-*test*
%{_bindir}/mir_*test*
%dir %{_libdir}/mir/tools
%{_libdir}/mir/tools/libmirserverlttng.so
%dir %{_libdir}/mir
%{_libdir}/mir/miral_wlcs_integration.so
%dir %{_libdir}/mir/server-platform
%{_libdir}/mir/server-platform/graphics-dummy.so
%{_libdir}/mir/server-platform/input-stub.so
%{_iconsdir}/hicolor/scalable/apps/spiral-logo.svg

%files test-libs-static
%license COPYING.GPL*
%{_libdir}/libmir-test-assist.a

%files demos
%license COPYING.GPL*
%doc README.md
%{_bindir}/mir_demo_*
%{_bindir}/miral-*
%{_datadir}/applications/miral-shell.desktop

%files kiosk
%{_bindir}/mir-x11-kiosk
%{_bindir}/mir-x11-kiosk-launch
