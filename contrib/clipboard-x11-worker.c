/* A worker that publishes X11 clipboard status
 */
#include <X11/Xlib.h>
#include <X11/extensions/Xfixes.h>
#include <stdio.h>

int main() {
  Display *const dpy = XOpenDisplay(0);
  const Window root = DefaultRootWindow(dpy);

  const Atom primary_selection = XInternAtom(dpy, "PRIMARY", False);

  int event_base;
  int error_base;
  if (!XFixesQueryExtension(dpy, &event_base, &error_base))
    return 1;

  XFixesSelectSelectionInput(dpy, root, primary_selection,
    XFixesSetSelectionOwnerNotifyMask |
    XFixesSelectionWindowDestroyNotifyMask |
    XFixesSelectionClientCloseNotifyMask);

  int first = !0;
  int last_owner;
  for (;;) {
    int owner = XGetSelectionOwner(dpy, primary_selection);
    if (first || owner != last_owner) {
      if (fprintf(stdout, "clip_data=%d\n", owner != None) < 0)
        break;
      fflush(stdout);
      first = 0;
      last_owner = owner;
    }

    XEvent e;
    XNextEvent(dpy, &e);
  }

  XCloseDisplay(dpy);
}
