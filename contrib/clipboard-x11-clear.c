/* Clear the X11 clipboard
 */
#include <X11/Xlib.h>

int main() {
  Display *const dpy = XOpenDisplay(0);
  const Window root = DefaultRootWindow(dpy);

  const Atom primary_selection = XInternAtom(dpy, "PRIMARY", False);
  XSetSelectionOwner(dpy, primary_selection, None, CurrentTime);

  XCloseDisplay(dpy);
}
