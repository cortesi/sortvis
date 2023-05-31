Some steps to get the script running:

Install the Cairo library.

    sudo apt install libcairo2-dev

Create a Python virtual environment to install the dependencies. If you haven't
done that before, see Brett Cannon's [quick-and-dirty guide].

    python3 -m venv venv_sortvis
    . venv_sortvis/bin/activate
    python -m pip install --upgrade pip
    python -m pip install pycairo scurve

Now you should be able to run the script.

    echo 7 6 0 2 1 3 4 5 > sequence.txt
    ./sortvis weave -f sequence.txt -e docs/images/stub- --background 1a1a1a --gradient-start 0040ff --gradient-end 00086a --border-width 0 -x 400
    echo 3 11 2 1 5 15 6 16 7 12 10 0 9 19 14 4 13 18 8 17 > sequence.txt
    ./sortvis weave -e docs/images/weave- -t -x 850 -f sequence.txt -s bitonicsort
    echo 17 21 23 16 6 0 9 22 26 20 29 25 2 4 7 18 27 3 5 15 31 11 1 14 28 13 10 24 8 30 19 12 > sequence.txt
    ./sortvis weave -e docs/images/weave- -t -x 850 -f sequence.txt -a bitonicsort
    rm sequence.txt

Once you have all the images, you can recreate all the markdown pages.

    python write_pages.py

If you want to test the site locally, install Ruby 2.7, then launch the site.

    cd docs
    bundle install
    bundle exec jekyll serve

[quick-and-dirty guide]: https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/