# ptext module: place this in your import directory.

# ptext.draw(text, pos=None, **options)

# Please see README.md for explanation of options.
# https://github.com/cosmologicon/pygame-text

from __future__ import division, print_function

from math import ceil, sin, cos, radians, exp
from collections import namedtuple
import pygame

# Global default values
DEFAULT_FONT_SIZE = 24
REFERENCE_FONT_SIZE = 100
DEFAULT_LINE_HEIGHT = 1.0
DEFAULT_PARAGRAPH_SPACE = 0.0
DEFAULT_FONT_NAME = None
FONT_NAME_TEMPLATE = "%s"
DEFAULT_COLOR = "white"
DEFAULT_BACKGROUND = None
DEFAULT_SHADE = 0
DEFAULT_OUTLINE_WIDTH = None
DEFAULT_OUTLINE_COLOR = "black"
OUTLINE_UNIT = 1 / 24
DEFAULT_SHADOW_OFFSET = None
DEFAULT_SHADOW_COLOR = "black"
SHADOW_UNIT = 1 / 18
DEFAULT_ALIGN = "left"  # left, center, or right
DEFAULT_ANCHOR = 0, 0  # 0, 0 = top left ;  1, 1 = bottom right
DEFAULT_STRIP = True
ALPHA_RESOLUTION = 16
ANGLE_RESOLUTION_DEGREES = 3
DEFAULT_UNDERLINE_TAG = None
DEFAULT_BOLD_TAG = None
DEFAULT_ITALIC_TAG = None
DEFAULT_COLOR_TAG = {}

AUTO_CLEAN = True
MEMORY_LIMIT_MB = 64
MEMORY_REDUCTION_FACTOR = 0.5

pygame.font.init()

# Options objects encapsulate the keyword arguments to functions that take a lot of optional keyword
# arguments.

# Options object base class. Subclass for Options objects specific to different functions.
# Specify valid fields in the _fields list. All keyword fields are optional. Unspecified fields
# default to None, unless otherwise specified in the _defaults list.
class _Options(object):
	_fields = ()
	_defaults = {}
	def __init__(self, **kwargs):
		fields = self._allfields()
		badfields = set(kwargs) - fields
		if badfields:
			raise ValueError("Unrecognized args: " + ", ".join(badfields))
		for field in fields:
			value = kwargs[field] if field in kwargs else self._defaults.get(field)
			setattr(self, field, value)
	@classmethod
	def _allfields(cls):
		return set(cls._fields) | set(cls._defaults)
	def asdict(self):
		return { field: getattr(self, field) for field in self._allfields() }
	def copy(self):
		return self.__class__(**self.asdict())
	def keys(self):
		return self._allfields()
	def __getitem__(self, field):
		return getattr(self, field)
	def update(self, **newkwargs):
		kwargs = self.asdict()
		kwargs.update(**newkwargs)
		return self.__class__(**kwargs)
	# For cached function calls, this is a hashable representation of the options object. Assumes
	# that all field values are either hashable, or dicts whose keys are comparable and values are
	# hashable.
	def key(self):
		values = []
		for field in sorted(self._allfields()):
			value = getattr(self, field)
			if isinstance(value, dict):
				value = tuple(sorted(value.items()))
			values.append(value)
		return tuple(values)
	def getsuboptions(self, optclass):
		return { field: getattr(self, field) for field in optclass._allfields() if hasattr(self, field) }

	# The following methods are just put here for code deduplication. A couple different functions
	# use a lot of the same code.
	def resolvetags(self):
		if self.underlinetag is _default_sentinel:
			self.underlinetag = DEFAULT_UNDERLINE_TAG
		if self.boldtag is _default_sentinel:
			self.boldtag = DEFAULT_BOLD_TAG
		if self.italictag is _default_sentinel:
			self.italictag = DEFAULT_ITALIC_TAG
		if self.colortag is _default_sentinel:
			self.colortag = DEFAULT_COLOR_TAG

# Used as the default value for any argument for which (1) None is a valid value, and (2) there's a
# global default value.
_default_sentinel = ()

# Options argument for the draw function. Specifies both text styling and positioning.
class _DrawOptions(_Options):
	_fields = ("pos",
		"fontname", "fontsize", "sysfontname", "antialias", "bold", "italic", "underline",
		"color", "background",
		"top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright",
		"midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery",
		"width", "widthem", "lineheight", "pspace", "strip", "align",
		"owidth", "ocolor", "shadow", "scolor", "gcolor", "shade",
		"alpha", "anchor", "angle",
		"underlinetag", "boldtag", "italictag", "colortag",
		"surf", "cache")
	_defaults = {
		"antialias": True, "alpha": 1.0, "angle": 0,
		"owidth": _default_sentinel,
		"shadow": _default_sentinel,
		"underlinetag": _default_sentinel,
		"boldtag": _default_sentinel,
		"italictag": _default_sentinel,
		"colortag": _default_sentinel,
		"surf": _default_sentinel, "cache": True }

	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		self.expandposition()
		self.expandanchor()
		self.resolvesurf()

	# Expand each 2-element position specifier and overwrite the corresponding 1-element
	# position specifiers.
	def expandposition(self):
		if self.topleft: self.left, self.top = self.topleft
		if self.bottomleft: self.left, self.bottom = self.bottomleft
		if self.topright: self.right, self.top = self.topright
		if self.bottomright: self.right, self.bottom = self.bottomright
		if self.midtop: self.centerx, self.top = self.midtop
		if self.midleft: self.left, self.centery = self.midleft
		if self.midbottom: self.centerx, self.bottom = self.midbottom
		if self.midright: self.right, self.centery = self.midright
		if self.center: self.centerx, self.centery = self.center

	# Update the pos and anchor fields, if unspecified, to be specified by the positional
	# keyword arguments.
	def expandanchor(self):
		x, y = self.pos or (None, None)
		hanchor, vanchor = self.anchor or (None, None)
		if self.left is not None: x, hanchor = self.left, 0
		if self.centerx is not None: x, hanchor = self.centerx, 0.5
		if self.right is not None: x, hanchor = self.right, 1
		if self.top is not None: y, vanchor = self.top, 0
		if self.centery is not None: y, vanchor = self.centery, 0.5
		if self.bottom is not None: y, vanchor = self.bottom, 1
		if x is None:
			raise ValueError("Unable to determine horizontal position")
		if y is None:
			raise ValueError("Unable to determine vertical position")
		self.pos = x, y

		if self.align is None: self.align = hanchor
		if hanchor is None: hanchor = DEFAULT_ANCHOR[0]
		if vanchor is None: vanchor = DEFAULT_ANCHOR[1]
		self.anchor = hanchor, vanchor

	# Unspecified surf values default to the display surface.
	def resolvesurf(self):
		if self.surf is _default_sentinel:
			self.surf = pygame.display.get_surface()

	def togetsurfoptions(self):
		return self.getsuboptions(_GetsurfOptions)


# Options for the layout function. By design, this has the same options as draw, although some of
# them are silently ignored.
class _LayoutOptions(_DrawOptions):
	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		self.expandposition()
		self.expandanchor()		
		if self.lineheight is None: self.lineheight = DEFAULT_LINE_HEIGHT
		if self.pspace is None: self.pspace = DEFAULT_PARAGRAPH_SPACE
		self.resolvetags()

	def towrapoptions(self):
		return self.getsuboptions(_WrapOptions)

	def togetfontoptions(self):
		return self.getsuboptions(_GetfontOptions)


class _DrawboxOptions(_Options):
	_fields = (
		"fontname", "sysfontname", "antialias", "bold", "italic", "underline",
		"color", "background",
		"lineheight", "pspace", "strip", "align",
		"owidth", "ocolor", "shadow", "scolor", "gcolor", "shade",
		"underlinetag", "boldtag", "italictag", "colortag",
		"alpha", "anchor", "angle", "surf", "cache")
	_defaults = {
		"antialias": True, "alpha": 1.0, "angle": 0, "anchor": (0.5, 0.5),
		"owidth": _default_sentinel,
		"shadow": _default_sentinel,
		"underlinetag": _default_sentinel,
		"boldtag": _default_sentinel,
		"italictag": _default_sentinel,
		"colortag": _default_sentinel,
		"surf": _default_sentinel, "cache": True }
	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		if self.fontname is None: self.fontname = DEFAULT_FONT_NAME
		if self.lineheight is None: self.lineheight = DEFAULT_LINE_HEIGHT
		if self.pspace is None: self.pspace = DEFAULT_PARAGRAPH_SPACE

	def todrawoptions(self):
		return self.getsuboptions(_DrawOptions)

	def tofitsizeoptions(self):
		return self.getsuboptions(_FitsizeOptions)


class _GetsurfOptions(_Options):
	_fields = ("fontname", "fontsize", "sysfontname", "bold", "italic", "underline", "width",
		"widthem", "strip", "color", "background", "antialias", "ocolor", "owidth", "scolor",
		"shadow", "gcolor", "shade", "alpha", "align", "lineheight", "pspace", "angle",
		"underlinetag", "boldtag", "italictag", "colortag", "cache")
	_defaults = {
		"antialias": True, "alpha": 1.0, "angle": 0,
		"owidth": _default_sentinel,
		"shadow": _default_sentinel,
		"underlinetag": _default_sentinel,
		"boldtag": _default_sentinel,
		"italictag": _default_sentinel,
		"colortag": _default_sentinel,
		"cache": True }

	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		if self.fontname is None: self.fontname = DEFAULT_FONT_NAME
		if self.fontsize is None: self.fontsize = DEFAULT_FONT_SIZE
		self.fontsize = int(round(self.fontsize))
		if self.align is None: self.align = DEFAULT_ALIGN
		if self.align in ["left", "center", "right"]:
			self.align = [0, 0.5, 1][["left", "center", "right"].index(self.align)]
		if self.lineheight is None: self.lineheight = DEFAULT_LINE_HEIGHT
		if self.pspace is None: self.pspace = DEFAULT_PARAGRAPH_SPACE
		self.color = _resolvecolor(self.color, DEFAULT_COLOR)
		self.background = _resolvecolor(self.background, DEFAULT_BACKGROUND)
		self.gcolor = _resolvecolor(self.gcolor, None)
		if self.shade is None: self.shade = DEFAULT_SHADE
		if self.shade:
			self.gcolor = _applyshade(self.gcolor or self.color, self.shade)
			self.shade = 0
		self.resolveoutlineshadow()
		self.alpha = _resolvealpha(self.alpha)
		self.angle = _resolveangle(self.angle)
		self.strip = DEFAULT_STRIP if self.strip is None else self.strip
		self.resolvetags()

	def resolveoutlineshadow(self):
		if self.owidth is _default_sentinel:
			self.owidth = DEFAULT_OUTLINE_WIDTH
		if self.shadow is _default_sentinel:
			self.shadow = DEFAULT_SHADOW_OFFSET
		self.ocolor = None if self.owidth is None else _resolvecolor(self.ocolor, DEFAULT_OUTLINE_COLOR)
		self.scolor = None if self.shadow is None else _resolvecolor(self.scolor, DEFAULT_SHADOW_COLOR)
		self._opx = None if self.owidth is None else ceil(self.owidth * self.fontsize * OUTLINE_UNIT)
		self._spx = None if self.shadow is None else tuple(ceil(s * self.fontsize * SHADOW_UNIT) for s in self.shadow)

	def checkinline(self):
		if self.angle is None or self._opx is not None or self._spx is not None or self.align != 0 or self.gcolor or self.shade:
			raise ValueError("Inline style not compatible with rotation, outline, drop shadow, gradient, or non-left-aligned text.")

	def towrapoptions(self):
		return self.getsuboptions(_WrapOptions)

	def togetfontoptions(self):
		return self.getsuboptions(_GetfontOptions)


class _WrapOptions(_Options):
	_fields = ("fontname", "fontsize", "sysfontname",
		"bold", "italic", "underline", "width", "widthem", "strip",
		"color",
		"underlinetag", "boldtag", "italictag", "colortag")
	_defaults = {
		"underlinetag": _default_sentinel,
		"boldtag": _default_sentinel,
		"italictag": _default_sentinel,
		"colortag": _default_sentinel,
	}

	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		self.resolvetags()
		if self.widthem is not None and self.width is not None:
			raise ValueError("Can't set both width and widthem")

		if self.widthem is not None:
			self.fontsize = REFERENCE_FONT_SIZE
			self.width = self.widthem * self.fontsize

		if self.strip is None:
			self.strip = DEFAULT_STRIP

	def togetfontoptions(self):
		return self.getsuboptions(_GetfontOptions)

	
class _GetfontOptions(_Options):
	_fields = ("fontname", "fontsize", "sysfontname", "bold", "italic", "underline")
	def __init__(self, **kwargs):
		_Options.__init__(self, **kwargs)
		if self.fontname is not None and self.sysfontname is not None:
			raise ValueError("Can't set both fontname and sysfontname")
		if self.fontname is None and self.sysfontname is None:
			fontname = DEFAULT_FONT_NAME
		if self.fontsize is None:
			self.fontsize = DEFAULT_FONT_SIZE
	def getfontpath(self):
		return self.fontname if self.fontname is None else FONT_NAME_TEMPLATE % self.fontname

class _FitsizeOptions(_Options):
	_fields = ("fontname", "sysfontname", "bold", "italic", "underline",
		"lineheight", "pspace", "strip",
		"underlinetag", "boldtag", "italictag", "colortag")
	_defaults = {
		"underlinetag": _default_sentinel,
		"boldtag": _default_sentinel,
		"italictag": _default_sentinel,
		"colortag": _default_sentinel,
	}

	def togetfontoptions(self):
		return self.getsuboptions(_GetfontOptions)

	def towrapoptions(self):
		return self.getsuboptions(_WrapOptions)

_font_cache = {}
def getfont(**kwargs):
	options = _GetfontOptions(**kwargs)
	key = options.key()
	if key in _font_cache: return _font_cache[key]
	if options.sysfontname is not None:
		font = pygame.font.SysFont(options.sysfontname, options.fontsize, options.bold or False, options.italic or False)
	else:
		try:
			font = pygame.font.Font(options.getfontpath(), options.fontsize)
		except IOError:
			raise IOError("unable to read font filename: %s" % options.getfontpath())
	if options.bold is not None:
		font.set_bold(options.bold)
	if options.italic is not None:
		font.set_italic(options.italic)
	if options.underline is not None:
		font.set_underline(options.underline)
	_font_cache[key] = font
	return font


# Return the largest integer in the range [xmin, xmax] such that f(x) is True.
def _binarysearch(f, xmin = 1, xmax = 256):
	if not f(xmin): return xmin
	if f(xmax): return xmax
	# xmin is the largest known value for which f(x) is True
	# xmax is the smallest known value for which f(x) is False
	while xmax - xmin > 1:
		x = (xmax + xmin) // 2
		if f(x):
			xmin = x
		else:
			xmax = x
	return xmin

_fit_cache = {}
def _fitsize(text, size, **kwargs):
	options = _FitsizeOptions(**kwargs)
	key = text, size, options.key()
	if key in _fit_cache: return _fit_cache[key]
	width, height = size
	def fits(fontsize):
		opts = options.copy()
		wmax, hmax = 0, 0
		for span in _wrap(text, fontsize=fontsize, width=width, **opts.towrapoptions()):
			y = span.font.get_linesize() * (opts.pspace * span.jpara + opts.lineheight * span.jline)
			w, h = span.font.size(span.text)
			wmax = max(wmax, span.right)
			hmax = max(hmax, y + h)
		return wmax <= width and hmax <= height
	fontsize = _binarysearch(fits)
	_fit_cache[key] = fontsize
	return fontsize

# Returns the color as a color RGB or RGBA tuple (i.e. 3 or 4 integers in the range 0-255)
# If color is None, fall back to the default. If default is also None, return None.
# Both color and default can be a list, tuple, a color name, an HTML color format string, a hex
# number string, or an integer pixel value. See pygame.Color constructor for specification.
def _resolvecolor(color, default):
	if color is None: color = default
	if color is None: return None
	try:
		return tuple(pygame.Color(color))
	except ValueError:
		return tuple(color)

def _applyshade(color, shade):
	f = exp(-0.4 * shade)
	r, g, b = [
		min(max(int(round((c + 50) * f - 50)), 0), 255)
		for c in color[:3]
	]
	return (r, g, b) + tuple(color[3:])

def _resolvealpha(alpha):
	if alpha >= 1:
		return 1
	return max(int(round(alpha * ALPHA_RESOLUTION)) / ALPHA_RESOLUTION, 0)

def _resolveangle(angle):
	if not angle:
		return 0
	angle %= 360
	return int(round(angle / ANGLE_RESOLUTION_DEGREES)) * ANGLE_RESOLUTION_DEGREES

# Return the set of points in the circle radius r, using Bresenham's circle algorithm
_circle_cache = {}
def _circlepoints(r):
	r = int(round(r))
	if r in _circle_cache:
		return _circle_cache[r]
	x, y, e = r, 0, 1 - r
	_circle_cache[r] = points = []
	while x >= y:
		points.append((x, y))
		y += 1
		if e < 0:
			e += 2 * y - 1
		else:
			x -= 1
			e += 2 * (y - x) - 1
	points += [(y, x) for x, y in points if x > y]
	points += [(-x, y) for x, y in points if x]
	points += [(x, -y) for x, y in points if y]
	points.sort()
	return points

# Rotate the given surface by the given angle, in degrees.
# If angle is an exact multiple of 90, use pygame.transform.rotate, otherwise fall back to
# pygame.transform.rotozoom.
def _rotatesurf(surf, angle):
	if angle in (90, 180, 270):
		return pygame.transform.rotate(surf, angle)
	else:
		return pygame.transform.rotozoom(surf, angle, 1.0)

# Apply the given alpha value to a copy of the Surface.
def _fadesurf(surf, alpha):
	surf = surf.copy()
	asurf = surf.copy()
	asurf.fill((255, 255, 255, int(round(255 * alpha))))
	surf.blit(asurf, (0, 0), None, pygame.BLEND_RGBA_MULT)
	return surf

def _istransparent(color):
	return len(color) > 3 and color[3] == 0

# Produce a 1xh Surface with the given color gradient.
_grad_cache = {}
def _gradsurf(h, y0, y1, color0, color1):
	key = h, y0, y1, color0, color1
	if key in _grad_cache:
		return _grad_cache[key]
	surf = pygame.Surface((1, h)).convert_alpha()
	r0, g0, b0 = color0[:3]
	r1, g1, b1 = color1[:3]
	for y in range(h):
		f = min(max((y - y0) / (y1 - y0), 0), 1)
		g = 1 - f
		surf.set_at((0, y), (
			int(round(g * r0 + f * r1)),
			int(round(g * g0 + f * g1)),
			int(round(g * b0 + f * b1)),
			0
		))
	_grad_cache[key] = surf
	return surf


# Tracks everything that can be updated by tags.
class TagSpec(namedtuple("TagSpec", ["underline", "bold", "italic", "color"])):
	@staticmethod
	def fromoptions(options):
		return TagSpec(
			underline = options.underline,
			bold = options.bold,
			italic = options.italic,
			color = options.color
		)
	def updateoptions(self, options):
		options.underline = self.underline
		options.bold = self.bold
		options.italic = self.italic
		options.color = self.color
	def toggleunderline(self):
		return self._replace(underline = not self.underline)
	def togglebold(self):
		return self._replace(bold = not self.bold)
	def toggleitalic(self):
		return self._replace(italic = not self.italic)
	def setcolor(self, color):
		return self._replace(color = color)

# Splits a string into substrings with corresponding tag specs.
# Empty strings are skipped. Consecutive identical tag specs are not merged.
# e.g. if tagspec0.underline = False and underlinetag = "_" then:
# _splitbytags("_abc__def_ ghi_") yields three items:
#   ("abc", TagSpec(underline=True))
#   ("def", TagSpec(underline=True))
#   (" ghi", TagSpec(underline=False))
def _splitbytags(text, tagspec0, color0, underlinetag, boldtag, italictag, colortag):
	colortag = { k: _resolvecolor(v, color0) for k, v in colortag.items() }
	tags = sorted((set([underlinetag, boldtag, italictag]) | set(colortag.keys())) - set([None]))
	if not tags:
		yield text, tagspec0
		return
	tagspec = tagspec0
	while text:
		tagsin = [tag for tag in tags if tag in text]
		if not tagsin:
			break
		a, tag = min((text.index(tag), tag) for tag in tagsin)
		if a > 0:
			yield text[:a], tagspec
		text = text[a + len(tag):]
		if tag == underlinetag:
			tagspec = tagspec.toggleunderline()
		if tag == boldtag:
			tagspec = tagspec.togglebold()
		if tag == italictag:
			tagspec = tagspec.toggleitalic()
		if tag in colortag:
			tagspec = tagspec.setcolor(colortag[tag])
	if text:
		yield text, tagspec

# The _Span class tracks many attributes of a single span of text, i.e. a string of text within a
# single line that has a single font and TagSpec. That is, a single span corresponds to a single
# call to font.render.
# This is not a clean abstraction, and some of the state of this object only makes sense in the
# context of the overall draw call. At various stages of the call, some of the fields will not yet
# be populated.
class _Span:
	# Phase 1: set by _wrapline
	def __init__(self, text, tagspec, x, font):
		self.tagspec = tagspec
		self.x = x  # Offset from the beginning of the line
		self.font = font
		self.settext(text)
	# Phase 2: set by _wrap
	def setlayout(self, jpara, jline, linewidth):
		self.jpara = jpara
		self.jline = jline
		self.linewidth = linewidth
	# Phase 3: set by getsurf
	# These are not required to determine layout or position, only for rendering.
	def setdetails(self, antialias, gcolor, background):
		self.antialias = antialias
		self.gcolor = gcolor
		self.background = background

	def settext(self, text):
		self.text = text
		self.width = self.getwidth(self.text)
		self.right = self.x + self.width

	def getwidth(self, text):
		return self.font.size(text)[0]

	def render(self):
		if self.gcolor is None:
			# Workaround: pygame.Font.render does not allow passing None as an argument value for
			# background. We have to call the 3-argument form to specify no background.
			args = self.text, self.antialias, self.tagspec.color
			if self.background is not None and not _istransparent(self.background):
				args += (self.background,)
			self.surf = self.font.render(*args).convert_alpha()
		else:
			self.surf = self.font.render(self.text, self.antialias, (0, 0, 0)).convert_alpha()
			w, h = self.surf.get_size()
			asc = self.font.get_ascent()
			gsurf0 = _gradsurf(h, 0.5 * asc, asc, self.tagspec.color, self.gcolor)
			gsurf = pygame.transform.scale(gsurf0, (w, h))
			self.surf.blit(gsurf, (0, 0), None, pygame.BLEND_RGBA_ADD)



# A breakpoint is a space character that immediately follows a non-space character, or one past the
# end of the line, if the line ends in a non-space character. (If canbreakatstart is True, then
# there is also a breakpoint at the beginning of the line.)
# A valid breakpoint is one such that font.width(text[:a]) is not greater than width. Exception: the
# first breakpoint in a line is always valid.
# This function returns the index of the last valid breakpoint.
def _getbreakpoint(text, width, font, canbreakatstart = False):
	def isvalid(breakpoint):
		return font.size(text[:breakpoint])[0] <= width
	# At any point, a is the index of a known valid break point. b is a candidate breakpoint, and c
	# is the rightmost breakpoint.
	c = len(text.rstrip(" "))
	if width is None or isvalid(c):
		return c
	if canbreakatstart:
		a = 0
	else:
		# Preserve leading spaces.
		lspaces = len(text) - len(text.lstrip(" "))
		a = text.index(" ", lspaces) if " " in text[lspaces:] else len(text)
	# Only one breakpoint, automatically valid as an exception.
	if a == c:
		return a
	# TODO: binary search
	while True:
		subtext = text[a:c]
		# The next breakpoint must occur after any leading spaces.
		sublspaces = len(subtext) - len(subtext.lstrip(" "))
		if " " not in subtext[sublspaces:]:
			return a
		b = a + subtext.index(" ", sublspaces + 1)
		if isvalid(b):
			a = b
		else:
			return a

# Split a single line of text.
# textandtags is the output of _splitbytags, i.e. a sequence of (string, tag spec) tuples.
def _wrapline(textandtags, width, getfontbytagspec):
	x = 0
	canbreakatstart = False
	lines = []
	line = []
	for text, tagspec in textandtags:
		font = getfontbytagspec(tagspec)
		while text:
			# TODO: options.split
			rwidth = None if width is None else width - x
			a = _getbreakpoint(text, rwidth, font, canbreakatstart)
			while a < len(text) and text[a] == " ":
				a += 1
			if a == 0:
				lines.append((line, x))
				line = []
				x = 0
				canbreakatstart = False
			else:
				span = _Span(text[:a], tagspec, x, font)
				line.append(span)
				x += span.width
				text = text[a:]
				canbreakatstart = True
	lines.append((line, x))
	return lines

def _wrap(text, **kwargs):
	options = _WrapOptions(**kwargs)
	# Returns a function mapping strings to int widths in the specified font
	opts = options.copy()
	def getfontbytagspec(tagspec):
		tagspec.updateoptions(opts)
		return getfont(**opts.togetfontoptions())
	# Apparently Font.render accepts None for the text argument, in which case it's treated as the
	# empty string. We match that behavior here.
	if text is None: text = ""
	spans = []
	tagspec0 = TagSpec.fromoptions(options)
	jline = 0
	for jpara, para in enumerate(text.replace("\t", "    ").split("\n")):
		if options.strip:
			para = para.rstrip(" ")
		tagargs = options.underlinetag, options.boldtag, options.italictag, options.colortag
		textandtags = list(_splitbytags(para, tagspec0, options.color, *tagargs))
		_, tagspec0 = textandtags[-1]
		for line, linewidth in _wrapline(textandtags, options.width, getfontbytagspec):
			if not line:
				jline += 1
				continue
			# Strip trailing spaces from the end of each line.
			span = line[-1]
			if options.strip:
				span.settext(span.text.rstrip(" "))
			elif options.width is not None:
				while span.text[-1] == " " and span.right > options.width:
					span.settext(span.text[:-1])
			linewidth = span.right
			for span in line:
				span.setlayout(jpara, jline, linewidth)
				spans.append(span)
			jline += 1
	return spans

			

_surf_cache = {}
_surf_tick_usage = {}
_surf_size_total = 0
_unrotated_size = {}
_tick = 0
def getsurf(text, **kwargs):
	global _tick, _surf_size_total
	options = _GetsurfOptions(**kwargs)
	key = text, options.key()
	if key in _surf_cache:
		_surf_tick_usage[key] = _tick
		_tick += 1
		return _surf_cache[key]

	if options.angle:
		surf0 = getsurf(text, **options.update(angle = 0))
		surf = _rotatesurf(surf0, options.angle)
		# draw() requires the unrotated size for proper positioning, but the unrotated surface will
		# not necessarily be cached, so we add it to a global store here. In principle you could
		# compute it from surf.get_size() and options.angle, were it not for rounding issues.
		_unrotated_size[(surf.get_size(), options.angle, text)] = surf0.get_size()
	elif options.alpha < 1.0:
		surf = _fadesurf(getsurf(text, **options.update(alpha = 1.0)), options.alpha)
	elif options._spx is not None:
		color = (0, 0, 0) if _istransparent(options.color) else options.color
		surf0 = getsurf(text, **options.update(background = (0, 0, 0, 0), color = color, shadow = None, scolor = None))
		sopts = {
			"color": options.scolor,
			"shadow": None,
			"scolor": None,
			"background": (0, 0, 0, 0),
			"gcolor": None,
			"colortag": { k: None for k in options.colortag },
		}
		ssurf = getsurf(text, **options.update(**sopts))
		w0, h0 = surf0.get_size()
		sx, sy = options._spx
		surf = pygame.Surface((w0 + abs(sx), h0 + abs(sy))).convert_alpha()
		surf.fill(options.background or (0, 0, 0, 0))
		dx, dy = max(sx, 0), max(sy, 0)
		surf.blit(ssurf, (dx, dy))
		x0, y0 = abs(sx) - dx, abs(sy) - dy
		if _istransparent(options.color):
			surf.blit(surf0, (x0, y0), None, pygame.BLEND_RGBA_SUB)
		else:
			surf.blit(surf0, (x0, y0))
	elif options._opx is not None:
		color = (0, 0, 0) if _istransparent(options.color) else options.color
		surf0 = getsurf(text, **options.update(color = color, ocolor = None, owidth = None))
		oopts = {
			"color": options.ocolor,
			"ocolor": None,
			"owidth": None,
			"background": (0, 0, 0, 0),
			"gcolor": None,
			"colortag": { k: None for k in options.colortag },
		}
		osurf = getsurf(text, **options.update(**oopts))
		w0, h0 = surf0.get_size()
		opx = options._opx
		surf = pygame.Surface((w0 + 2 * opx, h0 + 2 * opx)).convert_alpha()
		surf.fill(options.background or (0, 0, 0, 0))
		for dx, dy in _circlepoints(opx):
			surf.blit(osurf, (dx + opx, dy + opx))
		if _istransparent(options.color):
			surf.blit(surf0, (opx, opx), None, pygame.BLEND_RGBA_SUB)
		else:
			surf.blit(surf0, (opx, opx))
	else:
		# Each span is rendered separately into a Surface, and then the different spans' Surfaces
		# are blitted onto the final Surface.
		spans = _wrap(text, **options.towrapoptions())
		for span in spans:
			span.setdetails(options.antialias, options.gcolor, options.background)
			span.render()
		# Now to blit the span Surfaces together onto a single Surface. As an optimization, when
		# there is only one span Surface, just use that. (We can't use this optimization if there's
		# a gradient color, because the background color still needs to be applied.)
		if not spans:
			surf = pygame.Surface((0, 0)).convert_alpha()
		elif len(spans) == 1 and options.gcolor is None:
			surf = spans[0].surf
		else:
			font = spans[0].font
			w = max(span.linewidth for span in spans)
			linesize = font.get_linesize() * options.lineheight
			parasize = font.get_linesize() * options.pspace
			for span in spans:
				span.y = int(round(span.jline * linesize + span.jpara * parasize))
			h = max(span.y for span in spans) + font.get_height()
			surf = pygame.Surface((w, h)).convert_alpha()
			surf.fill(options.background or (0, 0, 0, 0))
			for span in spans:
				x = int(round(span.x + options.align * (w - span.linewidth)))
				surf.blit(span.surf, (x, span.y))
	if options.cache:
		w, h = surf.get_size()
		_surf_size_total += 4 * w * h
		_surf_cache[key] = surf
		_surf_tick_usage[key] = _tick
		_tick += 1
	return surf


# The actual position on the screen where the surf is to be blitted, rather than the specified
# anchor position.
def _blitpos(angle, pos, anchor, size, text):
	angle = _resolveangle(angle)
	x, y = pos
	sw, sh = size
	hanchor, vanchor = anchor
	if angle:
		w0, h0 = _unrotated_size[(size, angle, text)]
		S, C = sin(radians(angle)), cos(radians(angle))
		dx, dy = (0.5 - hanchor) * w0, (0.5 - vanchor) * h0
		x += dx * C + dy * S - 0.5 * sw
		y += -dx * S + dy * C - 0.5 * sh
	else:
		x -= hanchor * sw
		y -= vanchor * sh
	x = int(round(x))
	y = int(round(y))
	return x, y


def layout(text, **kwargs):
	options = _LayoutOptions(**kwargs)
	if options.angle != 0:
		raise ValueError("Nonzero angle not yet supported for ptext.layout")
	font = getfont(**options.togetfontoptions())
	fl = font.get_linesize()
	linesize = fl * options.lineheight
	parasize = fl * options.pspace

	spans = _wrap(text, **options.towrapoptions())

	rects = []
	fonts = []
	sw = max(span.linewidth for span in spans)
#	for tpiece, tagspec, x, jpara, jline, linewidth in spans:
	for span in spans:
		y = int(round(span.jpara * parasize + span.jline * linesize))
		rect = pygame.Rect(span.x, y, *font.size(span.text))
		rect.x += int(round(options.align * (sw - span.linewidth)))
		rects.append(rect)
	sh = max(rect.bottom for rect in rects)

	x0, y0 = _blitpos(options.angle, options.pos, options.anchor, (sw, sh), None)

	# Adjust the rects as necessary to account for outline and shadow.
	# TODO: the following is duplicated from _GetsurfOptions.__init__
	dx, dy = 0, 0
	if options.owidth is not None:
		opx = ceil(options.owidth * options.fontsize * OUTLINE_UNIT)
		dx, dy = max(dx, abs(opx)), max(dy, abs(opx))
	if options.shadow is not None:
		spx, spy = (ceil(s * options.fontsize * SHADOW_UNIT) for s in options.shadow)
		dx, dy = max(dx, -spx), max(dy, -spy)
	rects = [rect.move(x0 + dx, y0 + dy) for rect in rects]

	return [(span.text, rect, span.font) for span, rect in zip(spans, rects)]


def draw(text, pos=None, **kwargs):
	options = _DrawOptions(pos = pos, **kwargs)
	tsurf = getsurf(text, **options.togetsurfoptions())
	pos = _blitpos(options.angle, options.pos, options.anchor, tsurf.get_size(), text)
	if options.surf is not None:
		options.surf.blit(tsurf, pos)
	if AUTO_CLEAN:
		clean()
	return tsurf, pos

def drawbox(text, rect, **kwargs):
	options = _DrawboxOptions(**kwargs)
	rect = pygame.Rect(rect)
	hanchor, vanchor = options.anchor
	x = rect.x + hanchor * rect.width
	y = rect.y + vanchor * rect.height
	fontsize = _fitsize(text, rect.size, **options.tofitsizeoptions())
	return draw(text, pos=(x,y), width=rect.width, fontsize=fontsize, **options.todrawoptions())

def clean():
	global _surf_size_total
	memory_limit = MEMORY_LIMIT_MB * (1 << 20)
	if _surf_size_total < memory_limit:
		return
	memory_limit *= MEMORY_REDUCTION_FACTOR
	keys = sorted(_surf_cache, key=_surf_tick_usage.get)
	for key in keys:
		w, h = _surf_cache[key].get_size()
		del _surf_cache[key]
		del _surf_tick_usage[key]
		_surf_size_total -= 4 * w * h
		if _surf_size_total < memory_limit:
			break

