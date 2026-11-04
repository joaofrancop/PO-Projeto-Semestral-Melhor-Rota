# Git só neste projeto (conta joaofrancop)

A identidade global do PC (conta Yellow / joaoyellowmind) **nao e alterada**. Apenas este repositorio tem `user.name` e `user.email` locais.

Antes de `git push` nesta pasta, ative a conta correta no GitHub CLI:

```powershell
gh auth switch -u joaofrancop
```

Commits feitos aqui aparecem como **joaofrancop** no GitHub. Outros repositorios continuam com a configuracao global do computador.

Ver configuracao local:

```powershell
git config --local --list
```
