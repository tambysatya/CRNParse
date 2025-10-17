let
  nixpkgs = import <nixpkgs> { config.allowUnfree = true; };
  lib = nixpkgs.lib;
  pkgs = nixpkgs;

in
pkgs.mkShell {
  buildInputs = [
    pkgs.gcc
    pkgs.stdenv.cc.cc.lib  # ← IMPORTANT : runtime libstdc++ ici
    pkgs.cudaPackages.cuda_cccl.dev
    pkgs.expat
    pkgs.libz
    pkgs.zlib
    pkgs.libsbml
    pkgs.python312
    #pkgs.stdenv.cc.cc.lib
    #pkgs.python312Packages.libsbml
    #pkgs.python312Packages.scipy
    pkgs.python312Packages.pip
    #pkgs.python312Packages.tqdm


    #pkgs.python312Packages.jax
    #pkgs.python312Packages.jaxlib
    #pkgs.python312Packages.torch
    #sympy2jax
    #wadler-lindig
    #diffrax
    pkgs.cudaPackages.cudatoolkit           # ← runtime CUDA (libcudart.so)
    pkgs.cudaPackages_12_2.cudatoolkit
    pkgs.cudaPackages.cudnn                 # ← pour JAX + NN
    pkgs.cudaPackages.cuda_cupti            # ← pour profiling/tracing (optionnel)
  pkgs.cudaPackages_12_2.cudatoolkit
  pkgs.cudaPackages_12_2.cudnn
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
    export LD_LIBRARY_PATH=${pkgs.cudaPackages_12_2.cudatoolkit}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.cudaPackages.cudnn}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.cudaPackages.cuda_cupti}/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/run/opengl-driver/lib:$LD_LIBRARY_PATH


    unset SOURCE_DATE_EPOCH
  '';
}

