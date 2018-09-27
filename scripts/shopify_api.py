#!/usr/bin/env python

import shopify
import code
import sys
import os
import os.path
import glob
import subprocess
import functools
import yaml
import six
from six.moves import input, map

def start_interpreter(**variables):
    console = type('shopify ' + shopify.version.VERSION, (code.InteractiveConsole, object), {})
    import readline
    console(variables).interact()

class ConfigFileError(Exception):
    pass

def usage(usage_string):
    """Decorator to add a usage string to a function"""
    def decorate(func):
        func.usage = usage_string
        return func
    return decorate

class TasksMeta(type):
    _prog = os.path.basename(sys.argv[0])

    def __new__(mcs, name, bases, new_attrs):
        cls = type.__new__(mcs, name, bases, new_attrs)

        tasks = list(new_attrs.keys())
        tasks.append("help")
        def filter_func(item):
            return not item.startswith("_") and hasattr(getattr(cls, item), "__call__")
        tasks = filter(filter_func, tasks)
        cls._tasks = sorted(tasks)

        return cls

    def run_task(cls, task=None, *args):
        if task in [None, '-h', '--help']:
            cls.help()
            return

        # Allow unambigious abbreviations of tasks
        if task not in cls._tasks:
            matches = filter(lambda item: item.startswith(task), cls._tasks)
            if len(matches) == 1:
                task = matches[0]
            else:
                sys.stderr.write('Could not find task "%s".\n' % (task))

        task_func = getattr(cls, task)
        task_func(*args)

    @usage("help [TASK]")
    def help(cls, task=None):
        """Describe available tasks or one specific task"""
        if task is None:
            usage_list = []
            for task in iter(cls._tasks):
                task_func = getattr(cls, task)
                usage_string = "  %s %s" % (cls._prog, task_func.usage)
                desc = task_func.__doc__.splitlines()[0]
                usage_list.append((usage_string, desc))
            max_len = functools.reduce(lambda m, item: max(m, len(item[0])), usage_list, 0)
            print("Tasks:")
            cols = int(os.environ.get("COLUMNS", 80))
            for line, desc in usage_list:
                task_func = getattr(cls, task)
                if desc:
                    line = "%s%s  # %s" % (line, " " * (max_len - len(line)), desc)
                if len(line) > cols:
                    line = line[:cols - 3] + "..."
                print(line)
        else:
            task_func = getattr(cls, task)
            print("Usage:")
            print("  %s %s" % (cls._prog, task_func.usage))
            print("")
            print(task_func.__doc__)


@six.add_metaclass(TasksMeta)
class Tasks(object):
    _shop_config_dir = os.path.join(os.environ["HOME"], ".shopify", "shops")
    _default_symlink = os.path.join(_shop_config_dir, "default")

    @classmethod
    @usage("list")
    def list(cls):
        """list available connections"""
        for c in cls._available_connections():
            prefix = " * " if cls._is_default(c) else "   "
            print(prefix + c)

    @classmethod
    @usage("add CONNECTION")
    def add(cls, connection):
        """create a config file for a connection named CONNECTION"""
        filename = cls._get_config_filename(connection)
        if os.path.exists(filename):
            raise ConfigFileError("There is already a config file at " + filename)
        else:
            config = dict(protocol='https')
            domain = input("Domain? (leave blank for %s.myshopify.com) " % (connection))
            if not domain.strip():
                domain = "%s.myshopify.com" % (connection)
            config['domain'] = domain
            print("")
            print("open https://%s/admin/apps/private in your browser to generate API credentials" % (domain))
            config['api_key'] = input("API key? ")
            config['password'] = input("Password? ")
            if not os.path.isdir(cls._shop_config_dir):
                os.makedirs(cls._shop_config_dir)
            with open(filename, 'w') as f:
                f.write(yaml.dump(config, default_flow_style=False, explicit_start="---"))
        if len(list(cls._available_connections())) == 1:
            cls.default(connection)

    @classmethod
    @usage("remove CONNECTION")
    def remove(cls, connection):
        """remove the config file for CONNECTION"""
        filename = cls._get_config_filename(connection)
        if os.path.exists(filename):
            if cls._is_default(connection):
                os.remove(cls._default_symlink)
            os.remove(filename)
        else:
            cls._no_config_file_error(filename)

    @classmethod
    @usage("edit [CONNECTION]")
    def edit(cls, connection=None):
        """open the config file for CONNECTION with you default editor"""
        filename = cls._get_config_filename(connection)
        if os.path.exists(filename):
            editor = os.environ.get("EDITOR")
            if editor:
                subprocess.call([editor, filename])
            else:
                print("Please set an editor in the EDITOR environment variable")
        else:
            cls._no_config_file_error(filename)

    @classmethod
    @usage("show [CONNECTION]")
    def show(cls, connection=None):
        """output the location and contents of the CONNECTION's config file"""
        if connection is None:
            connection = cls._default_connection()
        filename = cls._get_config_filename(connection)
        if os.path.exists(filename):
            print(filename)
            with open(filename) as f:
                print(f.read())
        else:
            cls._no_config_file_error(filename)

    @classmethod
    @usage("default [CONNECTION]")
    def default(cls, connection=None):
        """show the default connection, or make CONNECTION the default"""
        if connection is not None:
            target = cls._get_config_filename(connection)
            if os.path.exists(target):
                if os.path.exists(cls._default_symlink):
                    os.remove(cls._default_symlink)
                os.symlink(target, cls._default_symlink)
            else:
                cls._no_config_file_error(target)
        if os.path.exists(cls._default_symlink):
            print("Default connection is " + cls._default_connection())
        else:
            print("There is no default connection set")

    @classmethod
    @usage("console [CONNECTION]")
    def console(cls, connection=None):
        """start an API console for CONNECTION"""
        filename = cls._get_config_filename(connection)
        if not os.path.exists(filename):
            cls._no_config_file_error(filename)

        with open(filename) as f:
            config = yaml.safe_load(f.read())
        print("using %s" % (config["domain"]))
        session = cls._session_from_config(config)
        shopify.ShopifyResource.activate_session(session)

        start_interpreter(shopify=shopify)

    @classmethod
    @usage("version")
    def version(cls, connection=None):
        """output the shopify library version"""
        print(shopify.version.VERSION)

    @classmethod
    def _available_connections(cls):
        return map(lambda item: os.path.splitext(os.path.basename(item))[0],
              glob.glob(os.path.join(cls._shop_config_dir, "*.yml")))

    @classmethod
    def _default_connection_target(cls):
        if not os.path.exists(cls._default_symlink):
            return None
        target = os.readlink(cls._default_symlink)
        return os.path.join(cls._shop_config_dir, target)


    @classmethod
    def _default_connection(cls):
        target = cls._default_connection_target()
        if not target:
            return None
        return os.path.splitext(os.path.basename(target))[0]

    @classmethod
    def _get_config_filename(cls, connection):
        if connection is None:
            return cls._default_symlink
        else:
            return os.path.join(cls._shop_config_dir, connection + ".yml")

    @classmethod
    def _session_from_config(cls, config):
        session = shopify.Session(config.get("domain"))
        session.protocol = config.get("protocol", "https")
        session.api_key = config.get("api_key")
        session.token = config.get("password")
        return session

    @classmethod
    def _is_default(cls, connection):
        return connection == cls._default_connection()

    @classmethod
    def _no_config_file_error(cls, filename):
        raise ConfigFileError("There is no config file at " + filename)

try:
    Tasks.run_task(*sys.argv[1:])
except ConfigFileError as e:
    print(e)
