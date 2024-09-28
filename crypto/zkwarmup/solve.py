import random
import time
import socket

# This ZKP works as follows:
#   - Prover (you) send some int s
#   - Verifier generates random b = 0 or b = 1
#   - Prover (you) send z satisfying the following:
#       - If b = 0, want z s.t. z^2 = s * y
#       - If b = 1, want z s.t. z^2 = s

# Abuse the bad seeding of random. Predict if verifier will send b = 0 or b = 1 and send s = i^2 * y^-1 or s = i^2
# accordingly. When you get a value of b from the verifier (which you should already know), send i back.

# Unrelated, but here's an interesting read (based on only the first page) I came across about ZKPs:
# https://people.eecs.berkeley.edu/~jfc/cs174/lecs/lec24/lec24.pdf
# It might help explain why the ZKP is designed this way.

rounds = 128
wait = 0.01


def flip_coin() -> int:
    return random.randrange(2)


n = 19261756194530262169516227535327268535825703622469356233861243450409596218324982327819027354327762272541787979307084854543427241827543331732057807638293377995167826046761991463655794445629511818504788588146049602678202660790161211079215140614149179394809442098536009911202757117559092796991732111808588753074002377241720729762405118846289128192452140379045358673985940236403266552967867241351260376075804662700969038717732248036975281084947926661161892037413944872628410488986135370175176475239647256670545733839891394321932103696968961386864456665963903759123610214930997530883831800104920546270573046968308379346633

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    random.seed(int(time.time()))

    s.connect(("challs.pwnoh.io", 13421))

    print("RECEIVED:", s.recv(4096))

    x = random.randrange(1, n)
    y = pow(x, 2, n)

    y_inv = pow(y, -1, n)

    # +5 instead of +2 for safety and to print final output
    for i in range(1, rounds + 5):
        print("ROUND", i)
        b = flip_coin()

        if b == 0:
            s.send(bytes(str(y_inv * i ** 2), "utf-8") + b"\n")
            time.sleep(wait)

            # b = 0\nProvide z:
            print("RECEIVED:", s.recv(4096))

            s.send(bytes(str(i), "utf-8") + b"\n")
            time.sleep(wait)

            # Provide s:
            print("RECEIVED:", s.recv(4096))
        else:
            s.send(bytes(str(i ** 2), "utf-8") + b"\n")
            time.sleep(wait)

            # b = 0\nProvide z:
            print("RECEIVED:", s.recv(4096))

            s.send(bytes(str(i), "utf-8") + b"\n")
            time.sleep(wait)

            # Provide s:
            print("RECEIVED:", s.recv(4096))

        # Eventually prints bctf{c4n_s0m30ne_g1v3_m3_a_r3a1_c01n_t0_fl1p}
