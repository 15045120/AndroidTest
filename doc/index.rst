========================
Android Test API
========================

>>> switch_device(device)

:description:
  switch to the Android Phone by serial-number
:device:
  The serial-number of Android Phone(adb devices).

------------

>>> assert_exists(template_pic, threshold=0.9, device=None, timeout=10)

:description:
 throw a Error if template picture is not in current screen of Android Phone
:template_pic:
  The object of Template class
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> assert_not_exists(template_pic, threshold=0.9, device=None, timeout=10)

:description:
 throw a Error if template picture is in current screen of Android Phone
:template_pic:
  The object of Template class
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> exists(template_pic, threshold=0.9, device=None, timeout=10)

:description:
  return True is template picture is in current screen of Android Phone, else return Flase
:template_pic:
  The object of Template class
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> touch(template_pic, threshold=0.9, device=None, delay=0.4, timeout=10)

:description:
  touch template picture,throw a Error if template picture is not in current screen of Android Phone
:template_pic:
  The object of Template class or a point like [110,220] or (110,220).
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:delay:
  When delay < 0.5, is in press station; When delay > 0.5, is in long press station.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> touch_if(template_pic, threshold=0.9, device=None, delay=0.4, timeout=10)

:description:
  touch template picture if template picture is  in current screen of Android Phone
:template_pic:
  The object of Template class or a point like [110,220] or (110,220).
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:delay:
  When delay < 0.5, is in press station; When delay > 0.5, is in long press station.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> long_touch(template_pic, threshold=0.9, device=None, delay=0.8, timeout=10)

:description:
  long touch template picture,throw a Error if template picture is not in current screen of Android Phone
:template_pic:
  The object of Template class or a point like [110,220] or (110,220).
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:delay:
  When delay < 0.5, is in press station; When delay > 0.5, is in long press station.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> touch_in(template_pic, target_pic, threshold=0.9, device=None, delay=0.4, timeout=10)

:description:
  touch small picture in big picture
:template_pic:
  The object of Template class, samll picture template object.
:target_pic:
  The object of Template class, big picture template object.
:threshold:
  The threshold of match template in opencv, the default is 0.9.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.
:delay:
  When delay < 0.5, is in press station; When delay > 0.5, is in long press station.
:timeout:
  Picture match will continue until time is overtime, the default is 10 second.

------------

>>> flick(start, direction, step=1, device=None)

:description:
  flick screen to different direction.
:start:
  The point to start flick screen.
:direction:
  The direction you want to flick, value is in [DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT].
:step:
  The step to flick.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.

------------

>>> swipe(start, end, device=None)

:description:
  swipe from one point to another point.
:start:
  The point to start swipe.
:end:
  The point to end swipe.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.

------------

>>> keyevent(keycode, device=None)

:description:
  do hardkey actioin using keycode.
:keyevent:
  The keycode of hardkey you want to operate to your Android Phone, value is in [HOME, BACK, VOLUME_UP, VOLUME_DOWN, POWER].
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.

------------

>>> text(input, device=None)

:description:
  input string via keyboard
:input:
  The input string.
:device:
  If your connect PC with more than one Android Phone, your will use this to identify which phone you want to operate by its serial number, beacuse every Android Phone has its own searial number.

------------

>>> image_to_string(template_pic)

:description:
  recognize text in pictures
:template_pic:
  The object of Template class or a list [top_left_x, top_left_y, bottom_right_x, bottom_right_y] like [120,200,200,400].

------------

>>> sleep(delay)

:description:
  sleep for some second
:delay:
  Sleep time.

------------

>>> end()

:description:
  to end runing case in your case


