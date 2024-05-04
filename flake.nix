{
  description = "Dev environment for the Language Engineering Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/23.11";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      pythonPackages = p: with p; [
          numpy pandas scipy seaborn scikit-learn jupyter matplotlib pip
          django requests django-crispy-forms django-crispy-bootstrap4
          elasticsearch tabulate elastic-transport
        ];
    in {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = with pkgs; [
          (pkgs.python3.withPackages pythonPackages)
        ];
      };
    };
}


