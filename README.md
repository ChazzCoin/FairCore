## FairCore

My goal? A base package with little to zero third-party
dependencies. I only made one exception, for DATE based functions (which uses, python-dateutil>=2.7.5).
Outside that, everything else is built on-top of python3 built-in modules.

Boo to bloat.
 
##### F Systems

* CLASS - Wrapped Functions. Routines. Threading. Callbacks. Listeners.
* LIST - [list] data type function helpers.
* DICT - {dict} data type function helpers.
* DATE - DateTime function helpers.
* LOG - Full Service Logging System.
* OS - Operating System Level helper functions.
* MATH - Simple math helpers.
* CONVERT - Convert data types.

**Data Type Helpers**

Just simple data type helpers. Lists, Dicts, Dates, etc...

```python
from F import LIST, DICT, DATE

""" (key, dict, defaultValue) """
dictOne = {"keyOne": "valueOne", "keyTwo": {"twoKeyOne":"twoValueOne"}}
DICT.get(key="keyOne", dic=dictOne)
DICT.get_key(value="valueOne", dict=dictOne)
DICT.get_all_keys(dictOne, ["keyOne", "keyTwo"])
DICT.get_from_path_keys(dictOne, "keyTwo", "twoKeyOne")
DICT.add_key_value(key="newKey", value="newValue", dic=dictOne)

""" (indexNumber, listObject, defaultValue) """
listOne = [1, 2, 3, 4, 5, 5]
LIST.get(index=0, items=listOne, default=False)
LIST.get_random(items=listOne)
LIST.remove_index(index=2, items=listOne)
LIST.scramble(listOne)
LIST.flatten(listOne, listOne, listOne)
LIST.remove_duplicates(list_in=listOne)
```

**Run Functions In The Background**

Run any function in the background, you can also add a call back,
or subscribe to the fair global channel.

```python
from F.CLASS import Thread

@Thread.runInBackground
def your_background_function():
    return "This function was run in the background."

```
**The Global FairCallbackChannel**

Run any function in the background and the FairGlobalCallback Channel,
will ALWAYS be called. You can subscribe any function as seen below
to begin receiving results/messages as well. Kind of like an override.

```python
from F.CLASS import FAIR_CALLBACK_CHANNEL

fairchannel = FAIR_CALLBACK_CHANNEL

@fairchannel.subscribe
def your_receive_global_callbacks(msg):
    return msg
```

**FairFunction**

A full function wrapper that autoMagically knows how to input
arguments and call functions for you. Makes running in the
background or setting up routines a breeze while also
'enhancing' your functions abilities and powers!

```python
from F.CLASS.Function import FairFunction

def your_getCallback(result):
    return result

def your_randomFunction(*args):
    pass

args = "arg1", "arg2"
function1 = FairFunction(function=your_randomFunction, arguments=args, callback=your_getCallback)
function1.run()
# or
function1.runBackground()
```

**FairRoutine**

Run any amount of functions how you want, sync them back in when
they are finished. More coming here, just the basics built.

```python
from F.CLASS.Routines import FairRoutine
routine1 = FairRoutine(functions=[FairFunction])
""" Run Each Function, One At a Time. """
routine1.start()
""" Run Each Function, All At Once, Keep Going. """
routine1.start_async()
""" Run Each Function, All At Once, Wait for All Results. """
routine1.start_await()

# other options
routine1.get_status()
```

**Log**

A quick, simple and easy loging solution for anyone.

```python
from F.LOG import Log

Log = Log()
e = "error"
Log.e(f"Failed to get key for dict.", error=e)
Log.w(f"This is a warning log message!")
Log.i(f"This is an info level logging message!")
Log.d(f"This is a debug level logging message!")
Log.v(f"This is a verbose level logging message!")
Log.s(f"This is a success message.")
```




    