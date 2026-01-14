conda activate cb && rm -rf docs/* && jupyter-book build source && cp -r source/_build/html/* docs/ && touch docs/.nojekyll && rm -rf source/_build
