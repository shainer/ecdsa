"""Implementation of elliptic curves and basic operations."""

from modular import invmod
import math

class ECPoint(object):
	"""Represents a point on an elliptic curve.

	(0, 0) is the point at infinity.
	"""

	def __init__(self, x, y):
		if x == 0 and y == 0:
			self.infinity = True
			self.point = (0, 0)
		else:
			self.infinity = False
			self.point = (x, y)

	def point(self, x, y):
		return self.point

	def x(self):
		return self.point[0]

	def y(self):
		return self.point[1]

	def isInfinity(self):
		return self.infinity

	def __str__(self):
		if self.isInfinity():
			return '(0, 0)'

		return '(%.3f, %.3f)' % (self.x(), self.y())

	def __eq__(self, o):
		if self.isInfinity():
			return o.isInfinity()

		return self.x() == o.x() and self.y() == o.y()


class EllipticCurve(object):
	"""Represents an elliptic curve in modulo p.
	"""
	def __init__(self, a, b, p):
		# Basic conditions for the curve to be valid.
		assert a < p and b > 0 and b < p and p > 2
		assert (4 * (a ** 3) + 27 * (b ** 2))  % p != 0

		self.a = a
		self.b = b
		self.p = p
		self.zero = ECPoint(0, 0)

	def isValid(self, point):
		if point == self.zero:
			return True

		l = (point.y() ** 2) % self.p
		r = ((point.x() ** 3) + self.a * point.x() + self.b) % self.p
		return l == r

	def add(self, p1, p2):
		"""Point addition on the curve."""
		if p1 == self.zero:
			return p2

		if p2 == self.zero:
			return p1

		if p1.x() == p2.x() and (p1.y() != p2.y() or p1.y() == 0):
			return self.zero

		if p1.x() == p2.x():
			m = ((3 * (p1.x() ** 2)) + self.a) * invmod(2 * p1.y(), self.p) % self.p
		else:
			m = (p1.y() - p2.y()) * invmod(p1.x() - p2.x(), self.p) % self.p

		xR = (m ** 2 - p1.x() - p2.x()) % self.p
		yR = (m * (p1.x() - xR) - p1.y()) % self.p

		return ECPoint(xR, yR)

	def scalarMul(self, p1, n):
		"""Scalar multiplication, implemented with the double-add algorithm."""
		res = self.zero
		acc = p1
		exp = n

		while exp > 0:
			if exp % 2 != 0:
				res = self.add(res, acc)

			acc = self.add(acc, acc)
			exp //= 2

		return res
