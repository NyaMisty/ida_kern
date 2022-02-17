# adapted from https://gist.github.com/williballenthin/b5e7a80691ed5e44e7fea1964bae18dc

import idc
import idaapi
import idautils

from ctypes import *

import ida_kern
k = ida_kern.IDAKern()
k.init()

HookCb = k.hook_to_notification_point.argtypes[1]

def do_callui(uicode, *args):
    ret = k.callui(uicode, *[c_void_p(c) for c in args])
    return ret

class CalluiHookPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = "Callui Hook Example"

    help = "Callui Hook Example"
    wanted_name = "CalluiHookExample"

    def init(self):
        import datetime
        self.bypassing = False
        #self.logfile = open('ui_notify.log', 'w')

        # can't use a bound method as a callback (since `self` doesn't get provided)
        #  so we'll create a closure that has access to `self`.
        # 
        # via: http://stackoverflow.com/a/7261524/87207
        def cb(user_data, notification_code, va_list):
            if self.bypassing:
                return 0
            if notification_code == k.ui_ask_str:
                print('ui_ask_str:')
                print('>.. notification code: %s' % (notification_code))
                print('>.. va_list: %s' % (va_list))
                print('>.. args: %s' % (va_list[:3],))
                prompt = cast(va_list[2], c_char_p)
                print('>.. prompt: %s' % prompt.value)
                if prompt.value == b'Please enter the type declaration':
                    self.bypassing = True
                    callui_ret = do_callui(notification_code, *va_list[:4]).cnd
                    self.bypassing = False
                    val = cast(va_list[0], POINTER(k.qstring))[0]
                    if val.body.array:
                        print("userInput: %s" % val)
                    if callui_ret[0]:
                        return 1
                    return 0 # there's no way to tell IDA that user has cancelled in this event, that's IDA's fault
            elif notification_code == k.ui_ask_form:
                print('ui_ask_form:')
                print('>.. notification code: %s' % (notification_code))
                print('>.. va_list: %s' % (va_list))
                print('>.. args: %s' % (va_list[:2],))
                form = cast(va_list[0], c_char_p)
                print('>.. form: %s' % form.value)
                if form.value == b'@0:0[]\nPlease enter a string\n\n <Please enter the type declaration:y:-1:80::>\n\n':
                    self.bypassing = True
                    callui_ret = do_callui(notification_code, *va_list[:2]).cnd
                    self.bypassing = False
                    print(callui_ret[0])
                    if callui_ret[0] != 1:
                        # but we can tell IDA user's cancellation here with value other than 0 and 1
                        return 2 if not callui_ret[0] else callui_ret[0]
                    # va_list: callui's argument list, supplied by hook_to_notification_point
                    ask_form_va = cast(va_list[1], POINTER(c_void_p))
                    # ask_form_va: ask_form's argument list, supplied by vask_form
                    qstr_out = cast(ask_form_va[0], POINTER(k.qstring))[0]
                    val = qstr_out.body.array
                    if val:
                        print("userInput: %s" % val)
                    return 1
            elif notification_code == k.ui_mbox:
                print('ui_mbox:')
                print('>.. notification code: %s' % (notification_code))
                print('>.. va_list: %s' % (va_list))
                print('>.. args: %s' % (va_list[:3],))
                prompt = cast(va_list[1], c_char_p)
                print('>.. prompt: %s' % prompt.value)

            return 0


        # need to keep a ref around, or the function gets garbage collected
        self.cb = HookCb(cb)

        # need to keep a ref around, or the param gets garbage collected
        self.ctx = c_long(69)

        return idaapi.PLUGIN_OK

    def run(self, arg):
        print('hints: run')
        k.hook_to_notification_point(k.HT_UI, self.cb, byref(self.ctx))

    def term(self):
        print('hints: term')
        k.unhook_from_notification_point(k.HT_UI, self.cb, byref(self.ctx))

try:
    plug.term()
except:
    pass
plug = CalluiHookPlugin()
plug.init()
plug.run(0)