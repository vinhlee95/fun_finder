## Installation
### 1. Manage python version with `asdf`:
```shell
$ brew install asdf
$ asdf current
python          3.11.2          Not installed. Run "asdf install python 3.11.2"
```

The python version is specified in `.tool-versions`.

Next, install the python version using `asdf`:
```shell
$ asdf install
...
Installed Python-3.11.2 to /Users/vinhle/.asdf/installs/python/3.11.2

$ asdf current
python          3.11.2          /Users/vinhle/dev/apps/tennis-reservation/.tool-versions
```

### 2. Create a new virtual environment using `virtualenv`:
First install `virtualenv` if it is not installed on your local machine:
```shell
$ brew install virtualenv
$ virtualenv --version
virtualenv 20.21.0 from /opt/homebrew/lib/python3.11/site-packages/virtualenv/__init__.py
```

Create a virtual environment, having python version installed by `asdf`:
```shell 
$ virtualenv --python=$(asdf which python) reservation
```

### 3. Activate the virtual environment
```shell
$ source reservation/bin/activate
```

After this step, we should use correct python version in the virtual environment:
```shell
$ python --version
Python 3.11.2

$ which python
/Users/vinhle/dev/apps/tennis-reservation/reservation/bin/python
```

### 4. Install dependencies
```shell
$ pip3 install -r requirements.txt
```


## Usage
### Test fetching available slots for 1 court
Uncomment these lines in e.g. `smash_olari.py`:
```python
# available_slots = fetch_smash_olari_availability()
# print(available_slots)
```

Then run the command:
```shell
make run center=smash_olari 
```

When the fetching is done, we should have output of available slots in [smash_olari.json](./example_response/smash_olari.json).

Note that the output is not yet formatted to JSON. Using your IDE to do this to make the output easier to read.

## Development ideas
- [x] Specify court name in the query

## Learning ideas
- [ ] Learn how langchain tools work behind the scene