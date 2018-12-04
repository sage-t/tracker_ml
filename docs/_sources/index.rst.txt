.. tracker-ml documentation master file, created by
   sphinx-quickstart on Mon Dec  3 20:00:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tracker-ml documentation
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   command_line_interface
   sdk


tracker-ml is the SDK and command line interface used with www.tracker.ml. These tools
enable local file tracking for every run of a machine learning project. Along with files,
parameters can also be tracked so that each run can be compared.


Example
========

Initialize tracker using the CLI and add the files you want to track. Then import
tracker_ml.tml anywhere and everywhere in your project. Use is easy::

   import tracker_ml.tml as tml

   tml.login("username", "password")
   tml.model("Logistic Regression")
   tml.record("description", "Tracker setup")

   # <machine learning code>

   # record int, float, or str
   tml.accuracy(0.42)
   tml.record("alpha", 0.9)

   # record multiple values under the same key
   tml.mrecord("epoch", 1)
   tml.mrecord("epoch", 2)
   tml.mrecord("epoch", 3)

