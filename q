diff --git a/shell/envrc/vimrc b/shell/envrc/vimrc
index 68e20cb..ee236ae 100644
--- a/shell/envrc/vimrc
+++ b/shell/envrc/vimrc
@@ -1,3 +1,8 @@
+" File              : vimrc
+" Author            : du min <min.du@hobot.cc>
+" Date              : 13.07.2018
+" Last Modified Date: 13.07.2018
+" Last Modified By  : du min <min.du@hobot.cc>
 set nocompatible
 filetype off
 
@@ -13,8 +18,9 @@ Plugin 'jiangmiao/auto-pairs'
 Plugin 'Yggdroot/indentLine'
 Plugin 'vim-scripts/python_fold'
 
-Plugin 'SirVer/ultisnips'
+Plugin 'alpertuna/vim-header'
 Plugin 'honza/vim-snippets'
+Plugin 'SirVer/ultisnips'
 
 Plugin 'pangloss/vim-javascript'
 Plugin 'mxw/vim-jsx'
@@ -38,6 +44,8 @@ autocmd Filetype html setlocal ts=2 sts=2 sw=2
 autocmd Filetype css setlocal ts=2 sts=2 sw=2
 autocmd Filetype scss setlocal ts=2 sts=2 sw=2
 autocmd Filetype javascript setlocal ts=2 sts=2 sw=2
+autocmd Filetype md setlocal ts=2 sts=2 sw=2
+autocmd Filetype markdown setlocal ts=2 sts=2 sw=2
 autocmd Filetype python setlocal ts=4 sts=4 sw=4
 
 "nerdtree
@@ -57,3 +65,9 @@ let g:ultisnips_python_style="google"
 
 "vim-jsx
 let g:jsx_ext_required = 0
+
+"vim-header
+let g:header_field_author = 'du min'
+let g:header_field_author_email = 'min.du@hobot.cc'
+map <F4> :AddHeader<CR>
+autocmd bufnewfile *.py :AddHeader
