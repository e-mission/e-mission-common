# e-mission-common library

Part of the greater [e-mission project](https://github.com/e-mission).

This library contains code used by multiple e-mission components including [e-mission-server](https://github.com/e-mission/e-mission-server), [e-mission-phone](https://github.com/e-mission/e-mission-phone), [em-public-dashboard](https://github.com/e-mission/em-public-dashboard), and [op-admin-dashboard](https://github.com/e-mission/op-admin-dashboard).

This repository uses the [Transcrypt](https://www.transcrypt.org/) library to compile Python code to JavaScript. This allows us to write and maintain code in 1 language and import it for use in all 4 of the above repos.

## Setup

Anaconda is required.

```bash
. bin/setup.sh
```

This will:
 - Retrieve setup scripts from `e-mission-server` and use them to set up a conda environment called `emcommon` with the dependencies listed in `bin/environment.yml` This way, the `emcommon` environment uses the same Python version as `e-mission-server`.
 - Run `npm install`.

Re-run this if you change the dependencies in `environment.yml` or `package.json`.

## To contribute

1. Make your changes to Python code under the `src` directory.
1. Run `bash bin/compile_to_js.sh` to build the JavaScript. This will produce output JS files in the `emcommon_js` directory. However, `pip install transcrypt` is required.
1. Commit changes from both the `src` and `emcommon_js` directories to your branch.

## Tips for writing code to work in both Python and JavaScript

1. Use the `emcommon.logger` module for all logs; it is set up to work in both languages.

    ```python
    import emcommon.logger as Log
    ```

1. When you need to run a snippet in Python but not in JavaScript, you can use the `skip` pragma to skip one line or multiple lines.
   
    ```python
    Log.info("This line executes in both Python and JavaScript")
    
    Log.info("But this line only executes in in Python") # __: skip
    
    # __pragma__('skip')
    Log.info("This whole block of lines only executes in Python")
    Log.info("JS ignores anything between the skip and noskip pragma comments")
    # __pragma__('noskip')
    
    Log.info("This line is back to executing in both Python and JavaScript")
    ```
1. When you need to run something in JavaScript but not in Python, you can use an **"executable comment"**, which starts with `'''?` and ends with `?'''`.
   
    ```python
    Log.info("This line executes in both Python and JavaScript")
    
    '''?
    Log.info("This only executes in JavaScript")
    Log.info("The Transcrypt compiler will convert this to JavaScript code")
    Log.info("But regular Python will just see it as a comment and ignore it")
    ?'''
    ```
1. If you need to insert raw JavaScript code, you can use the `js` pragma.
   
    ```python
    Log.info("This is Python code that executes in both Python and JavaScript")
    # __pragma__('js', '{}', 'alert("This is raw JavaScript code that executes in JavaScript")')
    ```
    If you need multiple lines of raw JavaScript, you can wrap the `js` pragma in an **"executable comment"**.
   
    ```python
    '''?
    __pragma__('js', '{}', """
      let msg = "This is raw JavaScript code that executes in JavaScript";
      msg += ", and it can be multiple lines";
      alert(msg);
    """)
    ?'''
    ```

For more detail, refer to the Transcrypt docs on the [many kinds of pragmas available.](https://www.transcrypt.org/docs/html/special_facilities.html)

## Using e-mission-common in a Python or JavaScript project

### For Python:

To test local changes:
1. Make your local changes in the `src/` directory.
1. From your other repo, run `pip install -e <path_to_this_repo>` to use the local version of e-mission-common.

To use a remote branch or tag in your Python project:
 - Use `pip install git+https://github.com/JGreenlee/e-mission-common@master`

   -OR-
 
 - List `git+https://github.com/JGreenlee/e-mission-common@master` in an `environment.yml`


### For JavaScript:

To test local changes:
1. Make your local changes in the `src/` directory.
1. Run `bash bin/compile_to_js.sh` to build the JavaScript.
1. From this repo, run `npm link` to establish a symlink to your local version of e-mission-common.
1. From the other repo, run `npm link e-mission-common` to use the symlinked version of this repo.

To use a remote branch or tag in your JavaScript project:
 - Add `"e-mission-common": "github:JGreenlee/e-mission-common#master"` to your `dependencies` in `package.json`.

## Unit testing

Due to the nature of this library, it is critical to test both the Python source and the compiled JavaScript. Ideally, we can write a test suite in a `.py` file and have it run in both Python and JavaScript environments.

This is possible, to a degree, using `transcrypt` to compile test files to JavaScript, and then running `jest` on the compiled JavaScript.
> `pytest` was chosen over `unittest` because it is more flexible, allowing tests to be written in a way that can be compiled to Jest-compatible JavaScript. (It is also more concise and friendly to write.)

See the `tests` directory for `.py` files that are not accompanied by a `.js` file. These files are intended to be run in both Python and JavaScript environments.

### Dedicated JS test files

There may be testing scenarios that must significantly diverge between Python and JavaScript versions. In these cases, we can write a separate `.js` file next to the `.py` file of the same name. In this case, no compilation is necessary; `pytest` will run the `.py` file and `jest` will run the `.js`.

### Running the tests

```bash
. bin/run_pytest.sh
```

```bash
. bin/run_jest.sh
```
