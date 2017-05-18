#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <stdio.h>

int main() {
  Display *const dpy = XOpenDisplay(0);
  const Window root = DefaultRootWindow(dpy);

  const KeyCode numlock_code = XKeysymToKeycode(dpy, XK_Num_Lock);
  XGrabKey(dpy, numlock_code, AnyModifier, root, True, GrabModeAsync,
    GrabModeAsync);
  XSelectInput(dpy, root, KeyReleaseMask);

  int first = !0;
  XKeyboardState s0;
  for (;;) {
    XKeyboardState s1;
    XGetKeyboardControl(dpy, &s1);

    if (first || s1.led_mask != s0.led_mask) {
      if (fprintf(stdout, "kb_leds=%lu\n", s1.led_mask) < 0)
        break;
      fflush(stdout);
      first = 0;
      s0 = s1;
    }

    XEvent e;
    XNextEvent(dpy, &e);
  }

  XCloseDisplay(dpy);
}
