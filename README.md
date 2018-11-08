# tracker_ml

www.tracker.ml SDK and CLI

## Install




## Build

Install build tools
```
python -m pip install --user --upgrade setuptools wheel
```

Create distribution archives
```
python setup.py sdist bdist_wheel
```

Install from archives
```
python -m pip install dist/tracker_ml-X.X.X.tar.gz
```

## Python SDK

### Use

First, initialize tracker using the CLI and update the files you want to track. Then import 
`trackerml` anywhere and everywhere. Use is easy:

```python
import tracker_ml.tml as tml

tml.login("username", "password")
tml.model("Logistic Regression")

# <machine learning code>

# record int, float, or str
tml.record("accuracy", 0.42)
tml.record("model", "Logistic Regression")

# record multiple values under the same key
tml.mrecord("epoch", 1)
tml.mrecord("epoch", 2)
tml.mrecord("epoch", 3)

# data will be saved locally and to the API on exit
```

All changes since the previous run and all recorded values will be automatically saved. The CLI
can be used to view/compare trials and undo changes.


## Command Line Interface

tracker.ml command line interface for locally tracking/reverting file changes and tracking results 
for each change. Similar to git, but works with the SDK to track every time a new model is 
trained/tested.


### Use

Use the help command. (Not all commands displayed work yet)

```
$ tracker --help
$ tracker status --help
```

Initialize in the project root. 

```
$ tracker init -u <username> -p <password> -n <project name>
```

Add file(s)/directory(s) that will be saved every run. 

```
$ tracker add .
```

Stop recording file(s)/directory(s) that would be saved every run. 

```
$ tracker remove .
```

View past trials and sort them

```
$ tracker status
 Total trials: 4
 Sorted by: id

  Id  |  Accuracy  |         Model
------------------------------------------
  4   |     63     |  Logistic Regression
  3   |     74     |  Logistic Regression
  2   |     50     |  Logistic Regression
  1   |     92     |  Logistic Regression
$ python tracker.py status -k accuracy -l 2 -r
 Total trials: 4
 Reverse sorted by: accuracy
 Only displaying 2 results

  Id  |  Accuracy  |         Model
------------------------------------------
  2   |     50     |  Logistic Regression
  4   |     63     |  Logistic Regression
```
