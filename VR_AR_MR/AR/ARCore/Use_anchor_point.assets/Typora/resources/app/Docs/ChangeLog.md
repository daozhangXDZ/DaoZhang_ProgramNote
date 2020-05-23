> **Notice**: We will end support for Linux 32bit soon.

## 0.9.70 (beta)

20, Apr

1. Fix wrong cursor position calculation logic on lines contain emoji.
2. Fix quote auto pair issue.

## 0.9.69 (beta)

19, Apr

1. Fix security bug on export and editing.
2. Add ASN.1 syntax highlight support.
3. Fix no default theme is loaded on first launch.
4. Improve copy & paste logic.
5. Improve search function, now search will not ignore whitespace.
6. Add error message for flowchart when rendering failed.
7. Fix image operations, support `align` attribute for `img` tag.
8. Fix emoji auto complete.
9. Fix bug that math not rendered on open sometimes, fix cursor issues relates to inline math.
10. Other bug fix.

## 0.9.68 (beta)

20, Mar, 2019

1. Fix security issues.
2. Fix regression bug on side bar, edit, images, links related functions.
3. Add syntax highlight for SPARQL and Crystal.

## 0.9.67 (beta)

16, Mar, 2019

1. Fix export HTML not working.
2. Improve Pandoc version detect logic.

## 0.9.66 (beta)

15, Mar, 2019

[Detail](https://support.typora.io/What's-New-0.9.66/)

1. Fix security issues.
2. Fix unnecessary escape in outline.
3. Fix click outline will cause content jumping.
4. Fix hide status bar not working.
5. Add language Vietnamese by [1234hdpa](https://github.com/1234hdpa).
6. Remove options for emoji autocomplete, it is now enabled by default.
7. Update flowchart library and fix issues related to flowchart.
8. Add options to configure reading speed.
9. Add `oz` ad supported language for syntax highlight.
10. Other bug fix.

## 0.9.65 (beta)

18, Feb, 2019

1. Save last chosen encodings for file.
2. Add Indonesia language support by [snatalius](https://github.com/snatalius).
3. Allow drag & drop to insert file links quickly.
4. Fix XSS for inline math, add security check for area tag.
5. Fix math block rendering issue.
6. Fix footnotes numbering on export.
7. Improve compatibility on Linux OS.
8. Other bug fix.

## 0.9.64 (beta)

25, Jan, 2019

1. Fix an XSS issue.
2. Fix word count in selection in word count panel.

## 0.9.63 (beta)

25, Jan, 2019

[Detail](https://support.typora.io/What's-New-0.9.63/)

1. Improve open quickly.
2. Support “Copy without Theme Styling”.
3. Add recent folders in jump list.
4. Show full path on file tree when hover on items.
5. Improved Japanese and Hrvatski translation.
6. Fix bugs on parsing Markdown content.
7. Improve math support and update to mhchem 3.3 for Chemistry support.
8. Fix button actions and links for spellcheck panel.
9. Add basic context menu in source code mode.
10. Fix bugs cursor jump when input block quotes or task lists.
11. Other bug fix.

## 0.9.62 (beta)

10, Jan, 2019

1. Fix bugs on math input and rendering.
2. Other regression bug fix.

## 0.9.61 (beta)

08, Jan, 2019

1. Support global search in opened folder.
2. Support filter in outline panel.
3. Support search in preferences panel.
4. Support select default unit for word count (character count, line counts, etc).
5. Support move file by drag & drop in file tree panel, support duplicate file in file panel.
6. Add Portuguese (Portugal) support by [camilo93](https://github.com/jcamilo93), add Galician support by [nunhes](https://github.com/nunhes).
7. Add COLOL as supported code highlight language.
8. Fix text in menu bar is invisible on Linux.
9. Update MathJax Rendering engine to 2.7.5
10. Fix word count bug when document contains list. 
11. Support disable GPU acceleration when launch Typora.
12. Add warnings for file move/delete, add options to reset all warning dialogs.
13. Fix an SSX issue when rendering `<img>`.
14. Fix bugs about math block in exported PDF/docx
15. Other bug fix.

## 0.9.60 (beta)

27, Oct, 2018

1. Fix rename or move file would make window unresponsive.
2. Fix shift+ctrl+v will trigger paste twice.
3. Fix cannot open markdown file by double click on Linux.
4. Fix links relates to spellcheck.
5. Fix some content cannot be parsed in limited time.
6. Fix inline math would get corrupt or wrong cursor after editing.

## 0.9.59 (beta)

23, Oct, 2018

[Detail](https://support.typora.io/What's-New-0.9.59/)

1. Support spellcheck for non-English languages.
2. Save learned spelling and support unlearn spelling from context menu.
3. Add menu item to open file properties on Windows.
4. Fix “preserve line break” get ignore when export as PDF. Fix incorrect modify/create time for exported PDF file.
5. Add warnings when user enter typewriter/focus mode in their first time.
6. Fix bug about cursor and update issues for math.
7. Improve typing response, improve scroll performance and slightly improve speed for opening document.
8. Improve behaviors for “indent first line”.
9. Fix bug that image storage folder not updated after open new file.
10. Add sort function for file tree in sidebar.
11. Other bug fix.

## 0.9.58 (beta)

12, Sep, 2018

1. Add options for custom image storage folder.
2. Fix a critical bug triggered when pasting contents into tables.
3. Fix bugs relates to loading remote images.
4. Fix bugs that `<source>` tag inside `<video>` does not work.
5. Fix a security issue when loading local iframes. (Special Thanks to Zhiyang Zeng(@Wester) from Tencent Blade Team).
6. Fix bugs about pasting into lists.
7. Fix save failure when user does not have a "document" folder.
8. Auto hide menubar when entering full screen mode.
9. Other bug fix.

## 0.9.57 (beta)

30, Aug, 2018

1. Fix image export.
2. Fix crashment on glibc 2.28. (Linux)
3. Fix copy math into MS Word (Windows).
4. Fix parse error for lists and links.
5. Fix outline not updated after switch documents.
6. Improve paste behavior.
7. Other bug fix.

## 0.9.56 (beta)

22, Aug, 2018

1. Fix some bugs on previous version.

## 0.9.54 (beta)

19, Aug, 2018

[Detail](http://support.typora.io/What's-New-0.9.54/)

1. support preview for inline HTML, support HTML blocks.
2. Support all common HTML tags including `video`, `iframe`, `kbd`, `details`, `ruby`, etc.
3. Change a few default shortcut keys.
4. Follow CommonMark’s standard for parsing line break. Now line break is aligned in inline styles.
5. Improve UI for table, math, search panel, etc. And fix some CSS issues.
6. Add Swedish UI. (Thanks to [@FelixZY](https://github.com/FelixZY))
7. Improve paste logic, and support parsing/converting more HTML contents, include gist snip, iframe embed, etc.
8. Fix `Return` key and related undo/redo on tables.
9. Fix rendering bugs when `Indent first line of paragraph` is enabled.
10. Math block with Pandoc style attributes can be still parsed as Math block.
11. Search text will begin from current caret position, instead of start from document beginning. 
12. Fix bug that sometimes Typora window is invisible on start.
13. Fix typo for language `sqlite`, add `tsx`, `stylus`, `julia` syntax highlight.
14. Language and other attribute of code fences will be included when export using Pandoc.
15. Support HTML Entity Number.
16. Improve logic about picking correct smart quotes. Fix smart pants not exported when using Pandoc.
17. Fix window will scroll to incorrect position when user input code or math block.
18. Other bug fix.


## 0.9.53 (beta)

1, Jun, 2018

1. Fix Markdown line break does not work.
2. Fix bugs relates to SmartyPants.
3. Fix return key on tables.
4. Fix mirror styles and typos.
5. Remove default shortcut keys of  "typewriter" mode to prevent user from activating it accidentally and does not know how to exit.

## 0.9.52 (beta)

27, May, 2018

1. Add Smart Punctuation (SmartyPants) Support.
2. Support remap unicode punctuations on parse. [detail](http://support.typora.io/SmartyPants).
3. Fix bugs on saving process.
4. Fix bugs that some options are not saved after change.
5. Fix bugs and improve UI of table functions.
6. Fix bug that styles inside underline (`<u>`) are not rendered.
7. Fix undo/redo logic when changing styles or in source code mode.
8. Add syntax highlight for pseudocode.
9. Add Hungarian interface. Improve labels and translations.
10. Improve URL detect logic.
11. Other bug fix.

## 0.9.51 (beta)

15, May, 2018

1. Add Croatian language.
2. Add Dependency on deb package.
3. Fix logic when quiting and open Typora.
4. other bug fix.


## 0.9.50 (beta)

4, May, 2018

1. Fix a bug that some code fences cannot be edited.

## 0.9.49 (beta)

2, May, 2018

1. Add option to reopen last files/folders or open custom folders on start up.
2. Add 'Save All' command in menubar.
3. Allow escape `^` when superscript is enabled.
4. Better select word, delete word and triple click support.
5. Bug fix on typing in inline math.
6. Support launch flag in advanced setting.
7. Other bug fix.

## 0.9.48 (beta)

3, Apr, 2018

1. Add options for preserve or ignore whitespace/single line break when editing or export.
2. Update mermaid support and re-enable html labels in mermaid diagram.
3. Use colored emoji on Windows.
4. Fix bugs on ordered lists.
5. Improve logic for auto pair.
6. Remember typewriter/focus mode on window close.
7. Improve syntax highlight logic in source code mode.
8. Fix bugs on editing files in One Drive.
9. Re-open unsaved content when restart Typora after crash.
10. Add Dutch language support.
11. Other bug fix.

## 0.9.47 (beta)

14, Mar, 2018

1. Fix insert table or headins from enu not work in v0.9.46

## 0.9.46 (beta)

13, Mar, 2018

1. Task lists follows GFM's spec ([#643](https://github.com/typora/typora-issues/issues/643)). You may need to update your theme if your theme are downloaded.
2. Support disable auto-warp for code fences.
3. Support paste image directly. Add default actions and quick actions when insert images.
4. New language supports: German by [rcvd](https://github.com/rcvd) and Gert, Czech by [byDave251](https://github.com/byDave251), Greek by [kiriakosv](https://github.com/typora/kiriakosv).
5. Add `mediawiki-texvc` support for math.
6. Improve UI for mermaid and sequence.
7. Fix bug for copy and resize table.
8. Improve export quotation for math equations for PDF, ePub and image output.
9. Fix parsing errors for blockquote and emphasis.
10. Fix bugs relates to Chinese IME.
11. Other bug fix and improvements.

## 0.9.44 (beta)

9, Feb, 2018

1. Fix bug that sometimes sidebar cannot be hide completely after resize.
2. Use background on diagram nodes, fix hyperlink on flowchart cannot be opened.
3. Improve URL auto detect logic.
4. Fix `****` cannot be parsed as `<hr>`.
5. Fix bug relates to context menu.
6. Other mirror fix.

## 0.9.43 (beta)

6, Feb, 2018

1. New language support: Spanish by  [thepiratejester](https://github.com/thepiratejester), French by [MOrdinateur](https://github.comMOrdinateur), Russian by [dragomano](https://github.com/dragomano), Japanese by [tomochan001](https://github.com/tomochan001), Portuguese by [akz92](https://github.com/akz92).
2. Improve parse logic for block quotes, lists, and tables.
3. Support custom tab size for code blocks. Add options for default ordered list styles.
4. Improve compatibility with net drivers.
5. Fix `<br>` not exported.
6. Fix scrollbar on sidebar cannot be dragged.
7. Fix a bug that window may become invisible on start up sometimes.
8. Add syntax highlight for `SAS`.
9. Other bug fix.

## 0.9.42 (beta)

25, Jan, 2018

1.  Improve Simplified Chinese translation by [NoDotCat](https://github.com/NoDotCat), [HowardTangHw](https://github.com/HowardTangHw),  [Emphasia](https://github.com/Emphasia)
2. More language support: Traditional Chinese translation (by [cyberrob](https://github.com/cyberrob)), Polish translation (by  [iriusturar](https://github.com/iriusturar)), Korean translation (by  [ryush00](https://github.com/ryush00),  [marigold9124](https://github.com/marigold9124)), Italian translation (by  [starise](https://github.com/starise), [jethro17](https://github.com/jethro17)).
3. Support resize on sidebar.
4. Add Privacy Policy.
5. Support quick open.
6. Fix some bugs for table editing.
7. Fix a bug that highlight, superscript, subscript, image and inline math is not rendered in outline.
8. Fix a bug that Typora may be opened in nonexistent display when multiple displays are used.
9. Some performance improvement on opening file.
10. Fix a bug that flowchart is not correctly rendered when Windows style line ending is used.
11. Equation numbering is support after export as docx format for some math formula.
12. Fix a word count bug for Korean language.
13. Fix bugs on list editing.
14. Other bug fix.

## 0.9.41 (beta)

14, Dec, 2017

1. Add Chinese user interface.
2. Tables with long content supports scroll horizontally.
3. Improve PDF export, fix bugs relates to PDF export.
4. Add [strict mode](http://support.typora.io/Strict-Mode/) option for parsing markdown.
5. Fix bug that cannot open correct link address for hyperlink syntax.
6. Some fix bug about markdown parse logic.
7. Fix bugs about `[TOC]` .
8. Fix a bug that some options in advanced settings are not applied.
9. Other bug fix.

## 0.9.38 (beta)

29, Oct, 2017

1. Support `<br/>` tag in live rendering.
2. Update emoji library to cover emojis introduced during Unicode 7.0~10.0
3. Add syntax highlight for twig.
4. Improve auto indent in code fences
5. Fix bug that file attributes are reset after save.
6. Fix bugs on PDF export.
7. Fix a bug that YAML does not follow CRLF preference.
8. Fix a bug that user cannot open folder from command line sometime.
9. Fix window restore logic relates to multiple screens.
10. Other bug fix.

## 0.9.37 (beta)

25, Sep, 2017

1. Support show word count in selection.
2. Add syntax highlight for scheme.
3. Support natural sort in files panel.
4. Fix task list cannot be copy/pasted correctly.
5. Fix code fences padding on PDF export.
6. Other bug fix.

## 0.9.36 (beta)

26, Aug, 2017

1. Fix a bug that user cannot jump using [TOC].
2. Fix on exported HTML, `@include-when-export` failed to convert as `<link>`.

## 0.9.34 (beta)

24, Aug, 2017

1. Add menu items for changing task list status.
2. Add syntax highlight for makefile, tcl.
3. Fix mermaid gantt cannot be rendered.
4. Fix backspace after emoji.
5. Fix window will scroll to top when switch from inactive window to active one.
6. Fix a bug that sometimes `Return` does not work.
7. Hot fix for `-` will be converted to other character in exported PDF.
8. Fix a bug that typora cannot be opened from terminal multiple times.
9. Other mirror fix.

## 0.9.33 (beta)

15, Aug, 2017

1. Fix a critical bug that some code fences may crash the app. 

## 0.9.32 (beta)

13, Aug, 2017

1. Fix 100% CPU usage with menu on KDE on some linux distribution.
2. Fix some regression bug:
   1. `Ctrl+-`/`Ctrl+=`/`ctrl+[`/`ctrl+]` not work as expect.
   2. Auto pair for normal markdown characters does not work.
   3. Fix for `<img height="200" />` , the height attribute won't be correctly added when rendering.
   4. Performance improving when typing.
   5. Zoom level sometimes is incorrect on startup.
3. `@import` and `@include-when-export` will be converted to linked stylesheet when export to HTML.
4. Fix a bug that `ctrl`+click on hyperlink cannot open other protocol like `magic:` or others.
5. Fix a bug that selection should extend by word in some cases. 
6. Fix a bug that after selection, the select anchor will always move to its start boundary.
7. Ctrl+Ip/Down key and PageUp/PageDown key can exit code fences when the cursor is at start/end position of the code fences.
8. Better image select logic when editing: double click and auto select all raw text of an image.
9. Can copy tables to Words from context menu.
10. Select word/select line also supports code fences and source code mode.

## 0.9.30 (beta)

9, Aug, 2017

1. Support file tree/list in left side panel.
2. Start using CSS variable in themes. Change theme styles may be easier.
3. Support relative link to files without adding `.md` or `.markdown`  explicitly. 
4. Diagrams can auto fit the max-width.
5. Improve auto detect logic for urls.
6. Fix exported HTML/PDF does not follow original markdown's logic of line break.
7. Fix syntax highlight in night theme and syntax for protobuf, diff and php+html does not work. 
8. Change some inappropriate descriptions in menu, dialog and tooltip.
9. Fix bug that some `<a>` tags are not parsed correctly.
10. No auto-pair for markdown symbols in inline math.
11. Support Chinese character in header anchors.
12. Fix bug of delete and return key on selected text or table.
13. Find/Replace input supports undo/redo and hit selection in code fences won't be removed.
14. Fix excepted HTML tags are not escaped in exported HTML.
15. Fix nav key on context menu
16. Fix  bug that Math block cannot be copied.
17. Add tooltips on button.
18. Other bug fix.

## 0.9.29 (beta)

24, Apr, 2017

1. Fix a critical bug.

## 0.9.28 (beta)

22, Apr, 2017

1. Fix launch errors.

## 0.9.27 (beta)

17, Apr, 2017

1. Support setting line ending char. Support CRLF line ending.
2. Add syntax highlight support for `ProtoBuf`, fix syntax highlight for `php+html` and `diff`.
3. Fix styles for "unibody" style.
4. Fix font not applied when exporting.
5. Improve copy/paste to prevent data or style lost.
6. Fix key navigation on context menu.
7. Fix a few typos in text resource.
8. Fix header anchor cannot support some unicode char.
9. Fix spellcheck sometimes not working in Linux.

## 0.9.25 (beta)

09, Mar, 2017

1. Fix "import" does not work.
2. Imporve encoding detecting logic for better compatibility.

## 0.9.24 (beta)

27, Feb, 2017

1. Support `alt` key on Windows to popup related menu.
2. Support open recent files from menubar.
3. Fix a bug that Typora cannot detect the encode of some files correctly. Allow manually select file encode from menubar.
4. Fix bugs that table headers and bold Chinese characters cannot be printed (export to PDF) correctly.
5. Fix crash when export contents into jpg file.
6. Show horizontal scrollbar when some table or dialog is too width.
7. Set default extensions for save and export dialog.
8. Add syntax highligh for `fortran`. Fix bugs of syntax highlight function for `Scala` and `C#`.
9. Exported HTML (without class) for code fences could follow w3c recommendations and be more friendly with Prism.
10. Fix some bugs relates to crash and data lose.
11. Fix bugs that some behavior for links are not correct.
12. Fix table parsing logic for special characters.
13. Fix a bug that some math block is invalid in exported EPub.
14. Fix a bug that `\{` is not correctly handled in inline math.
15. Other bug fix.

## 0.9.23 (beta)

4, Jan, 2017

1. Support move table row/col when drag on left/top side of table row/col or using shortcut keys: shift + ctrl + arrow key.
2. Add syntax highlighting for `cmake`, `cypher`, `dart`, `django`, `dtd`, `dylan`, `handlebars`, `idl`, `web idl`, `yacas`, `mbox`, `vhdl`, `julia`, `haxe`, and `hxml`.
3. Remove `//` after `mailto:` for auto generated mail link.
4. Fix image position for flowchart.
5. Fix a bug that some link url or image url are escaped twice.
6. Fix a  bug that `:+1:` is not recognized as emoji.
7. Fix refresh mathjax will convert inline math when inline math is not enabled.
8. Fix freeze when insert images.
9. Other bug fix and improvements.

## 0.9.22 (beta)

20, Nov, 2016

1. Fix the logic for relative path for `typora-root-url`.
2. Support recent used files on Windows jumplist.
3. Support paste images into Typora(after set-up).
4. Support copy images to selected folder when insert images.
5. Fix bugs related to collapsible outline panel.
6. Fix bugs that exported PDF may contain  HTML in bookmark.
7. Fix bugs about undo/redo for nest task list.
8. Fix mermaid no responding when Chinese character exists.
9. Change `Copy as Markdown` option from opt-in to opt-out.
10. Support elixir for code fences.
11. Fix cli support on Linux.
12. Fix some typo on interface.

## 0.9.21 (beta)

18, Oct, 2016

1. Support insert image from local file. Support drag & drop multiple images.
2. Add preference to use relative path when insert images.
3. Improve footnote export and behavior.
4. Add option for auto-numbering math blocks. Support command for refreshing math expression.
5. Add option set left outline panel collapsible.
6. Support `<img>` tag without a close tag.
7. Remove unnecessary math delimiter for exported LaTeX. 
8. Add syntax highlight for `ocaml`, `F#`, `elm`, `spreadsheet` and `pgp(Ascii Armor)`.
9. Auto-save time schedule can be configured in advanced options.

## 0.9.20 (beta)

6, Oct, 2016

1. Add support for simple HTML fragments, only includes: `<!--comments-->`, `<a href="http://typora.io">link</a>`, `<img src="http://www.w3.org/html/logo/img/mark-word-icon.png" width="200px" />`.
2. Fix syntax highlight for `Octave` is not working, and add `matlab` as its alias. 
3. Math expressions now support export to epub. Diagrams will be converted to images when export to epub/docx.
4. Fix a bug that arrow of diagrams is missing when export to HTML/PDF.
5. Fix a critical bug on tables.
6. Fix some export options are missing in `Export` menu.
7. Other bug fix.

## 0.9.19 (beta)

26, Sep, 2016

1. Launched our [Theme Gallery](http://theme.typora.io) to share and download Typora themes.
2. Fix a bug the menubar won't show automatically when Typora is fullscreened.
3. Improve paste behavior.
4. Fix unnecessary scroll.
5. Fix backspace after UTF-32 character.
6. Fix bugs related to inline code inside table.
7. Recover outline panel status when switch from source code mode.
8. Other bug fix.
9. A Linux build (Debian/Ubuntu) is [available](https://typora.io/#linux).

## 0.9.18 (beta)

4, Sep, 2016

1. Add options to auto pair common markdown symbols, like `*_ etc.
2. Add options to show markdown source for simple blocks when focus, like headings.
3. Fix a bug that sometimes special characters will cause inline math not rendered.
4. Fix a bug that sometime `Enter` key is not working. 
5. Fix some bugs under high DPI screen.
6. Fix a bug that footnote definition cannot be correctly input.

## 0.9.17 (beta)

27, Aug, 2016

1. Fix special characters cannot be input inside inline math.
2. Fix backspace cannot expand inline style.

## 0.9.16 (beta)

19, Aug, 2016

1. Support diagrams, includes sequence, flowchart and mermaid ([doc](http://support.typora.io/Draw-Diagrams-With-Markdown/)).
2. Fix a bug related to parsing `*` and escaped character.
3. Fix backspace inside code fences.
4. Fix escape character will gone in inline math, inline code, and other inline styles.
5. Fix special character, such as `#` cannot be inserted in ceylon code block.
6. Fix quote mark would cause typora not respond sometimes.
7. Allow custom keybindings ([doc](http://support.typora.io/Custom-Key-Binding/)).
8. Allow custom search service ([doc](http://support.typora.io/Add-Search-Service/)).
9. Fix shift+ctrl+home/end key on Windows.
10. Other bug fix and improvements.

## 0.9.15 (beta)

29, Jul, 2016

1. Fix a bug that `**` is not correctly parsed.
2. Fix bookmark not generated when export to PDF when there's h5 and h6 in article.
3. Fix list indentation not correctly saved.
4. Fix footnotes contains "_" cannot be exported correctly.
5. Fix a bug some file format cannot be exported via pandoc.
6. Add "Textile" as one export option.
7. Improve URL auto detection.
8. Fix content will be pasted twice when paste from typora to Word.
9. Other bug fix.

## 0.9.14 (beta)

25, Jul, 2016

1. Fix print/export PDF not work.

## 0.9.13 (beta)

24, Jul, 2016

1. Release x64 build.
2. Add focus mode and typewriter mode support.
3. Remember last status of outline bar.
4. Add syntax support for assembly and TOML.
5. Avoid the usage of 'AltGr' key combination in assigned shortcut.
6. Support kramdown style `[toc]` syntax.
7. Improve list indent/outdent logic.
8. Fix HTML entities not escaped in meta block.
9. Fix a bug that triple click cannot select current line correctly.
10. Fix auto indent for brackets in code fences.
11. Add options to export reStructuredText, and OPML format.
12. Fix user.css not included in exported HTML/PDF.
13. Fix some export option not work in unibody window style.
14. Fix cannot export/print in dark theme.
15. Other bug fix.

## 0.9.12 (beta)

22, Jun, 2016

1. Fix a critical bug that the indent in multi-level lists may keep increasing after save.
2. Fix the scrollbar style on side panel.

## 0.9.11 (beta)

21, Jun, 2016

1. Fix a critical bug that the indents of multi-level lists are wrong when parsing and generating markdown source.
2. Better ECMAScript6 syntax highlight support for javascript code fences. Add syntax highlight support for NSIS, JSX ([React](http://facebook.github.io/react)'s JavaScript syntax extension), vue, LiveScript, mathematica, properties (and .ini), tiki wiki, dockerfile in code fences.
3. Hide auto-complete lists when scrolling.
4. Fix internal link to heading (like [this](#0.9.4.5-(beta))) not work.
5. Fix a bug sometimes, pasting would append duplicate texts.
6. Rule change: capitalized characters are not allowed in filenames for theme css file
7. Make link clickable in about page.
8. Support single column table in insert table dialog.
9. Add enabled optional inline style support, like highlight or inline math, in menubar.

## 0.9.10 (beta)

15, Jun, 2016

1. Fix style that sometimes user can see script content.
2. Fix auto pair match inside image and avoid glitch when complete brackets.
3. Fix paste table, and paste inside footnotes.
4. Fix `]` cannot be escaped in footnotes.
5. Fix `h6` indent inside `[TOC]`.
6. Fix multiple level lists inside blockquote cannot be parsed correctly.
7. Enable ESC key to close insert table dialog.
8. Fix outline sidebar jumpping around when scrolling.
9. Fix ctrl+home/end not working.

## 0.9 (beta)

2, Jun, 2016

1. Fix a bug that Typora cannot be launched by opening md files on PCs without *Visual C++ library* installed.

## 0.9.8 (beta)

1, Jun, 2016

1. Fix a critical bug about saving in source code mode.
2. Fix save dialog keep poping up sometimes.
3. Improve logic for auto match paired quotes and brackets.
4. Fix inline math cannot be exported to some file types via pandoc.
5. Fix a bug that improper file name is auto generated when the article contains YAML forn matters.

## 0.9.7 (beta)

30, May, 2016

1. Fix typora.exe is misreported by some anti virus software.


## 0.9.6 (beta)

27, May, 2016

1. Add mobile "responsive" support for exported HTML.
2. Pandoc requires 1.16 and above. Fix exporting fail using Pandoc.
3. Better support for monitoring file content change by external apps.
4. Fix generating PDF takes too much time and reduce file size for PDF. Also fix a bug anchor link in PDF not working and Chinese character in printed PDF is not selectable.
5. Fix shortcut keys for `h6` not working.
6. Add syntax highlight for Powershell. 
7. Remember windows size when creating new window.
8. Can open `.md` file from `cmd.exe` directly, if typora is its default reader.
9. Fix that some advance options not work. Add options to auto hide menu bar.
10. Fix a critical bug in paste/undo which may case data lose.
11. Make `\label` work in math block.
12. Fix unnecessary empty char in inserted footnote.
13. Fix auto pair match and find&replace in math block.
14. Fix up/down key behavior on code fences.
15. Fix some HTML code  (like `&phone;`) not escaped in inline code.
16. Other bug fix.

## 0.9.5 (beta)

5, May, 2016

1. Add pandoc integration, import function and export function for docx, rtf, LaTeX, etc.
2. Able to open `.md` file or import supported files by drag and drop into typora's window.
3. Fix a bug that sometimes PDF cannot be exported correctly.
4. Fix `H4` style in `pixyll` theme.
5. Fix sql mode error for code blocks.
6. Fix a bug for parsing headers with underline style.
7. Fix a bug for undo/redo for editing lists.
8. Fix a bug when pasting lists.
9. Other bug fix.

## 0.9.4 (beta)

23, Apr, 2016

1. Fix LaTeX is not correctly exported after opening existing files.
2. Fix a bug which may cause content inside list items get lost.
3. Fix wrong indent for content inside list after parsing raw markdown.
4. Support "Open File Location" action.
5. Fix a bug that if image path contains special chars like quotes, the image cannot be displayed correctly.
6. Fix a bug related to paste lists.
7. Fix a bug some line breaks disappear in exported PDF.



## 0.9.3 (beta)

19, Apr, 2016

1. Fix the wrong bookmark structure in exported PDF.
2. Fix sometimes Chinese characters cannot be saved to file correctly.
3. In exported HTML, file name will be set to `<title>` tag.

## 0.9.2 (beta)

18, Apr, 2016

1. Better save feature: Support file auto save (need enable it from preference panel) and allow users to recover unsaved drafts form preference panel.
2. Better word count: Now click word count button from status bar, detailed info would show.
3. Better Print: Fix a bug that current window, instead of generated web view woulc be printted.
4. Better PDF exporting: Now exported PDF could contains Table of Contents as bookmarks, just like Mac version
5. Better fullscreen mode: Fullscreen mode can auto show menu bar for native style windows, and auto show/hide title bar control buttons for unibody windows. Newly created windows would also be fullscreen in fullscreen mode.
6. Fix table cannot be deleted in the beginning of the article.
7. Fix a bug that some lines will be duplicated after open.
8. Fix files on external disks cannot be opened.
9. Other bug fix.

## 0.9.1 (beta)

6, Apr, 2016

1. Fix a critical bug for saving.
2. Fix a critical bug for task list.

## 0.9.0 (beta)

4, Apr, 2016

1. Rewrite typora's Markdown parse engine and largely improve the performance on opening mid-sized files.
2. Fix bugs for pair auto-complete.
3. Fix bugs for Korean IME.
4. Fix a bug that typora will eat and replace non-breaking space.
5. Fix relative image path on exported HTML.
6. Fix a bug typora will detech wrong encoding sometimes.
7. Other bugs.

## 0.8.8 (beta)

13, Mar, 2016

1. Fix minor parse issue for URL, subscript and superscript.
2. Fix compatibility issue between Chinese IME and auto-pair feature
3. Include and autoload MathJax extension, including chemistry package and others (e.g. $\ce{C6H5-CHO}$).
4. Fix bug triggered by pressing `` ctrl+` `` twice.
5. Fix some menu item under "Edit" submenu does not work.
6. Support open hyperlink from context menu.
7. Other bug fix.

## 0.8.6 (beta)

4, Mar, 2016

1. Fix a critical bug on Delete key.

## 0.8.5 (beta)

3, Mar, 2016

1. Support ==highlight== syntax (should enable it from preference panel).
2. Support auto complete pairs of brackets, quotes and parentheses.
3. Fix bugs on lists.
4. Fix cut on windows. 
5. Fix selection styles in code fences, python code in code fences will use 4-space indent.
6. Fix customize font size, local image, local font does not work for exported PDF.
7. Fix bugs for LaTeX editing/rendering.
8. Auto insert path/urls from clipboard when insert images/hyperlinks from menubar or shortcut keys.
9. Other bug fix.

## 0.8.3 (beta)

24, Feb, 2015

1. Add basic support for editing in source code mode directly.
2. Support signle line break (shift+return).
3. Improve LaTeX rendering quality.
4. Support non-UTF8/16 encoded files, includes Shift-JIS, Big5, EUC-JP, EUC-KR, GB18030, ISO-8859-1, ISO-8859-2, ISO-8859-5, ISO-8859-6, ISO-8859-7, ISO-8859-8, ISO-8859-9, windows-1250, windows-1251, windows-1252, windows-1253, windows-1254, windows-1255, windows-1256. Other encodings is not supported yet.
5. Fix bug that tab+subbullet will be parsed as code fences.
6. Fix syntax highlight support for PHP, SQL, Objective-c, etc.
7. Fix then behavior when pressing ctrl or shift and arrow key.
8. Fix bugs in find/replace.
9. Fix small bugs in exported HTMLs.
10. Support drag & drop to insert images and fix images not shown with relative path.
11. Fix cut & paste function.

## 0.7.7 (beta)

11, Jun, 2015

1. Imporve stability and reliability on saving

## 0.7.6 (beta)

3, Jun, 2015

1. Fix a critical bug which may cause data lose.
2. Fix syntax parse for task list.
3. Improve theme `newsprint`.
4. Fix the unnecessary io operation when starting Typora.

## 0.7.5 (beta)

24, DEC, 2015

First beta version.

## 0.7.0 (alpha)

19, DEC, 2015

First alpha version.