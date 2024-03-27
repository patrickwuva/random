let mapleader = ","
call plug#begin('~/.vim/plugged')
  Plug 'preservim/nerdtree'
  Plug 'vim-scripts/indentpython.vim'	
  Plug 'tmsvg/pear-tree'
  Plug 'bfrg/vim-cpp-modern'
  Plug 'morhetz/gruvbox'
  Plug 'frazrepo/vim-rainbow'
  Plug 'preservim/nerdcommenter'
  Plug 'jiangmiao/auto-pairs'
  Plug 'itchyny/lightline.vim'
  Plug 'airblade/vim-gitgutter'
  Plug 'skywind3000/asyncrun.vim'
call plug#end()
let NERDTreeWinSize=17
set background=dark
colorscheme gruvbox
au BufNewFile, BufRead *.py
    \ set tabstop=4
    \ set softtabstop=4
    \ set shiftwidth=4
    \ set textwidth=79
    \ set expandtab
    \ set autoindent
    \ set fileformat=unix
au BufNewFile, BufRead *.js, *.html, *.css
    \ set tabstop=2
    \ set softtabstop=2
    \ set shiftwidth=2
au BufRead, BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/
let g:rainbow_active = 1
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l
filetype plugin on
set shiftwidth=4
set laststatus=2
syntax on
set noshowmode
set tabstop=4
set expandtab
set expandtab
set smartindent
set autoindent
set smarttab
set number
autocmd FileType c,python,java,javascript set number

inoremap (<CR> (<CR><CR>)<Esc>O
inoremap [<CR> [<CR><CR>]<Esc>O
inoremap {<CR> {<CR><CR>}<Esc>O

