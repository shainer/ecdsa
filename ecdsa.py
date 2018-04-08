import hashlib
import random

import modular
import elliptic_curves as ec


class DSAError(Exception):
    pass


def _hash_message(mbytes):
    """Computes a SHA1 of a message, expressed a bytes,
    and converts the digest to an integer. This makes it
    suitable to be signed/verified by DSA.
    """
    m = hashlib.sha1()
    m.update(mbytes)
    digest = m.hexdigest()

    H = int('0x' + digest, 16)
    return H


class EllipticCurveDSA(object):
    """Implementation of ECDSA."""

    def __init__(self, curve, G, n):
        """Inits the algorithm.

        Params:
            curve: (EllipticCurve object) an elliptic curve.
            G: (ECPoint object) curve's generator.
            n: (int) order of the generator.
        """
        self._curve = curve
        self._G = G
        self._n = n

    def GeneratePair(self):
        """Generates a key pair (d, Q)."""
        d = random.randint(1, self._n - 1)
        Q = self._curve.scalarMul(self._G, d)
        return (d, Q)

    def Sign(self, key, message):
        """Signs a message (a byte string) given the key."""
        d, _ = key
        h = _hash_message(message)
        r = 0
        s = 0

        while True:
            k = random.randint(1, self._n - 1)
            p = self._curve.scalarMul(self._G, k)

            r = p.x() % self._n
            # Try again with another random k
            if r == 0:
                continue

            k1 = modular.invmod(k, self._n)

            s = (((h + r*d) % self._n) * k1) % self._n
            # Try again with another random k
            if s == 0:
                continue
            break

        return (r, s)

    def Verify(self, signature, key, message):
        """Verifies a signature for a message.

        Raises DSAError for an invalid signature or key.
        """
        _, Q = key

        if not self._curve.isValid(Q):
            raise DSAError('[!!] Point %s is not valid.' % str(Q))

        r, s = signature
        if r < 1 or r > self._n - 1 or s < 1 or s > self._n - 1:
            raise DSAError('[!!] Signature (%lld, %lld) is out of bounds.' % (r, s))

        h = _hash_message(message)
        w = modular.invmod(s, self._n)
        u1 = (h * w) % self._n
        u2 = (r * w) % self._n
        P = self._curve.add(self._curve.scalarMul(self._G, u1), self._curve.scalarMul(Q, u2))

        return r == (P.x() % self._n)
