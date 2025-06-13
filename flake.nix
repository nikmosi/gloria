{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
    devenv.url = "github:cachix/devenv";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs =
    {
      self,
      nixpkgs,
      devenv,
      ...
    }@inputs:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      checks = {
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
      };

      devShells.${system} = {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            (
              { pkgs, config, ... }:
              {
                # This is your devenv configuration
                packages =
                  [ pkgs.hello ]
                  ++ self.checks.pre-commit-check.enabledPackages
                  ++ [
                    pkgs.python3
                    pkgs.uv
                  ];

                enterShell = ''
                  ${self.checks.pre-commit-check.shellHook}
                  exec ${pkgs.nushell}/bin/nu
                  hello
                '';

                processes.run.exec = "hello";
              }
            )
          ];
        };
      };
    };
}
