#!/usr/bin/python3
"""Validations."""

import ecdsa
import elliptic_curves as ec

if __name__ == '__main__':
    P = 233970423115425145524320034830162017933
    G = ec.ECPoint(182, 85518893674295321206118380980485522083)
    N = 29246302889428143187362802287225875743

    curve = ec.EllipticCurve(-95051, 11279326, P)
    dsa = ecdsa.EllipticCurveDSA(curve, G, N)

    key = dsa.GeneratePair()
    sig = dsa.Sign(key, b'hello world')

    if dsa.Verify(sig, key, b'hello world'):
        print('[**] Validation passed')
    else:
        print('[!!] Validation failed.')
