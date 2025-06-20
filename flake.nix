{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      checks = forAllSystems (system: {
        pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            check-added-large-files.enable = true;
            typos.enable = true;
            check-yaml.enable = true;
            convco.enable = true;
            end-of-file-fixer.enable = true;
            fix-byte-order-marker.enable = true;
            ruff-format.enable = true;
            ruff.enable = true;
            trim-trailing-whitespace.enable = true;
            mypy = {
              enable = true;
              stages = [ "pre-push" ];
              entry = "sh -c 'cd ./collector && source .venv/bin/activate && exec mypy .'";
            };
            ty = {
              enable = true;
              name = "ty check";
              entry = "sh -c 'cd ./collector && uvx ty check'";
              types = [ "python" ];
            };
            trufflehog = {
              enable = true;
              stages = [ "pre-push" ];
            };
          };
        };
      });

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = nixpkgs.legacyPackages.${system}.mkShell {
            inherit (self.checks.${system}.pre-commit-check) shellHook;
            buildInputs = self.checks.${system}.pre-commit-check.enabledPackages ++ [
              pkgs.python3
              pkgs.uv
            ];
          };
        }
      );
    };
}
