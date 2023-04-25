{ pkgs ? import <nixpkgs> {} }:
let
  packages = ps: with ps; [
    numpy
    matplotlib
    pygame
    (
      buildPythonPackage rec {
        pname = "perlin_noise";
        version = "1.12";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-AexC2fK8M4rlLtuwabN1+4P+xReE4XR5NmztH3BjlXw=";
        };
        doCheck = false;
      }
    )
    (
      buildPythonPackage rec {
        pname = "easing_functions";
        version = "1.0.4";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-4Yx5MdRFuF8oxNFa0Kmke7ZdTi7vwNs4QESPriXj+d4=";
        };
        doCheck = false;
        #propagatedBuildInputs = [
        #];
      }
    )
  ];
  python = pkgs.python3.withPackages packages;
in pkgs.mkShell {
  buildInputs = [ python ];
}
