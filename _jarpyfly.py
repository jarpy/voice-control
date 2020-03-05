# -*- coding: utf-8 -*-

from dragonfly import CompoundRule, Grammar, MappingRule, Integer, Dictation, Function
from aenea.strict import Key, Text, Pause                   
from dragonfly import Key as OriginalKey
from dragonfly import FocusWindow as LocalFocusWindow
from aenea import ProxyAppContext as AppContext
from dragonfly.windows.clipboard import Clipboard

import pyttsx
import win32gui

speech_engine = pyttsx.init()

global_context = None

emacs_context = AppContext(title="emacs")
vscode_linux_context = AppContext(title="Code - OSS")
vscode_windows_context = AppContext(title="Visual Studio Code")
gmail_context = AppContext(title="Elastic Mail")
terminal_context = AppContext(title="termite")

firefox_context = AppContext(executable="firefox")
chrome_context = AppContext(title="Google Chrome")
chromium_context = AppContext(title="Chromium")
browser_context = chrome_context | chromium_context | firefox_context
vscode_context = vscode_linux_context | vscode_windows_context

nato_alphabet = {
    'alpha': 'a',
    'alfa': 'a',
    'offer': 'a',
    'of the': 'a',
    'bravo': 'b',
    'charlie': 'c',
    'delta': 'd',
    'echo': 'e',
    'foxtrot': 'f',
    'golf': 'g',
    'hotel': 'h',
    'india': 'i',
    'juliett': 'j',
    'juliet': 'j',
    'julian': 'j',
    'kilo': 'k',
    'killer': 'k',
    'lima': 'l',
    'limo': 'l',
    'mike': 'm',
    'november': 'n',
    'oscar': 'o',
    'papa': 'p',
    'popper': 'p',
    'quebec': 'q',
    'québec': 'q',
    'romeo': 'r',
    'sierra': 's',
    'sarah': 's',
    'tango': 't',
    'uniform': 'u',
    'victor': 'v',
    'whiskey': 'w',
    'x-ray': 'x',
    'yankee': 'y',
    'zulu': 'z',
    'zero': '0',
    'one': '1',
    'won': '1',
    'two': '2',
    'to': '2',
    'too': '2',
    'three': '3',
    'for': '4',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'niner': '9',
}


def down_case(text):
    "This thing => this thing"
    return text.lower()

def smash_case(text):
    "This thing => thisthing"
    return text.lower().replace(' ', '')

def kebab_case(text):
    "This thing => this-thing"
    return text.lower().replace(' ', '-')

def snake_case(text):
    "This thing => this_thing"
    return text.lower().replace(' ', '_')

def nato_to_char(text):
    try:
        print "Nato: %s" % text
        return [nato_alphabet[phonetic] for phonetic in text.lower().split()]
    except KeyError:
        return ["nato error".split()]  # FIXME: make a noise


# Emacs (and vscode)
emacs_grammar = Grammar("emacs", emacs_context | vscode_context)
class EmacsRule(MappingRule):
    mapping = {
        "clang": Key("c-g:2"),
        "yank": Key("c-y"),
        "one window": Key("c-x, 1"),
        "two windows": Key("c-x, 1, c-x, 3"),
        "three windows": Key("c-x, 1, c-x, 3, c-x, 3, c-x, plus"),
        "four windows": Key("c-x, 1, c-x, 2, c-x, 3, s-down, c-x, 3, c-x, plus"),
        "six windows": Key("c-x, 1, c-x, 2, c-x, 3, c-x, 3, s-down, c-x, 3, c-x, 3, c-x, plus"),
        "kill buffer": Key("c-x, k"),
        "kill word": Key("a-d"),
        "done with buffer": Key("c-x, hash"),
        "retro word": Key("a-b"),
        "pro word": Key("a-f"),
        "kill line": Key("c-k"),
        "kill whole line": Key("c-a, c-a, c-k, c-k"),
        "window right": Key("s-right"),
        "window far right": Key("s-right:4"),
        "window left": Key("s-left"),
        "window far left": Key("s-left:4"),
        "window down": Key("s-down"),
        "window up": Key("s-up"),
        "open line": Key("c-e, a-o"),
        "save (buffer|file)": Key("c-x, c-s"),
        "Centre view": Key("c-u, 1, 0, c-l"),
        "(no no|nono)": Key("cs-minus"),
        "(duplicate|dupe|double) (line|region|that)": Key("c-c, d"),
        "(top|start) [of] buffer": Key("as-comma"),
        "(bottom|end) [of] buffer": Key("as-dot"),
        "start [of] line": Key("c-a"),
        "end [of] line": Key("c-e"),
        "(search forward|pro search) <text>": Key("c-s") + Text("%(text)s"),
        "(search forward|pro search)": Key("c-s"),
        "(mark|set mark)": Key("c-space"),
        "jump line": Key("j, l"),
        "jump word": Key("j, w"),
}

    extras = [
        Dictation("text"),
        Integer("n", 1, 9),
    ]
emacs_grammar.add_rule(EmacsRule())


class FindFileRule(CompoundRule):
    spec = "(find|open) file <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-x, c-f").execute()
        Text(smash_case(extras["text"])).execute()
        # Key("enter").execute()
emacs_grammar.add_rule(FindFileRule())


class RecentFileRule(CompoundRule):
    spec = "recent file <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-c, f").execute()
        Text(smash_case(extras["text"])).execute()
        # Key("enter").execute()
emacs_grammar.add_rule(RecentFileRule())


class JumpBufferRule(CompoundRule):
    spec = "(jump|go|switch) buffer <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-x, b").execute()
        Text(smash_case(extras["text"])).execute()
        Key("enter").execute()
emacs_grammar.add_rule(JumpBufferRule())


class JumpWordRule(CompoundRule):
    spec = "jump word <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        letters = nato_to_char(str(extras["text"]))
        Key("j, w").execute()
        Key(', '.join(letters)).execute()
emacs_grammar.add_rule(JumpWordRule())


class MetaXRule(CompoundRule):
    spec = "metaxu <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("a-x").execute()
        Pause("10").execute()
        Text(smash_case(str(extras["text"]))).execute()
        Key("enter").execute()
emacs_grammar.add_rule(MetaXRule())

emacs_grammar.load()

# Global
global_grammar = Grammar("global-grammar", context=global_context)

class DowncaseRule(CompoundRule):
    spec = "(flatten|lower|downcase) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(down_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(DowncaseRule())


class SmashRule(CompoundRule):
    spec = "smash <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(smash_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(SmashRule())


class KebabRule(CompoundRule):
    spec = "kebab <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(kebab_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(KebabRule())


class SnakeRule(CompoundRule):
    spec = "snake <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(snake_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(SnakeRule())


class NatoRule(CompoundRule):
    spec = "(nato|type|press|punch|push) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        print("NatoRule: %s" % str(extras["text"]))
        letters = nato_to_char(str(extras["text"]))
        Key(', '.join(letters)).execute()
global_grammar.add_rule(NatoRule())


class LongoptRule(CompoundRule):
    spec = "longopt <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(kebab_case('--' + str(extras["text"])))
        t.execute()

global_grammar.add_rule(LongoptRule())

global_grammar.load()


class GmailRule(MappingRule):
    mapping = {
        "archive": Key("y"),
        "mute": Key("m"),
        "next": Key("k"),
        "inbox": Key("g, i"),
        "oldest": Key("j:100"),
        "newest": Key("k:100"),
        "open": Key("o"),
        "(expand|show all)": Key(";"),
    }

gmail_grammar = Grammar("gmail", gmail_context)
gmail_grammar.add_rule(GmailRule())
gmail_grammar.load()


class BrowserRule(MappingRule):
    mapping = {
        "top": Key("home"),
        "bottom": Key("end"),
        "down": Key("pgdown"),
        "up": Key("pgup"),
        "links": Key("a-dot"),
        "close": Key("c-w"),
        "reload": Key("cs-r"),
        "(bigger|zoom in)": Key("cs-plus"),
        "(smaller|zoom out)": Key("cs-minus"),
        "refresh": Key("cs-r"),
        "close tab": Key("c-w"),
        "tab <n>": Key("c-%(n)d"),
        "new window": Key("c-n"),
        "new tab": Key("c-t"),
        "browse <text>": Key("c-l") + Text("%(text)s") + Key("enter"),
        "browse history <text>": Key("c-l") + Text("%(text)s") + Key("down"),
        "slack channel <text>": Key("c-k") + Text("%(text)s"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]


gmail_grammar = Grammar("browser", browser_context)
gmail_grammar.add_rule(BrowserRule())
gmail_grammar.load()

# Terminal
terminal_grammar = Grammar("terminal", terminal_context)
class TermiteRule(MappingRule):
    mapping = {
        "(bigger|zoom in)": Key("c-plus"),
        "(smaller|zoom out)": Key("c-minus"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
terminal_grammar.add_rule(TermiteRule())

class BashRule(MappingRule):
    mapping = {
        "new session <text>": Text("tmux new-session -t %(text)s") + Key("enter"),
        "(attach|connect) session <text>": Text("tmux attach -t %(text)s") + Key("tab, enter"),
        "list sessions": Text("tmux list-sessions") + Key("enter"),
        "(Rerun last|do again|do it again)": Key("up, enter"),
        "go home": Text("cd ~") + Key("enter"),
        "go source (folder|dir|directory)": Text("cd ~/src/") + Key("enter"),
        "get pods": Text("kubectl get pods") + ("enter"),
        "git reset hard": Text("git reset --hard") + Key("enter"),
        "git pull": Text("git pull") + Key("enter"),
        "git fetch [all]": Text("git fetch --all") + Key("enter"),
        "git log patch": Text("git log --oneline -p") + Key("enter"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
terminal_grammar.add_rule(BashRule())


class FuzzyFileRule(CompoundRule):
    spec = "fuzzy <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("space, c-t").execute()
        Text(smash_case(extras["text"])).execute()
terminal_grammar.add_rule(FuzzyFileRule())


class FuzzyCDRule(CompoundRule):
    spec = "go (folder|directory) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        query = smash_case(str(extras["text"]))
        Text("cd; cd (fd | fzf --query %s)" % query).execute()
        Key("enter").execute()
terminal_grammar.add_rule(FuzzyCDRule())


class FuzzyEditRule(CompoundRule):
    spec = "edit <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        query = smash_case(str(extras["text"]))
        Text("findedit %s)" % query).execute()
        Key("enter").execute()

terminal_grammar.add_rule(FuzzyEditRule())


class TmuxRule(MappingRule):
    mapping = {
        "rename window <text>": Key("c-b, comma") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "rename session <text>": Key("c-b, dollar") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "terminal <n>": Key("c-b, %(n)d"),
        "(disconnect|detach) session": Key("c-b, d"),
        "(jump|switch|select|choose) session": Key("c-b, w"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]

terminal_grammar.add_rule(TmuxRule())
terminal_grammar.load()


class WindowManagementRule(MappingRule):
    mapping = {
        "abort": Key("c-c"),
        "[focus] window up": Key("s-up"),
        "[focus] window down": Key("s-down"),
        "[focus] window left": Key("s-left"),
        "[focus] window right": Key("s-right"),
        "[focus] frame up": Key("ca-up"),
        "[focus] frame down": Key("ca-down"),
        "[focus] frame left": Key("ca-left"),
        "[focus] frame right": Key("ca-right"),
        "[focus] (next|other) (screen|monitor)": Key("cw-j"),
        "spank": Key("enter"),
        "(twin|double|hard) spank": Key("enter") + Pause("50") + Key("enter"),
        "yes": Key("y, enter"),
        "no": Key("n, enter"),
        "markdown bullet <text>": Key("space, asterisk, space") + Text("%(text)s") + Key("space"),
        "soft string <text>": Key("quote") + Text("%(text)s") + Key("quote"),
        "(search back|retro search) <text>": Key("c-r") + Pause("50") + Text("%(text)s"),
        "hoover [<n>]": Key("a-backspace:%(n)d"),
        "slurp [<n>]": Key("a-backspace:%(n)d"),
        "maximise": Key("w-m"),
        "say clipboard": OriginalKey("cas-e"),
        "go up": Key("up"),
        "go down": Key("down"),
        "page up": Key("pageup"),
        "page down": Key("pagedown"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 1, 9),
    ]
    defaults = {
        "n": 1,
    }

class SwitchAwesomeTagRule(CompoundRule):
    spec = "(desktop|desk|tag) <n>"
    extras = [Integer("n", 1, 9)]

    def _process_recognition(self, node, extras):
        # Focus Aenea client via AutoHotkey
        OriginalKey("cas-a").execute()

        # Switch tag
        keystroke = "cas-%s" % extras["n"]
        Key(keystroke).execute()


wm_grammar = Grammar("window management")
wm_grammar.add_rule(WindowManagementRule())
wm_grammar.add_rule(SwitchAwesomeTagRule())
wm_grammar.load()


class JarpyDebugRule(CompoundRule):
    spec = "jarpy debug"

    def _process_recognition(self, node, extras):
        # Key("w-1").execute()
        print "Jarpy do debug good!"
        speech_engine.say('Good morning.')
        speech_engine.runAndWait()


grammar = Grammar("jarpy debug")
grammar.add_rule(JarpyDebugRule())
grammar.load()

# Local Variables:
# python-shell-interpreter: "ipython2"
# flycheck-python-pycompile-executable: "python2"
# flycheck-python-pylint-executable: "python2"
# flycheck-python-flake8-executable: "python2"
# End:
