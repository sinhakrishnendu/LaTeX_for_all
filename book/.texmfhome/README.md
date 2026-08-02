# Isolated TeX user tree

The build scripts point `TEXMFHOME` to this intentionally minimal directory.
This prevents unrelated user-installed package versions from shadowing the
stable packages supplied by the selected TeX distribution. Project-specific
TeX additions may be placed here if they become necessary.
