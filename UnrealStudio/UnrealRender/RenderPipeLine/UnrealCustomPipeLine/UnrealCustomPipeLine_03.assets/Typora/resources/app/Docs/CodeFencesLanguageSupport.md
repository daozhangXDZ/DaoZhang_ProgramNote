# Code Fences Language Support

The latest version of Typora support syntax highlight of following languages (in lower case):

- asp (alias: aspx, asp.net)
- javascript (alias: js, text/javascript)
- json
- typescript
- clojure
- coffeescript (alias: coffee)
- css
- less
- scss
- gfm (github flavored markdown)
- markdown
- xml
- haskell
- html (alias: htmlmixed)
- lua
- commonlisp (alias: lisp)
- pascal
- perl
- php (and php+html)
- cython
- python
- ruby
- shell (alias: sh, bash)
- sql
- sqlite
- mssql
- mysql
- mariadb
- cql (alias: cassandra)
- plsql
- tex (and stex, latex)
- tiddlywiki (alias: wiki)
- vb (alias: basic)
- vbscript
- velocity
- verilog
- xquery
- yaml
- go
- groovy
- nginx
- octave (alias: matlab)
- oz
- c (alias: clike)
- c++ (alias: cpp, cc)
- objective-c (alias: obj-c, objc)
- scala
- c# (alias: csharp)
- java
- squirrel
- ceylon
- kotlin
- swift
- r (alias: rlang, r-lang)
- d
- diff
- erlang
- http
- jade
- rst (alias: restructuredtext)
- rust
- jinja2
- jsp
- erb
- embeddedjs (alias: ejs)
- powershell
- dockerfile
- jsx (alias: react)
- vue (alias: vue.js, vue-template)
- nsis
- tiki (alias: tikiwiki, tiki-wiki)
- properties (alias: ini)
- livescript
- assembly (alias: asm, nasm, gas)
- toml
- ocaml
- F#
- elm
- elixir
- spreadsheet
- pgp (alias: asciiarmor, pgp-keys)
- cmake
- cypher
- dart
- django
- dtd (alias: xml-dtd)
- dylan
- handlebars
- idl
- web-idl
- yacas
- mbox
- bhdl
- julia
- haxe
- hxml
- pseudocode
- SAS
- twig
- scheme
- tcl
- makefile
- protobuf
- fortran
- COBOL

Please note that the language you specific in <code>```{lang}</code> is case insensitive for typora when choose the corresponding syntax highlight.


### My language is not listed above...

Typora use CodeMirror for code fences with syntax highlight, so, if the language you want is not supported in Typora, you could:

1. Check whether the language is support on <http://codemirror.net/mode/> or not, if so, send us an email, and we will add related support.
2. If the language is not supported on <http://codemirror.net/mode/>, please check <https://github.com/codemirror/CodeMirror/wiki/Mode-wish-list> for adding syntax highlight on CodeMirror. After it is supported by CodeMirror, Typora will follow.