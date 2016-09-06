#coding=utf-8

import argparse

import sys
import argparse
import qrcode
sys.path.extend(['/usr/lib/python2.7/dist-packages', '/usr/lib/python2.7/'])
import qrtools

import utils

VERSION="0.1"

def encode(data, target):
    img = qrcode.make(data)
    img.save(target)

def decode(img):
    if not img:
        return None
    qr = qrtools.QR()
    if qr.decode(img):
        return qr.data
    else:
        raise ValueError("Failed to decode data from '%s'" % img)

class QRCodeShellParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(QRCodeShellParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """
        Prints a usage message incorporating the message to stderr and exit.
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, ("error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                "for more information.\n") %
                {'errmsg': message.split(choose_from)[0],
                    'mainp': progparts[0],
                    'subp': progparts[2]})

class Shell(object):

    def get_base_parser(self):
        """
        Get a base parser including some global arguments.
        """
        parser = QRCodeShellParser(prog = 'qrcode',
                description='A python app for creating and decoding QR Codes',
                epilog='See "qrcode help COMMAND" for help on a specific comand.',
                add_help = False
        )
        parser.add_argument(
                '-h', '--help',
                action='store_true',
                help=argparse.SUPPRESS,
        )
        parser.add_argument(
                '-v', '--version',
                action='version',
                version='0.1',
        )
        return parser

    def get_subcommand_parse(self):
        """
        Auto discover subcommands.
        """
        parser = self.get_base_parser()
        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        self._find_actions(subparsers, self)
        return parser

    def _find_actions(self, subparsers, actions_module):
        """
        Find attribute starts with "do_" in a actions module and append to the subcommands.
        """
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help =desc.strip()
            arguments = getattr(callback, 'arguments', [])
            subparser = subparsers.add_parser(command,
                    help=action_help,
                    description=desc,
                    add_help=False,
            )
            subparser.add_argument('-h', '--help',
                    action='help',
                    help=argparse.SUPPRESS,
            )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    @utils.arg('-d','--data',
            dest='data',
            metavar='<data>',
            type=str,
            help='The data to generate qrcode.',
            default=None,
    )
    @utils.arg('-o','--output',
            dest='output',
            metavar='<output>',
            help='Write qrcode to <file>',
            default=None,
    )
    def do_encode(self, args):
        """
        Generate qrcode for the given data.
        """
        if args.data is None:
            print("ERROR: option '--data/-d' is required.")
            self.subcommands['encode'].print_help()
            return False
        if args.output is None:
            print("ERROR: option '--output/-o' is required.")
            self.subcommands['encode'].print_help()
            return False
        img = qrcode.make(args.data)
        img.save(args.output)
        return True

    @utils.arg('-f','--file',
            dest='file',
            metavar='<file>',
            help='The qrcode to decode.',
            default=None,
    )
    def do_decode(self, args):
        """
        Decode a qrcode, return the data.
        """
        if args.file is None:
            print("ERROR: option '--file/-f' is required.")
            self.subcommands['decode'].print_help()
        qr = qrtools.QR()
        if qr.decode(args.file):
            print(qr.data)
            return qr.data
        else:
            raise ValueError("Failed to decode data from '%s'" % args.file)

    def do_bash_completion(self, argv):
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in sc._optionals._option_string_actions.keys():
                options.add(option)
        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))


    @utils.arg('command',
            metavar='<subcommand>',
            nargs='?',
            help='Display help for <subcommand>'
    )
    def do_help(self, argv):
        """
        Display help about this program or one of its subcommands.
        """
        if argv.command:
            if argv.command in self.subcommands:
                self.subcommands[argv.command].print_help()
            else:
                print("'%s' is not a valid subcommand." % args.command)
        else:
            self.parser.print_help()

    def main(self, argv):
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        subcommand_parser = self.get_subcommand_parse()
        self.parser = subcommand_parser
        if options.help or not argv:
            subcommand_parser.print_help()
            return 0
        args = subcommand_parser.parse_args(argv)
        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0
        args.func(args)

def main():
    Shell().main(sys.argv[1:])

if __name__ == "__main__":
    main()
