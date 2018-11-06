# Access aliased terminal command

If you use terminal a lot, you know about `~/.bashrc` and `~/.bash_profile` and other files you can use to modify your bash. You probably also know you can create aliases for commands that you use a lot: `alias la="ls -la"`

You can also change default behaviour of some commands, for example add arguments: `alias ls="ls -G"`.

But what if you then want to access the original `ls` without the `-G`. Use uppercased name: `LS`. It seems that `alias` in bash creates alias only for exact match while bash commands are not case sensitive by default. You can as well use `Ls` or `lS`. It's all the same.

> Erratum: I was [informed on twitter](https://twitter.com/JanTvrdik/status/1059468717749350400) that my "solution" works only on case-insensitive and case-preserving systems, like Mac. On case-sensitive systems this doesn't work. You can instead [use backslash before a command](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_03_01): `\ls`
