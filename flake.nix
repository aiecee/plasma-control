{
  description = "plasma-control";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
  };

  outputs = { self, nixpkgs }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs;
            [
              ruff
              # python packages
              (python311.withPackages (ps: with ps;
              let
                inherit (pkgs.python311.pkgs) buildPythonPackage fetchPypi;
                adafruitPackage = { pname, version, sha256 }: buildPythonPackage {
                  inherit pname version;
                  doCheck = false;
                  pyproject = true;
                  src = fetchPypi {
                    inherit pname version sha256;
                  };
                  nativeBuildInputs = [
                    setuptools-scm
                  ];
                };
                pixelbuf = adafruitPackage {
                  pname = "adafruit-circuitpython-pixelbuf";
                  version = "2.0.4";
                  sha256 = "sha256-vRJ4tg2CgVos3zNDKTGeUF93zFuYJ4hZ1OcGyX8N3tY=";
                };
                ticks = adafruitPackage {
                  pname = "adafruit-circuitpython-ticks";
                  version = "1.0.13";
                  sha256 = "sha256-2FCc5N9HBeOllrtFenEBSt0uN6++ugy9akCzstp2B9g=";
                };
                asyncio = adafruitPackage {
                  pname = "adafruit-circuitpython-asyncio";
                  version = "1.3.0";
                  sha256 = "sha256-hoz46diQaM6XWnv9kLmm/Hz2/NFGIn5AXOeYfoOEBdM=";
                };
                httpserver = adafruitPackage {
                  pname = "adafruit-circuitpython-httpserver";
                  version = "4.5.5";
                  sha256 = "sha256-C2HeBePD/mIpiU3tf6OdkqspEn3FE8MYkFRfCeft5Hc=";
                };
                neopixel = adafruitPackage {
                  pname = "adafruit-circuitpython-neopixel";
                  version = "6.3.11";
                  sha256 = "sha256-x7dpPoe8s1SbxkOUgiwKDyhGxKB2dIxmBZUgMA7GjOs=";
                };
              in
              [
                # editor packages
                python-lsp-server
                pip

                # adafruit
                pixelbuf
                ticks
                asyncio
                httpserver
                neopixel
              ]))
            ];
        };
      });
    };

}
