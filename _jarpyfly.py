from dragonfly import CompoundRule, Grammar, MappingRule, Integer, Dictation, Function
from aenea.strict import Key, Text, Pause
from dragonfly import Key as OriginalKey
from aenea import ProxyAppContext as AppContext
from dragonfly.windows.clipboard import Clipboard
import pyttsx
speech_engine = pyttsx.init()


emacs_context = AppContext(title="emacs")
vscode_context = AppContext(title="Code - OSS")
gmail_context = AppContext(title="Elastic Mail")
terminal_context = AppContext(title="termite")

firefox_context = AppContext(executable="firefox")
chrome_context = AppContext(title="Google Chrome")
chromium_context = AppContext(title="Chromium")
browser_context = chrome_context | chromium_context | firefox_context


def downcase(text):
    "This thing => this thing"
    return str(text).lower()

def smash(text):
    "This thing => thisthing"
    return str(text).lower().replace(' ', '')

def kebab_case(text):
    "This thing => this-thing"
    return str(text).lower().replace(' ', '-')

def snake_case(text):
    "This thing => this_thing"
    return str(text).lower().replace(' ', '_')

# Emacs (and vscode)
emacs_grammar = Grammar("emacs", emacs_context | vscode_context)
class EmacsRule(MappingRule):
    mapping = {
        "clang": Key("c-g:5"),
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
        "start [of] line": Key("c-a"),
        "kill whole line": Key("c-a, c-a, c-k, c-k"),
        "window right": Key("s-right"),
        "window far right": Key("s-right:4"),
        "window left": Key("s-left"),
        "window far left": Key("s-left:4"),
        "window down": Key("s-down"),
        "window up": Key("s-up"),
        "open line": Key("c-e, a-o"),
        "(no no|nono)": Key("cs-minus"),
        "(duplicate|dupe|double) (line|region|that)": Key("c-c, d"),
        "(top|start) [of] buffer": Key("as-comma"),
        "(bottom|end) [of] buffer": Key("as-dot"),
        "(search forward|pro search) <text>": Key("c-s") + Text("%(text)s"),
        "(search forward|pro search)": Key("c-s"),
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
        Text(smash(extras["text"])).execute()
        # Key("enter").execute()
emacs_grammar.add_rule(FindFileRule())


class RecentFileRule(CompoundRule):
    spec = "recent file <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-c, f").execute()
        Text(smash(extras["text"])).execute()
        # Key("enter").execute()
emacs_grammar.add_rule(RecentFileRule())


class JumpBufferRule(CompoundRule):
    spec = "(jump|go|switch) buffer <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-x, b").execute()
        Text(smash(extras["text"])).execute()
        Key("enter").execute()
emacs_grammar.add_rule(JumpBufferRule())


class MetaXRule(CompoundRule):
    spec = "metaxu <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("a-x").execute()
        Text(smash(extras["text"])).execute()
        Key("enter").execute()
emacs_grammar.add_rule(MetaXRule())

emacs_grammar.load()

# Global
global_grammar = Grammar("global")

class DowncaseRule(CompoundRule):
    spec = "(flatten|lower|downcase) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text(downcase(extras["text"])).execute()
global_grammar.add_rule(DowncaseRule())


class SmashRule(CompoundRule):
    spec = "smash <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text(smash(extras["text"])).execute()
global_grammar.add_rule(SmashRule())


class KebabRule(CompoundRule):
    spec = "kebab <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text(kebab_case(extras["text"])).execute()
global_grammar.add_rule(KebabRule())


class SnakeRule(CompoundRule):
    spec = "snake <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text(snake_case(extras["text"])).execute()
global_grammar.add_rule(SnakeRule())

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
        "tab <n>": Key("a-%(n)d"),
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
        "(attach|connect) session <text>": Text("tmux attach -t %(text)s") + Key("enter"),
        "list sessions": Text("tmux list-sessions") + Key("enter"),
        "go home": Text("cd ~") + Key("enter"),
        "go source (folder|dir|directory)": Text("cd ~/src/") + Key("enter"),
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
        Text(smash(extras["text"])).execute()
terminal_grammar.add_rule(FuzzyFileRule())


class FuzzyCDRule(CompoundRule):
    spec = "go (folder|directory) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text("cd ").execute()
        Key("c-t").execute()
        Text(smash(extras["text"])).execute()
terminal_grammar.add_rule(FuzzyCDRule())


class FuzzyEditRule(CompoundRule):
    spec = "edit <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text("$EDITOR ").execute()
        Key("c-t").execute()
        Text(smash(extras["text"])).execute()
terminal_grammar.add_rule(FuzzyEditRule())


class TmuxRule(MappingRule):
    mapping = {
        "rename window <text>": Key("c-b, comma") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "rename session <text>": Key("c-b, dollar") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "terminal <n>": Key("c-b, %(n)d"),
        "(disconnect|detach) session": Key("c-b, d"),
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
        "desktop [<n>]": Key("w-%(n)d:4"),
        "[focus] window down": Key("s-down"),
        "[focus] window up": Key("s-up"),
        "[focus] window left": Key("s-left"),
        "[focus] window down": Key("s-down"),
        "[focus] (frame down|next frame|other frame|frame)": Key("w-j"),
        "[focus] (next|other) (screen|monitor)": Key("cw-j"),
        "spank": Key("enter"),
        "(twin|double|hard) spank": Key("enter/25:2"),
        "yes": Key("y, enter"),
        "no": Key("n, enter"),
        "markdown bullet <text>": Key("space, asterisk, space") + Text("%(text)s") + Key("space"),
        "browse <text>": Key("c-l") + Text("%(text)s") + Key("enter"),
        "browse history <text>": Key("c-l") + Text("%(text)s") + Key("down"),
        "(search back|retro search) <text>": Key("c-r") + Pause("50") + Text("%(text)s"),
        "hoover [<n>]": Key("a-backspace:%(n)d"),
        "slurp [<n>]": Key("a-backspace:%(n)d"),
        "maximise": Key("w-m"),
        "say clipboard": OriginalKey("cas-e"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 1, 9),
    ]
    defaults = {
        "n": 1,
    }

wm_grammar = Grammar("window magagement")
wm_grammar.add_rule(WindowManagementRule())
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