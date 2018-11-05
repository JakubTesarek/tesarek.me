# Access aliased terminal command

If you use terminal a lot, you know about `~/.bashrc` and `~/.bash_profile` and other files you can use to modify your bash. You probably also know you can create aliases for commands that you use a lot: `alias la="ls -la"`

You can also change default behaviour of some commands, for example add arguments: `alias ls="ls -G"`.

But what if you then want to access the original `ls` without the `-G`. Use uppercased name: `LS`. It seems that `alias` in bash creates alias only for exact match while bash commands are not case sensitive by default. You can as well use `Ls` or `lS`. It's all the same.
