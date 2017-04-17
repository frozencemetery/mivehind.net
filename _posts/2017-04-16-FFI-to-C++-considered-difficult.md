---
layout: post
tags:
  - tech
---

As was perhaps inevitable, I've combined two of my current interests.  So
here's a Rust program that uses the current version (0.1.2/0.1.3) of the
[QT5 bindings](https://github.com/rust-qt) to make a simple interface:

```rust
extern crate cpp_utils;
extern crate qt_core;
extern crate qt_widgets;

use cpp_utils::{AsBox, StaticCast};

use qt_core::connections::Signal;
use qt_core::slots::SlotNoArgs;
use qt_core::string::String;

use qt_widgets::application::Application;
use qt_widgets::push_button::PushButton;
use qt_widgets::qvb_ox_layout::QvbOxLayout as VBoxLayout;
use qt_widgets::widget::Widget;

fn glom<T>(ptr: *mut T) -> &'static mut T {
    unsafe { ptr.as_mut() }.expect("null pointer in glom")
}

fn main() {
    Application::create_and_exit(|_| {
        let mut widget = Widget::new(AsBox);
        let mut layout = VBoxLayout::new((widget.as_mut_ptr(), AsBox));
        let mut button = PushButton::new((&String::from("Quit"), AsBox));

        button.set_enabled(true);

        layout.add_widget(button.static_cast_mut() as *mut _);

        widget.resize((250, 150));
        widget.set_window_title(&String::from("QEMU"));
        widget.show();

        let b_ref = button.into_raw();

        let on_click = SlotNoArgs::new(|| {
            glom(b_ref).set_enabled(false) };
            Application::quit()
        });

        glom(b_ref).signals().clicked().connect(&on_click);

        Application::exec()
    });
}
```

So there's a lot to unpack here.  I should probably start by saying that
Rust's C Foreign-Function Interface (FFI) is "fine" - that is, it works, and it's
fairly straightforward to use, but it's not particularly brilliant or even
novel.  Next, QT is not a C library; rather, it is many C++ libraries.
Which is to say that the Rust FFI is not designed for this.  Actually, now
might be a good time to break out the C++ version of this for comparison:

```C++
#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class VerticalBox : public QWidget {
public:
    VerticalBox(QApplication *app, QWidget *parent = 0);

private slots:
    void OnClick();

private:
    QPushButton *quit;
    QApplication *app;
};

VerticalBox::VerticalBox(QApplication *app, QWidget *parent): QWidget(parent) {
    QVBoxLayout *vbox = new QVBoxLayout(this);

    QPushButton *quit = new QPushButton("quit");
    quit->setEnabled(true);
    vbox->addWidget(quit);

    connect(quit, &QPushButton::clicked, this, &VerticalBox::OnClick);

    setLayout(vbox);

    this->quit = quit;
    this->app = app;
}

void VerticalBox::OnClick() {
    quit->setEnabled(false);
    app->exit();
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    VerticalBox window(&app);
    window.resize(250, 150);
    window.setWindowTitle("QEMU");
    window.show();

    return app.exec();
}
```

Now that I've thoroughly upset the syntax highlighting of both my blog and my
editor, let me call out a few things.  First, this is a semi-contrived
example: a real application would probably not care about disabling the quit
button before quitting the application itself.  Second, the boilerplate for
both users of QT is about the same: there's an entire other file for QT
dependency management in C++, but the Rust code has a longer prelude.  (For
more on building QT in C++, see
[this post](https://mivehind.net/2017/04/02/On-compatibility-by-design/) in
the unlikely event that you stumble across this post and want minutiae from
someone who doesn't know the project history).

As for the build process itself, the C++ is substantially faster but much more
fiddly.  In a C++ context, I'm making use of my distro's header files and
shared objects, so it only takes a few seconds.  In the Rust context, though,
there isn't a strong notion of shared objects yet: I have to download each
crate and build it from source before it's (statically) linked into my
binary.  I understand there is work being done on this, but because these
crates only have to be built once, the hour (!!!) overhead on the first build
here isn't a huge issue (since it never happens again).  It also "just
worked™" - I didn't have to do anything special beyond the normal rust process.

Part of the reason the Rust build is slower than it might otherwise be is that
it dynamically generates the bindings.  The rust-qt folk have a tool for
automatically generating bindings to C++ libraries, which is nice because QT
has an enormous number of functions.  The drawback is that there are several
warts over the calling code.  For instance, QT has its own type for Strings,
so there's a lot of `&String::from`; Rust's trait system can be used to fix
this, but it must be done by hand.  Ditto the awkwardness of taking a tuple as
an argument.

There are also a couple of (what I imagine must be) bugs in its naming; the
one I'm highlighting is the transition from the C++ type `QVBoxLayout` to the
Rust type `qvb_ox_layout::QvbOxLayout`.  Which leads nicely into the point I
want to highlight, which is how poorly the inheritance is getting handled
here.  In the C++ code, my `VerticalBox` object inherits from the `QWidget`
parent class, and so I can define my own, custom, widgets easily; in the Rust,
though, there's no such convenience, and my custom widgets have to hold their
own widget object inside them.

This leads directly to the two uses of `unsafe` in this code (which happen to
both be safe, thankfully) that I've highlighted in the `glom` function.
Within the `on_click` callback, we'd really like to do, as we do in the C++
case, manipulate part of our state (button).  However, if we do so, then
button is moved to within the closure, and I can't wire it to `connect` after.
And I can't reverse the order that these things are declared in, because then
the callback won't be initialized at time of reistration!  (As for the "slots"
abstraction itself, I will not defend the way QT implements this in C++, so
it's not at all surprising that it's ugly in Rust as well.)

For a 0.1-series release, it's impressive that this works at all.  Going
forward, a more powerful FFI is something Rust really needs to work on, even
if it requires some knowledge of how C++ works.  I'm hopeful that this might
actually be a priority for Mozilla because the *Monkey JavaScript JITs have
only a C++ interface; however, right now I believe they're using a (different)
binding generator tool for Servo.  I think it's sufficiently clear that a
better story for handling inheritance is needed, at the very least.

### Attribution

The code in this post is adapted from both
[the Rust-QT example](https://github.com/rust-qt/qt_widgets/blob/master/examples/form1.rs)
and [Jan Bodnar's QT5 tutorial](http://zetcode.com/gui/qt5/).  I promise that
this is just code for me learning the tools and that I am not
[going dark](https://blog.codinghorror.com/dont-go-dark/).
