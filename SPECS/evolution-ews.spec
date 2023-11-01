%global libmspack_version 0.4

Name: evolution-ews
Version: 3.28.5
Release: 13%{?dist}
Group: Applications/Productivity
Summary: Evolution extension for Exchange Web Services
License: LGPLv2
URL: https://wiki.gnome.org/Apps/Evolution
Source: http://download.gnome.org/sources/%{name}/3.28/%{name}-%{version}.tar.xz

%global eds_evo_version %{version}

Patch01: evolution-ews-3.28.5-import-event-timezone.patch

# https://gitlab.gnome.org/GNOME/evolution-ews/commit/dc50ba5a50a7b74f1d2710e5f860a7e81ab60d0b
Patch02: evolution-ews-3.28.5-disable-reminder-types.patch

# https://gitlab.gnome.org/GNOME/evolution-ews/commit/6d3dc9c50be654a9e250cfd53626f8526ff9eb70
Patch03: evolution-ews-3.28.5-unknown-responsetype-as-needs-action.patch

# https://gitlab.gnome.org/GNOME/evolution-ews/issues/19
Patch04: evolution-ews-3.28.5-contact-country-forgotten.patch

# https://gitlab.gnome.org/GNOME/evolution-ews/issues/21
Patch05: evolution-ews-3.28.5-meeting-with-attachment.patch

# https://gitlab.gnome.org/GNOME/evolution-ews/commit/f50530ad101b47d461a345ff2b8b295b86c05d3a
Patch06: evolution-ews-3.28.5-double-collection-backend-populate.patch

# RH bug #1696761
Patch07: evolution-ews-3.28.5-cve-2019-3890.patch

# RH bug #1741091
Patch08: evolution-ews-3.28.5-birthday-date.patch

# RH bug #1764818
Patch09: evolution-ews-3.28.5-sync-category-list.patch

# RH bug #1765005
Patch10: evolution-ews-3.28.5-save-only-if-organizer.patch

# RH bug #1886026
Patch11: evolution-ews-3.28.5-oauth2-simplify.patch

# RH bug #1885229
Patch12: evolution-ews-3.28.5-oauth2-endpoints.patch

# RH bug #1972749
Patch13: evolution-ews-3.28.5-cmake-variable-name-comparison.patch

# RH bug #2082245
Patch14: evolution-ews-3.28.5-autodiscover-improvements.patch

Requires: evolution >= %{eds_evo_version}
Requires: evolution-data-server >= %{eds_evo_version}
Requires: %{name}-langpacks = %{version}-%{release}
Requires: libmspack >= %{libmspack_version}

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: intltool
BuildRequires: pkgconfig(camel-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(evolution-data-server-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(evolution-mail-3.0) >= %{eds_evo_version}
BuildRequires: pkgconfig(evolution-shell-3.0) >= %{eds_evo_version}
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libebackend-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(libebook-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(libecal-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(libedata-book-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(libedata-cal-1.2) >= %{eds_evo_version}
BuildRequires: pkgconfig(libemail-engine) >= %{eds_evo_version}
BuildRequires: pkgconfig(libical)
BuildRequires: pkgconfig(libmspack) >= %{libmspack_version}
BuildRequires: pkgconfig(libsoup-2.4)

%description
This package allows Evolution to interact with Microsoft Exchange servers,
versions 2007 and later, through its Exchange Web Services (EWS) interface.

%package langpacks
Summary: Translations for %{name}
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description langpacks
This package contains translations for %{name}.

%prep
%setup -q

%patch01 -p1 -b .import-event-timezone
%patch02 -p1 -b .disable-reminder-types
%patch03 -p1 -b .unknown-responsetype-as-needs-action
%patch04 -p1 -b .contact-country-forgotten
%patch05 -p1 -b .meeting-with-attachment
%patch06 -p1 -b .double-collection-backend-populate
%patch07 -p1 -b .cve-2019-3890
%patch08 -p1 -b .birthday-date
%patch09 -p1 -b .sync-category-list
%patch10 -p1 -b .save-only-if-organizer
%patch11 -p1 -b .oauth2-simplify
%patch12 -p1 -b .oauth2-endpoints
%patch13 -p1 -b .cmake-variable-name-comparison
%patch14 -p1 -b .autodiscover-improvements

%build

mkdir _build
cd _build

export CFLAGS="$RPM_OPT_FLAGS -Wno-deprecated-declarations"
%cmake -G "Unix Makefiles" ..
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

cd _build
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%doc NEWS README
%{_libdir}/evolution/modules/module-ews-configuration.so
%{_libdir}/evolution-data-server/camel-providers/libcamelews.so
%{_libdir}/evolution-data-server/camel-providers/libcamelews.urls
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendews.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendews.so
%{_libdir}/evolution-data-server/registry-modules/module-ews-backend.so
%{_libdir}/evolution-ews/libcamelews-priv.so
%{_libdir}/evolution-ews/libevolution-ews.so
%{_datadir}/metainfo/org.gnome.Evolution-ews.metainfo.xml
%{_datadir}/evolution/errors/module-ews-configuration.error
%{_datadir}/evolution-data-server/ews/windowsZones.xml

%files langpacks -f _build/%{name}.lang

%changelog
* Fri May 06 2022 Milan Crha <mcrha@redhat.com> - 3.28.5-13
- Related: #2082245 (Fix issues in the patch found by Coverity scan)

* Fri May 06 2022 Milan Crha <mcrha@redhat.com> - 3.28.5-12
- Resolves: #2082245 (Backport fixes to improve autodiscovery)

* Wed Jun 16 2021 Milan Crha <mcrha@redhat.com> - 3.28.5-11
- Resolves: #1972749 (PrintableOptions.cmake: Correct variable name comparison)

* Wed Oct 07 2020 Milan Crha <mcrha@redhat.com> - 3.28.5-10
- Resolves: #1886026 (Simplify OAuth2 for outlook.office365.com server)
- Resolves: #1885229 (Allow change of the Microsoft 365 OAuth2 endpoints)

* Wed Nov 13 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-9
- Remove patch for RH bug #1765005 (Reject creating meetings organized by other users)

* Tue Oct 29 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-8
- Remove patch for RH bug #1765005 (Send meeting change notifications only if being the organizer)

* Thu Oct 24 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-7
- Add patch for RH bug #1764818 (Sync CategoryList with mail Labels)
- Add patch for RH bug #1765005 (Send meeting change notifications only if being the organizer)

* Wed Oct 23 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-6
- Add patch for RH bug #1741091 (Birthday date of Contact depends on system timezone)

* Mon May 27 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-5
- Rebuild with added gating

* Mon Apr 15 2019 Milan Crha <mcrha@redhat.com> - 3.28.5-4
- Add patch for RH bug #1696761 (CVE-2019-3890 - SSL Certificates are not validated)

* Mon Oct 01 2018 Milan Crha <mcrha@redhat.com> - 3.28.5-3
- Add "Enable only Notification reminders in the calendar" upstream fix
- Add "Treat 'Unknown' ResponseType as Needs-Action" upstream fix
- Add "I#19 - Country is forgotten along the way to exchange server" upstream fix
- Add "I#21 - Meeting with attachment cannot be saved in 2010" upstream fix
- Add "Collection backend schedules two 'populate' requests after going online" upstream fix

* Tue Sep 04 2018 Milan Crha <mcrha@redhat.com> - 3.28.5-2
- Add patch for RH bug #1625162 (Calendar invites added with the wrong time zone)

* Mon Jul 30 2018 Milan Crha <mcrha@redhat.com> - 3.28.5-1
- Update to 3.28.5

* Mon Jul 16 2018 Milan Crha <mcrha@redhat.com> - 3.28.4-1
- Update to 3.28.4

* Mon Jun 18 2018 Milan Crha <mcrha@redhat.com> - 3.28.3-1
- Update to 3.28.3

* Mon Apr 09 2018 Milan Crha <mcrha@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Milan Crha <mcrha@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Milan Crha <mcrha@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Mon Feb 19 2018 Milan Crha <mcrha@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Tue Feb 06 2018 Milan Crha <mcrha@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Mon Jan 08 2018 Milan Crha <mcrha@redhat.com> - 3.27.4-1
- Update to 3.27.4

* Mon Dec 11 2017 Milan Crha <mcrha@redhat.com> - 3.27.3-1
- Update to 3.27.3

* Mon Nov 13 2017 Milan Crha <mcrha@redhat.com> - 3.27.2-1
- Update to 3.27.2

* Wed Nov 08 2017 Milan Crha <mcrha@redhat.com> - 3.27.1-2
- Rebuild for newer libical

* Mon Oct 16 2017 Milan Crha <mcrha@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Mon Oct 02 2017 Milan Crha <mcrha@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Milan Crha <mcrha@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Mon Sep 04 2017 Milan Crha <mcrha@redhat.com> - 3.25.92.2-1
- Update to 3.25.92.2

* Mon Sep 04 2017 Milan Crha <mcrha@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Tue Aug 22 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.25.91-2
- Install COPYING as %%license

* Mon Aug 21 2017 Milan Crha <mcrha@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Mon Aug 07 2017 Milan Crha <mcrha@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 3.25.4-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Milan Crha <mcrha@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Mon Jun 19 2017 Milan Crha <mcrha@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Mon May 22 2017 Milan Crha <mcrha@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Thu Apr 27 2017 Milan Crha <mcrha@redhat.com> - 3.25.1-2
- Split translations into separate package

* Mon Apr 24 2017 Milan Crha <mcrha@redhat.com> - 3.25.1-1
- Update to 3.25.1

* Mon Apr 10 2017 Milan Crha <mcrha@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Milan Crha <mcrha@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Mon Mar 13 2017 Milan Crha <mcrha@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Milan Crha <mcrha@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 13 2017 Milan Crha <mcrha@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Milan Crha <mcrha@redhat.com> - 3.23.4-1
- Update to 3.23.4

* Mon Dec 12 2016 Milan Crha <mcrha@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Mon Nov 21 2016 Milan Crha <mcrha@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Mon Oct 24 2016 Milan Crha <mcrha@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Mon Oct 10 2016 Milan Crha <mcrha@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Milan Crha <mcrha@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Sep 12 2016 Milan Crha <mcrha@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Mon Aug 29 2016 Milan Crha <mcrha@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Mon Aug 15 2016 Milan Crha <mcrha@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Mon Jul 18 2016 Milan Crha <mcrha@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Mon Jun 20 2016 Milan Crha <mcrha@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Mon May 23 2016 Milan Crha <mcrha@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Mon Apr 25 2016 Milan Crha <mcrha@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Mon Apr 11 2016 Milan Crha <mcrha@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Mon Mar 21 2016 Milan Crha <mcrha@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Mar 14 2016 Milan Crha <mcrha@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Mon Feb 29 2016 Milan Crha <mcrha@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 15 2016 Milan Crha <mcrha@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 David Tardon <dtardon@redhat.com> - 3.19.4-2
- rebuild for libical 2.0.0

* Mon Jan 18 2016 Milan Crha <mcrha@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Mon Dec 14 2015 Milan Crha <mcrha@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Mon Nov 23 2015 Milan Crha <mcrha@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Mon Oct 26 2015 Milan Crha <mcrha@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Mon Oct 12 2015 Milan Crha <mcrha@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Milan Crha <mcrha@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Mon Sep 14 2015 Milan Crha <mcrha@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Mon Aug 31 2015 Milan Crha <mcrha@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Mon Aug 17 2015 Milan Crha <mcrha@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Mon Jul 20 2015 Milan Crha <mcrha@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Mon Jun 22 2015 Milan Crha <mcrha@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Milan Crha <mcrha@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Mon Apr 27 2015 Milan Crha <mcrha@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Mon Apr 13 2015 Milan Crha <mcrha@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Milan Crha <mcrha@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Milan Crha <mcrha@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Mon Mar 02 2015 Milan Crha <mcrha@redhat.com> - 3.15.91-1
- Update to 3.15.91

* Mon Feb 16 2015 Milan Crha <mcrha@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Mon Jan 26 2015 Milan Crha <mcrha@redhat.com> - 3.13.10-1
- Update to 3.13.10

* Mon Dec 22 2014 Milan Crha <mcrha@redhat.com> - 3.13.9-1
- Update to 3.13.9

* Mon Nov 24 2014 Milan Crha <mcrha@redhat.com> - 3.13.8-1
- Update to 3.13.8

* Mon Oct 27 2014 Milan Crha <mcrha@redhat.com> - 3.13.7-1
- Update to 3.13.7

* Mon Sep 22 2014 Milan Crha <mcrha@redhat.com> - 3.13.6-1
- Update to 3.13.6

* Mon Aug 25 2014 Milan Crha <mcrha@redhat.com> - 3.13.5-1
- Update to 3.13.5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Milan Crha <mcrha@redhat.com> - 3.13.4-1
- Update to 3.13.4

* Mon Jul 14 2014 Milan Crha <mcrha@redhat.com> - 3.12.4-1
- Update to 3.12.4

* Mon Jun 09 2014 Milan Crha <mcrha@redhat.com> - 3.12.3-1
- Update to 3.12.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Milan Crha <mcrha@redhat.com> - 3.12.2-1
- Update to 3.12.2

* Mon Apr 14 2014 Milan Crha <mcrha@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Milan Crha <mcrha@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Mon Mar 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Mon Mar 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Mon Feb 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Mon Jan 13 2014 Milan Crha <mcrha@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Sun Dec 01 2013 Matthew Barnes <mbarnes@redhat.com> - 3.11.2-3
- Add $RPM_OPT_FLAGS to $CFLAGS (RH bug #1035930)

* Thu Nov 21 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-2
- Rebuild for new libical (RH bug #1023020)

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-1
- Update to 3.11.2
- Disable compiler warnings about deprecated symbols

* Tue Oct 22 2013 Matthew Barnes <mbarnes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Mon Sep 23 2013 Milan Crha <mcrha@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Mon Sep 16 2013 Milan Crha <mcrha@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Mon Sep 02 2013 Milan Crha <mcrha@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Mon Aug 19 2013 Milan Crha <mcrha@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Mon Jul 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Mon Jul 08 2013 Milan Crha <mcrha@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Mon Jun 17 2013 Milan Crha <mcrha@redhat.com> - 3.9.3-1
- Update to 3.9.3
- Add dependency on libmspack 0.4+

* Mon May 27 2013 Milan Crha <mcrha@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Sat May 25 2013 Rex Dieter <rdieter@fedoraproject.org> 3.9.1-2
- rebuild (libical)

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Mon Mar 25 2013 Milan Crha <mcrha@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Mon Feb 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Matthew Barnes <mbarnes@redhat.com> - 3.7.3.1-1
- Update to 3.7.3.1

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Mon Oct 22 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Mon Sep 17 2012 Milan Crha <mcrha@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Mon Sep 03 2012 Milan Crha <mcrha@redhat.com> - 3.5.91-1
- Update to 3.5.91
- Remove patch for new xmlOutputBuffer API (fixed upstream)

* Mon Aug 20 2012 Milan Crha <mcrha@redhat.com> - 3.5.90-1
- Update to 3.5.90
- Add patch for new xmlOutputBuffer API

* Mon Aug 06 2012 Milan Crha <mcrha@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Mon Jun 04 2012 Milan Crha <mcrha@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Sun Apr 29 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Mon Mar 26 2012 Milan Crha <mcrha@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Mon Mar 19 2012 Milan Crha <mcrha@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Tue Mar 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Mon Feb 20 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Mon Feb 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Mon Jan 16 2012 Milan Crha <mcrha@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Milan Crha <mcrha@redhat.com> - 3.3.3-1
- Update to 3.3.3
- Removed the last patch (fixed upstream)

* Mon Nov 21 2011 Milan Crha <mcrha@redhat.com> - 3.3.2-1
- Update to 3.3.2
- Removed obsolete patches (fixed upstream)

* Mon Nov 07 2011 Matthew Barnes <mbarnes@redhat.com> - 3.3.1-1
- Initial packaging for Fedora 17.
