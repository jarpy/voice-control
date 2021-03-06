# -*- coding: utf-8 -*-

from dragonfly import CompoundRule, Grammar, MappingRule, Integer, Dictation, Function
from aenea.strict import Key, Text, Pause, Mouse
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
vscode_context = vscode_linux_context | vscode_windows_context

gmail_context = AppContext(title="Elastic Mail")
slack_context = AppContext(title="Slack")
terminal_context = AppContext(title="termite")
virtualbox_context = AppContext(title="Oracle VM VirtualBox")

firefox_linux_context = AppContext(executable="firefox")
firefox_windows_context = AppContext(title="Mozilla Firefox")
discord_context = AppContext(title="Discord")
chrome_context = AppContext(title="Google Chrome")
chromium_context = AppContext(title="Chromium")
browser_context = chrome_context | chromium_context | firefox_linux_context | firefox_windows_context

#dcs_context = AppContext(title='Digital Combat Simulator'
dcs_context = AppContext(executable="dcs.exe")

def focus_aenea_client():
    """Ensure the Aenea client has focus in the Windows VM"""
    # Triggers an AutoHotkey script that must be running.
    OriginalKey("cas-a").execute()

def switch_awesome_tag(n):
    """Switch to Awesome tag number n"""
    focus_aenea_client()
    keystroke = "cas-%s" % n
    Key(keystroke).execute()

def focus_visual_studio_code():
    """Focus (and raise) Visual Studio Code in the Windows VM"""
    switch_awesome_tag(3)
    Pause("20").execute()
    # Trigger an AutoHotkey script that must be running.
    OriginalKey("cas-c").execute()

def focus_terminal():
    focus_aenea_client()
    Key("cas-1").execute()
    Pause("20").execute()

def down_case(text):
    "This thing => this thing"
    print "down_case <- %s" % text
    return str(text).lower()

def smash_case(text):
    "This thing => thisthing"
    print "smash_case <- %s" % text
    return str(text).lower().replace(' ', '')

def kebab_case(text):
    "This thing => this-thing"
    print "kebab_case <- %s" % text
    return str(text).lower().replace(' ', '-')

def snake_case(text):
    "This thing => this_thing"
    print "snake_case <- %s" % text
    return str(text).lower().replace(' ', '_')

def screaming_snake_case(text):
    "This thing => THIS_THING"
    print "screaming_snake_case <- %s" % text
    return snake_case(text).upper()

def title_case(text):
    "This thing => This Thing"
    print "title_case <- %s" % text
    return str(text).title()

def pascal_case(text):
    "This thing => ThisThing"
    print "pascal_case <- %s" % text
    return title_case(text).replace(" ", "")

def nato_to_char(text):
    print "nato_to_char <- %s" % text

    fixups = {
        "if one": "f1",
        "of one": "f1",
        "oh one": "f1",
        "if won": "f1",
        "of won": "f1",
        "oh won": "f1",
        "if too": "f2",
        "of too": "f2",
        "if two": "f2",
        "of two": "f2",
        "oh two": "f2",
        "if three": "f3",
        "of three": "f3",
        "oh three": "f3",
        "if for": "f4",
        "of for": "f4",
        "if four": "f4",
        "of four": "f4",
        "oh four": "f4",
        "if five": "f5",
        "of five": "f5",
        "oh five": "f5",
        "if six": "f6",
        "of six": "f6",
        "oh six": "f6",
        "if seven": "f7",
        "of seven": "f7",
        "oh seven": "f7",
        "if ate": "f8",
        "of ate": "f8",
        "oh ate": "f8",
        "if eight": "f8",
        "of eight": "f8",
        "oh eight": "f8",
        "if nine": "f9",
        "of nine": "f9",
        "oh nine": "f9",
        "if ten": "f10",
        "of ten": "f10",
        "oh ten": "f10",
        "if eleven": "f11",
        "of eleven": "f11",
        "oh eleven": "f11",
        "if twelve": "f12",
        "of twelve": "f12",
        "oh twelve": "f12",
    }

    nato_alphabet = {
        'alpha': 'a',
        'alfa': 'a',
        'offer': 'a',
        'bravo': 'b',
        'charlie': 'c',
        'delta': 'd',
        'echo': 'e',
        'ecco': 'e',
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
        'decimal': '.',
        # "Fake" phonetics
        'escape': 'escape',
        'space': 'space',
        'enter': 'enter',
        'up': 'pgup',
        'down': 'pgdown',
        'hash': '#',
        'pipe': '|',
        'tab': 'tab',
        'untab': 's-tab',
        'backslash': 'backslash',
        'f1': 'f1',
        'f2': 'f2',
        'f3': 'f3',
        'f4': 'f4',
        'f5': 'f5',
        'f6': 'f6',
        'f7': 'f7',
        'f8': 'f8',
        'f9': 'f9',
        'f10': 'f10',
        'f11': 'f11',
        'f12': 'f12',
    }

    text = text.lower()
    try:
        fix = fixups[text]
        print "nato_to_char fixup '%s' -> '%s'" % (text, fix)
        text = fix
    except KeyError:
        pass

    phonetics = text.split()
    glyphs = []
    for phonetic in phonetics:
        try:
            glyphs.append(nato_alphabet[phonetic])
        except KeyError:
            glyphs.append("#")  # FIXME: make a noise
    print "nato_to_char -> %s" % glyphs
    return glyphs

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
        "balance windows": Key("c-x, plus"),
        "(kill|close) window": Key("c-x, 0"),
        "kill buffer": Key("c-x, k"),
        "kill word": Key("a-d"),
        "save [buffer]": Key("c-x, c-s"),
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
        "jump window": Key("c-x, o"),
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
        "occurrences": Key("c-o"),
        "(mark|set mark)": Key("cas-space"),
        "jump line": Key("c-c, f6, l"),
        "jump word": Key("c-c, f6, w"),
        "(show|list) buffers": Key("c-x, c-b"),
        "untab": Key("s-escape"),
    }

    extras = [
        Dictation("text"),
        Integer("n", 1, 9),
    ]
emacs_grammar.add_rule(EmacsRule())


class JumpWord1Rule(CompoundRule):
    spec = "jump word <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        print "JumpWord1Rule: " + str(extras["text"])
        Key("c-c, f6, e").execute()
        Pause("20").execute()
        Key(nato_to_char(str(extras["text"]))[0]).execute()
emacs_grammar.add_rule(JumpWord1Rule())

class FindFileRule(CompoundRule):
    spec = "(find|open) file <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("c-x, c-f").execute()
        Text(smash_case(extras["text"])).execute()
        # Key("enter").execute()
emacs_grammar.add_rule(FindFileRule())


class RecentFileRule(CompoundRule):
    spec = "[(find|open)] recent file <text>"
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
    spec = "(smash|smashcase) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(smash_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(SmashRule())


class KebabRule(CompoundRule):
    spec = "(kebabcase|kebab|shawarma) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(kebab_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(KebabRule())


class SnakeRule(CompoundRule):
    spec = "(snakecase|snake|serpent|parselmouth|parseltongue) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(snake_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(SnakeRule())


class ScreamingSnakeRule(CompoundRule):
    spec = "(screaming|loud|shout|shouting|noisy) (snakecase|snake|serpent|parselmouth|parseltongue) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(screaming_snake_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(ScreamingSnakeRule())


class TitleRule(CompoundRule):
    spec = "(title|title case) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(title_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(TitleRule())


class PascalRule(CompoundRule):
    spec = "(pascal|pascal case|smash title) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        t = Text(pascal_case(str(extras["text"])))
        t.execute()
global_grammar.add_rule(PascalRule())


class NatoRule(CompoundRule):
    spec = "(nato|type|press|punch|push) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
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
        "read [that]": Key("o"),
        "(expand|show all)": Key(";"),
    }
gmail_grammar = Grammar("gmail", gmail_context)
gmail_grammar.add_rule(GmailRule())
gmail_grammar.load()


class DiscordRule(MappingRule):
    mapping = {
        "[discord] channel": Key("escape, c-k") + Text("%(text)s"),
    }
discord_grammar = Grammar("discord", discord_context)
discord_grammar.add_rule(DiscordRule())
discord_grammar.load()


class BrowserRule(MappingRule):
    mapping = {
        "top": Key("home"),
        "bottom": Key("end"),
        "down": Key("pgdown"),
        "up": Key("pgup"),
        "links": Key("escape") + Pause("10") + Key("f"),
        "go back": Key("escape") + Pause("10") + Key("s-h"),
        "go forward": Key("escape") + Pause("10") + Key("s-l"),
        "open <text>": Key("a-home") + Pause("50") + Key("escape") + Pause("10") + Key("o") + Pause("10") + Text("%(text)s"),
        "(search|google) [for] <text>": Key("a-home") + Pause("50") + Text("%(text)s"),
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
        #"slack channel <text>": Key("c-k") + Text("%(text)s"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]

browser_grammar = Grammar("browser", browser_context)
browser_grammar.add_rule(BrowserRule())
browser_grammar.load()


class SlackRule(MappingRule):
    mapping = {
        "[slack] channel <text>": Key("escape, c-k") + Text("%(text)s"),
        "(quit|leave|part|close) channel": Text("/leave") + Key("enter"),
        "Mark [channel] read": Key("escape, escape"),
    }
    extras = [
        Dictation("text"),
    ]
slack_grammar = Grammar("slack", slack_context)
slack_grammar.add_rule(SlackRule())
slack_grammar.load()


# DCS
def radio_menu(*args):
    keys = ["backslash/20"]
    for number in args:
        keys.append("f%s/20" % number)
    key_spec = ", ".join(keys)

    print "radio_menu -> Key('%s')" % key_spec
    return Key(key_spec)

def ctld(*args):
    """Operate the CTLD radio menu in DCS.

    Takes integers as args, specifying the CTLD sub-menu options to select.
    """
    keys = ["backslash/20", "f10/20", "f6/20"]
    for number in args:
        keys.append("f%s/20" % number)
    key_spec = ", ".join(keys)

    print "ctld -> Key('%s')" % key_spec
    return Key(key_spec)


dcs_grammar = Grammar("dcs", dcs_context)
class DCSRule(MappingRule):
    mapping = {
        "radio": Key("backslash"),
        "radio <n>": Key("f%(n)d"),
        "(radio exit|exit radio)": Key("f12"),
        "refuel and rearm": radio_menu(8, 1),
        "request repair": radio_menu(8, 3),
        "ground power (on|connect|attach)": radio_menu(8, 2, 1),
        "ground power (off|disconnect|remove|attach)": radio_menu(8, 2, 2),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
dcs_grammar.add_rule(DCSRule())

class CTLDRule(MappingRule):
    mapping = {
        "load anti (air|airaft) troops": ctld(1, 4),
        "load anti tank troops": ctld(1, 5),
        "load mortar (squad|troops|crew)": ctld(1, 5),

        "unpack crate": ctld(6, 1),
        "drop crate":   ctld(6, 2),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
dcs_grammar.add_rule(CTLDRule())
dcs_grammar.load()


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
        "(rerun last|do again|do it again|run again)": Key("up, enter"),
        "(git|get) reset hard": Text("git reset --hard") + Key("enter"),
        "(git|get|show) diff": Text("git diff") + Key("enter"),
        "(git|get|show) status": Text("git status") + Key("enter"),
        "(git|get) stash": Text("git stash") + Key("enter"),
        "[(git|get)] (stash pop|pop stash)": Text("git stash pop") + Key("enter"),
        "[(git|get)] (stash show|show stash)": Text("git stash show -p") + Key("enter"),
        "(git|get) pull": Text("git pull") + Key("enter"),
        "(git|get) fetch [all]": Text("git fetch --all") + Key("enter"),
        "[show] (git|get) log": Text("fzf-git-log") + Key("enter"),
        "[(git|get)] commit [patch]": Text("git commit -p") + Key("enter"),
        "[(git|get)] push": Text("git push") + Key("enter"),
        "[(git|get)] push force": Text("git push --force"),
        "[(git|get)] push [(this|new)] branch [to origin]": Text("git push -u origin (git rev-parse --abbrev-ref HEAD)") + Key("enter"),
        "[(git|get)] rebase on master": Text("git fetch origin && git rebase origin/master") + Key("enter"),
        "[(git|get)] rebase abort": Text("git rebase --abort") + Key("enter"),
        "[(git|get)] commit all": Text("git commit --all") + Key("enter"),
        "abort [(git|get)] rebase": Text("git rebase --abort") + Key("enter"),

        "chudder": Key("a-g"),
        "(chudder|folder|directory|go) home": Text("cd ~") + Key("enter"),
        "(chudder|folder|directory) up": Text("cd ..") + Key("enter"),

        "Lang Lang": Text("exa -la") + Key("enter"),

        "(show|list) [docker] containers": Text("docker ps -a") + Key("enter"),
        "show environment": Text("env") + Key("enter"),

        "(show|list) tasks": Text("task ls") + Key("enter"),

        "grep [for] <text>": Text("rg %(text)s") + Key("enter"),
        "grep that for <text>": Key("c-p") + Text(" | rg -i %(text)s") + Key("enter"),

        "findedit <text>": Text("findedit %(text)s") + Key("enter"),
        "grepedit <text>": Text("grepedit %(text)s") + Key("enter"),
        "findedit <text> here": Text("findedit %(text)s $PWD") + Key("enter"),
        "grepedit <text> here": Text("grepedit %(text)s $PWD") + Key("enter"),

        "(switch|google|cube|kubernetes|kates) project": Text("kzf-project") + Key("enter"),
        "(switch|google|cube|kubernetes|kates) project <text>": Text("kzf-project %(text)s") + Key("enter"),
        "(switch|cube|kubernetes|kates) cluster": Text("kzf-cluster") + Key("enter"),
        "(switch|cube|kubernetes|kates) cluster <text>": Text("kzf-cluster %(text)s") + Key("enter"),
        "(switch|cube|kubernetes|kates) namespace": Text("kzf-namespace") + Key("enter"),
        "(switch|cube|kubernetes|kates) namespace <text>": Text("kzf-namespace %(text)s") + Key("enter"),
        "(cube|kubernetes|kates) get pods": Text("kubectl get pods") + Key("enter"),

        "tail (pod|log|logs)":        Text("kzf-tail") + Key("enter"),
        "tail (pod|log|logs) <text>": Text("kzf-tail %(text)s") + Key("enter"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
terminal_grammar.add_rule(BashRule())


class GitBranchRule(CompoundRule):
    spec = "(git|get|new|create) branch <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text("git branch ").execute()
        Text(kebab_case(extras["text"])).execute()
        Key("enter").execute()
terminal_grammar.add_rule(GitBranchRule())


class GitCheckoutRule(CompoundRule):
    spec = "[(git|get)] checkout [branch] <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Text("git checkout ").execute()
        Text(kebab_case(extras["text"])).execute()
        Key("enter").execute()
terminal_grammar.add_rule(GitCheckoutRule())


class FuzzyFileRule(CompoundRule):
    spec = "fuzzy <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        Key("space, c-t").execute()
        Text(smash_case(extras["text"])).execute()
terminal_grammar.add_rule(FuzzyFileRule())


class FuzzyCDRule(CompoundRule):
    spec = "(chudder|folder|directory) <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        query = smash_case(str(extras["text"]))
        Key("a-g").execute()
        Pause("50").execute()
        Text(query).execute()
terminal_grammar.add_rule(FuzzyCDRule())


class FuzzyEditRule(CompoundRule):
    spec = "edit <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        query = smash_case(str(extras["text"]))
        focus_terminal()
        Text("findedit ").execute()
        Text(query).execute()
        Key("enter").execute()
terminal_grammar.add_rule(FuzzyEditRule())


class TmuxRule(MappingRule):
    mapping = {
        "(connect|attach) [session]": Text("tmux attach") + Key("enter"),
        "new (window|tab|shell|terminal)": Key("c-b, c"),
        "rename (window|tab|shell|terminal) <text>": Key("c-b, comma") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "rename session <text>": Key("c-b, dollar") + Key("backspace:50") + Text("%(text)s") + Key("enter"),
        "(window|shell|terminal) <n>": Key("c-b, %(n)d"),
        "(disconnect|detach) session": Key("c-b, d"),
        "(jump|switch|select|choose) session": Key("c-b, w"),
        "switch": Key("c-b, w"),
        "switch <n>": Key("c-b, %(n)d"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 0, 9),
    ]
terminal_grammar.add_rule(TmuxRule())
terminal_grammar.load()


wm_grammar = Grammar("window management")
class WindowManagementRule(MappingRule):
    mapping = {
        "abort": Key("c-c"),
        "escape": Key("escape"),
        "(twin|double) escape": Key("escape, escape"),
        "[focus] window up": Key("s-up"),
        "[focus] window down": Key("s-down"),
        "[focus] window left": Key("s-left"),
        "[focus] window right": Key("s-right"),
        "[focus] frame up": Key("ca-up"),
        "[focus] frame down": Key("ca-down"),
        "[focus] frame left": Key("ca-left"),
        "[focus] frame right": Key("ca-right"),
        "(make master|master frame|frame master|center frame)": Key("ca-enter"),
        "left master": Key("ca-left, ca-left, ca-enter"),
        "right master": Key("ca-right, ca-right, ca-enter"),
        "[focus] (next|other) (screen|monitor)": Key("cw-j"),
        "spank": Key("enter"),
        "(twin|double|hard) spank": Key("enter") + Pause("50") + Key("enter"),
        "yes": Key("y, enter"),
        "no": Key("n, enter"),
        "markdown bullet <text>": Key("space, asterisk, space") + Text("%(text)s") + Key("space"),
        "soft string <text>": Key("quote") + Text("%(text)s") + Key("quote"),
        "(search back|retro search)": Key("c-r"),
        "(search back|retro search) <text>": Key("c-r") + Pause("50") + Text("%(text)s"),
        "hoover [<n>]": Key("a-backspace:%(n)d"),
        "slurp [<n>]": Key("a-backspace:%(n)d"),
        "maximise": Key("w-m"),
        "say clipboard": OriginalKey("cas-e"),
        "go up": Key("up"),
        "go down": Key("down"),
        "go [to the] (top|start)": Key("home"),
        "go [to the] (bottom|end)": Key("end"),
        "page up": Key("pgup"),
        "page down": Key("pgdown"),
        "cut [that]": Key("c-x"),
        "copy [that]": Key("c-c"),
        "shift copy [that]": Key("cs-c"),
        "Delete [that]": Key("delete"),
        "paste [that]": Key("c-v"),
        "Tabular": Key("tab"),
        "Twin tabular": Key("tab") + Pause("10") + Key("tab"),

        "[left] click": Mouse("left"),
        "(right click|crick)": Mouse("right"),
        "middle click": Mouse("middle"),
    }
    extras = [
        Dictation("text"),
        Integer("n", 1, 9),
    ]
    defaults = {
        "n": 1,
    }
wm_grammar.add_rule(WindowManagementRule())

class SwitchAwesomeTagRule(CompoundRule):
    spec = "(desktop|desk|tag) <n>"
    extras = [Integer("n", 1, 9)]

    def _process_recognition(self, node, extras):
        switch_awesome_tag(extras["n"])
wm_grammar.add_rule(SwitchAwesomeTagRule())

class FocusVisualStudioCodeRule(CompoundRule):
    spec = "focus [visual studio] code"
    def _process_recognition(self, node, extras):
        focus_visual_studio_code()
wm_grammar.add_rule(FocusVisualStudioCodeRule())

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
