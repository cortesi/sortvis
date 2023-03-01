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
    ./sortvis weave -f sequence.txt -e docs/images/stub- --background 000000 --gradient-start 0040ff --gradient-end 00086a --border-width 0 -x 400

[quick-and-dirty guide]: https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/