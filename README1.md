# financial tool
## Synopsis

A financial tool to keep track of personal expenditures.

## Code Example

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Motivation

I use this tool to collect data on my personal expenditures.

In the end I display this data in diagrams or just run some queries over it to get valuable information on my money expenditure behaviour.

This tool is some kind of learning by doing/learning by advancing when it comes to `python` programming and `sqlite3`.

It started out providing a GUI using **Tkinter**, but soon i focused on the API calls themselves.

I really do not want to do any more GUI programming with **Tkinter** - In fact, the GUI should be provided by a browser.

I separated the logic from the GUI and built a simple database framework just for the fun of it - more of a `sqlite3` wrapper class, which simplifies the transcations on the database.
 - `utils/database.py`
 - `utils/sqlite3_db.py`


Several **accounts** can be created.
In my case an **account** is more likely a topic like __expenditures__, __bitcoins__, __cash__, __assets__, ...

**__Soon to come:__**
 - higher focus on the actual API
   + list accounts
   + create accounts
   + transfer
 - build a proper browser GUI
   + activate the server once more
   + include simple queries to show data in diagrams
 - containerize it (docker)

## Installation

Not yet installable. Should be soon.

Start the GUI like this:
 - `python input_gui.py`

## API Reference

The API calls are limited to program arguments/options.

**__Soon to come:__**
 - REST API endpoints

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

A short snippet describing the license (MIT, Apache, etc.)
