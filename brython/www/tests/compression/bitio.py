class BitIO:

    def __init__(self, bytestream=b''):
        self.bytestream = bytearray(bytestream)
        self.bytenum = 0
        self.bitnum = 0

    @property
    def pos(self):
        return self.bytenum * 8 + self.bitnum

    def read(self, nb, order="lsf", trace=False):
        result = 0
        coef = 1 if order == "lsf" else 2 ** (nb - 1)
        for _ in range(nb):
            if self.bitnum == 8:
                if self.bytenum == len(self.bytestream) - 1:
                    return None
                self.bytenum += 1
                self.bitnum = 0
            mask = 2 ** self.bitnum
            if trace:
                print("bit", int(bool(mask & self.bytestream[self.bytenum])))
            result += coef * bool(mask & self.bytestream[self.bytenum])
            self.bitnum += 1
            if order == "lsf":
                coef *= 2
            else:
                coef //= 2
        return result

    def move(self, nb):
        if nb == 0:
            return
        elif nb > 0:
            bitpos = self.bitnum + nb
            while bitpos > 7:
                self.bytenum += 1
                if self.bytenum == len(self.bytestream):
                    raise Exception("can't move {} bits".format(nb))
                bitpos -= 8
            self.bitnum = bitpos
        else:
            bitpos = self.bitnum + nb
            while bitpos < 0:
                self.bytenum -= 1
                if self.bytenum == -1:
                    raise Exception("can't move {} bits".format(nb))
                bitpos += 8
            self.bitnum = bitpos

    def show(self):
        for x in self.bytestream:
            s = str(bin(x))[2:]
            s = "0" * (8 - len(s)) + s
            print(s, end=" ")
        print()

    def write(self, *bits):
        for bit in bits:
            if not self.bytestream:
                self.bytestream.append(0)
            byte = self.bytestream[self.bytenum]
            if self.bitnum == 8:
                if self.bytenum == len(self.bytestream) - 1:
                    byte = 0
                    self.bytestream += bytes([byte])
                self.bytenum += 1
                self.bitnum = 0
            mask = 2 ** self.bitnum
            if bit:
                byte |= mask
            else:
                byte &= ~mask
            self.bytestream[self.bytenum] = byte
            self.bitnum += 1

    def write_int(self, value, nb, order="lsf"):
        """Write integer on nb bits."""
        if value >= 2 ** nb:
            raise ValueError("can't write value on {} bits".format(nb))
        bits = []
        while value:
            bits.append(value & 1)
            value >>= 1
        # pad with 0's
        bits = bits + [0] * (nb - len(bits))
        if order != "lsf":
            bits.reverse()
        assert len(bits) == nb
        self.write(*bits)

if __name__ == "__main__":
    text = """Pleurez, doux alcyons, ?? vous, oiseaux sacr??s,
    Oiseaux chers ?? Th??tis, doux alcyons, pleurez.

    Elle a v??cu, Myrto, la jeune Tarentine.
    Un vaisseau la portait aux bords de Camarine.
    L?? l'hymen, les chansons, les fl??tes, lentement,
    Devaient la reconduire au seuil de son amant.
    Une clef vigilante a pour cette journ??e
    Dans le c??dre enferm?? sa robe d'hym??n??e
    Et l'or dont au festin ses bras seraient par??s
    Et pour ses blonds cheveux les parfums pr??par??s.
    Mais, seule sur la proue, invoquant les ??toiles,
    Le vent imp??tueux qui soufflait dans les voiles
    L'enveloppe. ??tonn??e, et loin des matelots,
    Elle crie, elle tombe, elle est au sein des flots.

    Elle est au sein des flots, la jeune Tarentine.
    Son beau corps a roul?? sous la vague marine.
    Th??tis, les yeux en pleurs, dans le creux d'un rocher
    Aux monstres d??vorants eut soin de la cacher.
    Par ses ordres bient??t les belles N??r??ides
    L'??l??vent au-dessus des demeures humides,
    Le portent au rivage, et dans ce monument
    L'ont, au cap du Z??phir, d??pos?? mollement.
    Puis de loin ?? grands cris appelant leurs compagnes,
    Et les Nymphes des bois, des sources, des montagnes,
    Toutes frappant leur sein et tra??nant un long deuil,
    R??p??t??rent : ?? h??las ! ?? autour de son cercueil.

    H??las ! chez ton amant tu n'es point ramen??e.
    Tu n'as point rev??tu ta robe d'hym??n??e.
    L'or autour de tes bras n'a point serr?? de n??uds.
    Les doux parfums n'ont point coul?? sur tes cheveux."""

    #text = "adsqfqgqs"
    text = text.encode("utf-8")
    io = BitIO(text)

    while True:
        bit = io.read(1)
        if bit is None:
            break
    io.move(-16)
    print(io.read(8), io.read(8))

    io.write_bits(0, 0, 0, 0, 0, 0, 0, 1)
    print(io.bytestream[-1])

    io.write_int(ord("x"), 8)
    print(chr(io.bytestream[-1]))
