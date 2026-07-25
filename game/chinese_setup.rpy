# Chinese translation setup for Ren'Py 7.x
# - Dialogue / names: game/chinese.rpt (auto-loaded as language "chinese")
# - UI strings: translate chinese strings (below)
# Toggle from main menu: 中文 / Русский

init -999 python:
    # Ren'Py 7 calls load_all_rpts() on every FullRestart (e.g. splash -> main menu).
    # StringTranslator.add() raises on duplicates; tolerate re-loads / repeated keys.
    import renpy.translation as _zh_translation

    _zh_orig_stl_add = _zh_translation.StringTranslator.add

    def _zh_stl_add_tolerant(self, old, new, newloc):
        if old in self.translations:
            return
        return _zh_orig_stl_add(self, old, new, newloc)

    _zh_translation.StringTranslator.add = _zh_stl_add_tolerant

    # Prefer Chinese on first launch.
    config.default_language = "chinese"

default persistent._language = "chinese"


init -1 python hide:

    def _apply_language_font():
        # Font must follow preferences.language only (same source as translations).
        if preferences.language == "chinese":
            style.default.font = "simhei.ttf"
            style.default.language = "eastasian"
        else:
            style.default.font = "DejaVuSans.ttf"
            style.default.language = "unicode"

    # Russian display names (Character(...) args in script.rpy). .rpt has Chinese.
    _CHARACTER_NAMES = (
        ("p", "Я"),
        ("g", "Попутчица"),
        ("j", "Связной"),
        ("b", "Омская Птица"),
        ("n", "Надя"),
        ("o", "Прохожий"),
        ("d", "Попутчик"),
        ("l", "Девочка"),
        ("w", "Старик"),
        ("v", "Голос"),
        ("s", "Проститутка"),
        ("sg", "Девушка"),
        ("t", "Таксист"),
        ("mc", "Ведущий"),
        ("ph", "Телефон"),
        ("j1", "Санитар 1"),
        ("j2", "Санитар 2"),
    )

    def _apply_character_names():
        # Character() bakes names at init; re-apply after language changes.
        translate = getattr(store, "_zh_translate_str", None)
        for attr, russian in _CHARACTER_NAMES:
            ch = getattr(store, attr, None)
            if ch is None or not hasattr(ch, "name"):
                continue
            if preferences.language == "chinese" and translate is not None:
                ch.name = translate(russian)
            else:
                ch.name = russian

    store._apply_language_font = _apply_language_font
    store._apply_character_names = _apply_character_names
    config.change_language_callbacks.append(_apply_language_font)
    config.change_language_callbacks.append(_apply_character_names)


# After 00defaults (init 1500) writes first-run prefs, and before init_translation
# calls _init_language(): keep menu flag and Ren'Py language in lockstep.
# Old web saves often had preferences.language=None while _language defaulted to
# "chinese" → SimHei + Russian until a manual language click.
init 1600 python hide:

    want = persistent._language
    if want == "chinese":
        _preferences.language = "chinese"
    else:
        _preferences.language = None

    _apply_language_font()
    _apply_character_names()


# Keep translate-before-% for old_substitutions + %(var)s lines (same quirk as 6.11).
# Also translate interpolated variable values and whitespace-collapsed aliases.
init 0 python:

    import re as _re

    def _zh_translate_str(s):
        if not isinstance(s, basestring):
            return s
        # Script lines often differ from .rpt by trailing spaces / doubled spaces.
        candidates = [s]
        stripped = s.strip()
        if stripped and stripped not in candidates:
            candidates.append(stripped)
        rstripped = s.rstrip()
        if rstripped and rstripped not in candidates:
            candidates.append(rstripped)
        for cand in list(candidates):
            collapsed = _re.sub(r"[ \t]+", " ", cand)
            if collapsed not in candidates:
                candidates.append(collapsed)
        for cand in candidates:
            rv = renpy.translate_string(cand, language="chinese")
            if rv != cand:
                return rv
        return s

    def _zh_alias_collapsed_keys():
        # Build collapsed/strip-key aliases into the chinese string table when possible.
        try:
            stl = renpy.game.script.translator.strings.get("chinese")
        except Exception:
            return
        if stl is None:
            return
        translations = getattr(stl, "translations", None) or getattr(stl, "str_translations", None)
        if not translations:
            return
        # StringTranslator stores via .translations dict in older code; R7 uses .translation
        mapping = getattr(stl, "translation", None)
        if mapping is None:
            mapping = translations
        extra = {}
        for old, new in list(mapping.items()):
            if not isinstance(old, basestring):
                continue
            aliases = [
                _re.sub(r"[ \t]+", " ", old),
                old.strip(),
                old.rstrip(),
                old.strip() + " ",
                old.rstrip() + " ",
            ]
            for a in aliases:
                if a and a != old and a not in mapping and a not in extra:
                    extra[a] = new
        if extra:
            for old, new in extra.items():
                renpy.translation.add_string_translation("chinese", old, new, None)

    _zh_alias_collapsed_keys()

    _TagQuotingDict = renpy.exports.TagQuotingDict
    _orig_tag_getitem = _TagQuotingDict.__getitem__

    def _tag_getitem_translated(self, key):
        rv = _orig_tag_getitem(self, key)
        if isinstance(rv, basestring) and preferences.language == "chinese":
            store = vars(renpy.store)
            if key in store and isinstance(store[key], basestring):
                rv = _zh_translate_str(store[key]).replace("{", "{{")
        return rv

    _TagQuotingDict.__getitem__ = _tag_getitem_translated

    _original_exports_say = renpy.exports.say

    def _exports_say_translate_first(who, what, interact=True, *args, **kwargs):
        if preferences.language == "chinese" and isinstance(what, basestring):
            what = _zh_translate_str(what)
            old = renpy.config.old_substitutions
            if old and isinstance(what, basestring):
                what = what % renpy.exports.tag_quoting_dict
                renpy.config.old_substitutions = False
                try:
                    return _original_exports_say(who, what, interact=interact, *args, **kwargs)
                finally:
                    renpy.config.old_substitutions = old
        return _original_exports_say(who, what, interact=interact, *args, **kwargs)

    renpy.exports.say = _exports_say_translate_first


init 1 python hide:

    def _language_chinese():
        persistent._language = "chinese"
        renpy.change_language("chinese")
        # Classic main_menu builds ui.buttons once; restart_interaction does not
        # rebuild their labels. Re-enter the screen so _(label) is reapplied.
        renpy.jump("main_menu_screen")

    def _language_russian():
        persistent._language = None
        renpy.change_language(None)
        renpy.jump("main_menu_screen")

    config.main_menu = [
            ("Начать игру", "start", "True"),
            ("Загрузить", _intra_jumps("load_screen", "main_game_transition"), "True"),
            ("Настройки", _intra_jumps("preferences_screen", "main_game_transition"), "True"),
            ("Местные", "locals", "persistent.seen_locals != None"),
            ("Грибы", "video", "persistent.seen_video != None"),
            ("Омск", "ending", "persistent.seen_ending != None"),
            # Use Latin "Chinese" so DejaVu can render it in Russian mode;
            # translate chinese strings maps it to 「中文」.
            ("Chinese", _language_chinese, "True"),
            ("Русский", _language_russian, "True"),
            ("О проекте", "about_notice", "True"),
            ("Выйти", ui.jumps("_quit"), "True"),
        ]


# UI string translations (menu / common)
translate chinese strings:

    old "Chinese"
    new "中文"

    old "О проекте"
    new "关于/声明"

    old "Начать игру"
    new "开始游戏"

    old "Загрузить"
    new "读取"

    old "Настройки"
    new "设置"

    old "Местные"
    new "「当地人」"

    old "Грибы"
    new "「蘑菇」"

    old "Омск"
    new "「鄂木斯克」"

    old "Выйти"
    new "退出"

    old "Return"
    new "返回"

    old "Preferences"
    new "设置"

    old "Save Game"
    new "保存游戏"

    old "Load Game"
    new "读取游戏"

    old "Main Menu"
    new "主菜单"

    old "Quit"
    new "退出"

    old "Yes"
    new "是"

    old "No"
    new "否"

    old "Empty Slot."
    new "空存档。"

    old "Previous"
    new "上一页"

    old "Next"
    new "下一页"

    old "Page"
    new "页"

    old "Auto"
    new "自动"

    old "Quick"
    new "快速"

    old "Display"
    new "显示"

    old "Window"
    new "窗口"

    old "Fullscreen"
    new "全屏"

    old "Transitions"
    new "转场"

    old "All"
    new "全部"

    old "Some"
    new "部分"

    old "None"
    new "无"

    old "Skip"
    new "快进"

    old "Seen Messages"
    new "已读"

    old "All Messages"
    new "全部"

    old "Begin Skipping"
    new "开始快进"

    old "After Choices"
    new "选项之后"

    old "Stop Skipping"
    new "停止快进"

    old "Keep Skipping"
    new "继续快进"

    old "Text Speed"
    new "文字速度"

    old "Auto-Forward Time"
    new "自动前进时间"

    old "Music Volume"
    new "音乐音量"

    old "Sound Volume"
    new "音效音量"

    old "Voice Volume"
    new "语音音量"

    old "Joystick..."
    new "手柄…"

    old "Loading will lose unsaved progress.\nAre you sure you want to do this?"
    new "读取将丢失未保存进度。\n确定要继续吗？"

    old "Are you sure you want to quit?"
    new "确定要退出吗？"

    old "Are you sure you want to return to the main menu?\nThis will lose unsaved progress."
    new "确定要返回主菜单吗？\n未保存的进度将会丢失。"

    old "Skip Mode"
    new "快进模式"

    old "Fast Skip Mode"
    new "快速快进模式"
