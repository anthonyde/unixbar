unixbar :sunglasses:
=======

unixbar is a [Unix-philosophical][1] status bar driver.  It aims to replace
the complicated driver script that everyone writes when using status bar
programs like dzen2 or lemonbar with a tool that does the same thing with
modular and reusable components.  By handling all communication between data
sources and the bar itself, unixbar allows you to focus on how data is
presented.

Features:

 * Modular configuration
 * Support for reusable workers written in any language
 * Support for extending the core feature set with modules

The screenshot below demonstrates a configuration with multiple status icons,
notifications, and an OSD all controlled by the same instance of unixbar.

![A sample bar with multiple status icons, notifications, and OSD][2]

See the [config][3] branch for details about this configuration.

[1]: http://www.catb.org/esr/writings/taoup/html/ch01s06.html
[2]: sample.png?raw=true "Sample screenshot (config branch)"
[3]: https://github.com/anthonyde/unixbar/tree/config

Installation
------------

Requirements:

 * Python 3.5
 * A status bar program like dzen2 or lemonbar

First, get the code:

    $ git clone https://github.com/anthonyde/unixbar.git

The default configuration uses lemonbar.  If you use a different status bar
program, see the next section to change the configuration first.

Next, run the code:

    $ cd unixbar
    $ ./run-unixbar

A status bar should appear displaying the current time.

Configuration
-------------

Two subpackages of unixbar determine the active configuration: `config` and
`lib`.  `config` defines initialization parameters, event handlers, and how
data is transformed and presented.  `lib` defines workers and extension
modules.

Knowing how data flows through unixbar will make it easier to configure.  In
general, data is processed in the following order:

 * A worker sends data to unixbar
 * A data transformer, if configured, runs on the data
 * Viewers format the data for presentation
 * Views are aggregated and sent to the bar for rendering

### Bar Configuration

The `bar_args` function in the `config` subpackage determines how the status
bar is launched.  It returns a list of strings containing the bar command and
its arguments.  A simple example might look like the following:

```python
def bar_args():
  return ["somerandombar", "-bg", "black"]
```

The `bar_click` function handles click events.  See the default configuration
for more information.

### Workers and Extension Modules

Workers and extension modules are components that introduce new functionality,
such as periodically reporting battery status or adding support for
notifications.  They are defined in the `lib` subpackage.

A worker is a piece of code that runs automatically when unixbar starts.
Workers can send data to unixbar by printing 'key=value' strings to standard
output, one per line.  These key-value pairs are cached internally and passed
to viewers for presentation.

Two types of workers are supported: thread workers and process workers.
Thread workers run as threads inside the main unixbar process and can only be
defined in an extension module, while process workers run as children of the
main process and can consist of any executable file.  All executable files in
the `lib` directory will be run as process workers.

Extension modules are Python modules in the `lib` subpackage containing code
that can be used by workers other extensions, or configuration.  These are
automatically loaded when unixbar starts and can be accessed by importing them
from `lib`.

For more information see the examples in the `contrib` directory.  You can
symlink these files from 'lib' to use them in your own configuration.

### Viewers

Viewers are functions that control how data is presented.  They are defined in
the `config` subpackage and accept worker data as input.  This data is
populated from an internal cache by parameter name.  Each viewer can print
'key=value' strings containing formatted data which is cached internally for
rendering.

If data is accepted from an untrusted source, such as a window title, an
access point name, or any other string that could be crafted by a third party,
it's important to sanitize that data as needed by your status bar program
before it is rendered.  Rendering untrusted data directly could potentially
allow an attacker to control the contents of the status bar or even execute
arbitrary commands depending on the program you use.

Data transformers can optionally transform worker data before it is sent to
viewers, e.g. for automatic type conversion.  See the `data` module and the
sample configuration for details.

Finally, the `print_bar` function in the `config` subpackage controls the
overall layout of the bar.  It receives formatted view data as input and
prints a string that is sent to the status bar.

Development
-----------

Feel free to fork this project on [GitHub][4], publish a branch with your own
configuration, or share your workers and extension modules by putting them in
the `contrib` directory and sending a pull request.  Bug reports, feature
requests, and changes to the core program are also welcome.

[4]: https://github.com/anthonyde/unixbar

License
-------

The files in this project are released under version 3 of the GNU General
Public License unless stated otherwise.  See the file `LICENSE` for details.
