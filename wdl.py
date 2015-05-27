import weechat as w
import re
import os.path

SCRIPT_NAME = "wdl"
SCRIPT_AUTHOR = "Luca Ognibene <luca.ognibene@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "auto download irc"

CHANNEL = "#serie.tv.sub-ita"
CMDPATH = "/getitcmd.txt"


def get_cmd():
    cmd = ""
    if os.path.exists(CMDPATH):
        with open(CMDPATH) as f:
            cmd = f.read().strip()
    return cmd


def connected_cb(data, signal, signal_data):
    w.command("", "/join %s" % CHANNEL)
    w.command("", )
    return w.WEECHAT_RC_OK


def join_cb(data, signal, signal_data):
    # signal is for example: "freenode,irc_in2_join"
    # signal_data is IRC message, for example: ":nick!user@host JOIN :#channel"
    nick = w.info_get("irc_nick_from_host", signal_data)
    server = signal.split(",")[0]
    channel = signal_data.split(":")[-1]
    ownNick = w.info_get("irc_nick", server)
    if ownNick == nick:
        buffer = w.info_get("irc_buffer", "%s,%s" % (server, channel))
        if buffer:
            cmd = get_cmd()
            if cmd:
                w.command("", cmd)
            else:
                w.prnt("", "Empty CMD")
                w.command("", "/quit")
    return w.WEECHAT_RC_OK


def cb_process_message(data, wbuffer, date, tags, displayed, highlight, prefix, message):
    # process message: weechat |  | xfer: file WIFI.Signal.Strength.Premium.v9.2.0.MULTI-Up.By-CaMik.rar received from MaLeFiC|ANDRoiD|01 (91.121.178.115): OK | set([''])
    # w.prnt("", "process message: %s | %s | %s | %s" % (buffer_name, prefix, message, str(tags)))
    r = re.findall("xfer: file (.+?) received from .+?: (.+?)$", message)
    if r:
        (f, status) = r[0]
        w.command("", "/quit")
    return w.WEECHAT_RC_OK
    

def timer_cb(data, remaining_calls):
    return w.WEECHAT_RC_OK


w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
           SCRIPT_LICENSE, SCRIPT_DESC, "", "")
w.hook_signal("irc_server_connected", "connected_cb", "")
w.hook_signal("*,irc_in2_join", "join_cb", "")
# w.hook_timer(1000, 0, 0, "timer_cb", "")
w.hook_print('', '', '', 1, 'cb_process_message', '')
