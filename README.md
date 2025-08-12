# RPM-build

```bash
mock -r alma+epel-10-x86_64_v2 --resultdir ./build --sources ~/rpmbuild/SOURCES/ --buildsrpm --spec SPEC_FILE
mock -r alma+epel-10-x86_64_v2 --resultdir ./build ./build/SRPM_FILE
```