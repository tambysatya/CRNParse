let
  nixpkgs = import <nixpkgs> { config.allowUnfree = true; };
  lib = nixpkgs.lib;
  pkgs = nixpkgs;

in
pkgs.mkShell {
  buildInputs = [
    pkgs.gcc
    pkgs.stdenv.cc.cc.lib  # ← IMPORTANT : runtime libstdc++ ici
      ];

  shellHook = ''
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python312.sitePackages}:$PYTHONPATH"
    export PYTHONPATH="CRNTools/:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    export LD_LIBRARY_PATH=${lib.getLib pkgs.gcc}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.expat}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.libz}/lib:$LD_LIBRARY_PATH

    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH


    unset SOURCE_DATE_EPOCH
  '';
}

