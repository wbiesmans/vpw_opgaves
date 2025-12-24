import bisect
import dataclasses
from typing import List, Set


@dataclasses.dataclass
class Straat:
    kruispunt_a: int
    kruispunt_b: int
    lengte: int
    nodig: bool

    def __hash__(self):
        return self.kruispunt_a * 1000000 + self.kruispunt_b * 1000 + int(lengte)


@dataclasses.dataclass
class Kruispunt:
    index: int
    straten: Set[Straat] = dataclasses.field(default_factory=set)

    def __repr__(self):
        return str(self.index)


@dataclasses.dataclass
class Pad:
    kruispunten: List[Kruispunt] = dataclasses.field(default_factory=list)
    afstand: int = 0
    straten: list = dataclasses.field(default_factory=list)

    def __lt__(self, other):
        return self.afstand < other.afstand

    def __eq__(self, other):
        return self.afstand == other.afstand

    def __repr__(self):
        return str(self.kruispunten)


def pad_is_compleet(pad, nodige_straten):
    for straat in nodige_straten:
        if straat not in pad.straten:
            return False

    return True


def straat_drie_keer(straten_lijst):
    laatste_straat = straten_lijst[-1]
    count = 0
    for straat in straten_lijst:
        if straat == laatste_straat:
            count += 1

    if count == 3:
        return True
    elif count > 3:
        return ValueError("Should not happen")
    else:
        return False


def straat_twee_keer(pad, laatste_straat, laatste_kruispunt):
    index = 0
    for straat in pad.straten:
        if straat == laatste_straat:
            if pad.kruispunten[index] == laatste_kruispunt:
                return True
        index = index + 1
    return False


def vind_kortste_pad(straten, depot, aantal_kruispunten):
    # Nodige straten
    nodige_straten = []
    for straat in straten:
        if straat.nodig:
            nodige_straten.append(straat)

    # Maak kruispunten
    kruispunten = []
    for k in range(aantal_kruispunten):
        kruispunt = Kruispunt(index=k)
        kruispunten.append(kruispunt)

    for straat in straten:
        kruispunten[straat.kruispunt_a].straten.add(straat)
        kruispunten[straat.kruispunt_b].straten.add(straat)

    paden = [Pad(kruispunten=[kruispunten[depot]])]

    max_afstand = 99999999999
    beste_pad = None
    current_step = 0
    while paden:
        current_step += 1
        nieuwe_paden = []
        pad = paden[0]
        laatste_kruispunt = pad.kruispunten[-1]
        pad_lengte = pad.afstand
        # Only consider paths that are still potential solutions
        if pad_lengte > max_afstand and beste_pad:
            continue
        for straat in laatste_kruispunt.straten:
            nieuw_pad_lengte = pad_lengte + straat.lengte
            if nieuw_pad_lengte > max_afstand and beste_pad:
                continue

            kruispunten_copy = pad.kruispunten.copy()
            straten_copy = pad.straten.copy()
            straten_copy.append(straat)

            if straat_twee_keer(pad, straat, laatste_kruispunt):
                continue

            if laatste_kruispunt.index == straat.kruispunt_a:
                kruispunten_copy.append(kruispunten[straat.kruispunt_b])
                nieuw_pad = Pad(
                    kruispunten=kruispunten_copy,
                    afstand=nieuw_pad_lengte,
                    straten=straten_copy,
                )
            elif laatste_kruispunt.index == straat.kruispunt_b:
                kruispunten_copy.append(kruispunten[straat.kruispunt_a])
                nieuw_pad = Pad(
                    kruispunten=kruispunten_copy,
                    afstand=nieuw_pad_lengte,
                    straten=straten_copy,
                )
            else:
                raise ValueError("Case should not happen")

            nieuwe_paden.append(nieuw_pad)

        paden.pop(0)

        for nieuw_pad in nieuwe_paden:
            if nieuw_pad.kruispunten[-1].index == depot:
                if pad_is_compleet(nieuw_pad, nodige_straten):
                    if pad.afstand < max_afstand:
                        beste_pad = nieuw_pad
                        max_afstand = nieuw_pad.afstand
                        too_long = len(paden)
                        for i, pad in enumerate(paden):
                            if pad.afstand >= max_afstand:
                                too_long = i
                                break
                        print(f"Pruned {len(paden) - too_long}/{len(paden)}")
                        paden = paden[:too_long]

            bisect.insort(paden, nieuw_pad)

    return max_afstand


if __name__ == "__main__":
    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/ijsjes/wedstrijd.invoer") as f:
        lines = f.readlines()

    output_lines = []

    num_opgaves = int(lines[0])
    opgaves = []
    line_idx = 1
    lines_out = []
    for i in range(num_opgaves):
        aantal_straten, aantal_kruispunten = lines[line_idx].strip().split()
        aantal_straten = int(aantal_straten)
        aantal_kruispunten = int(aantal_kruispunten)
        straten = []
        line_idx += 1
        for j in range(aantal_straten):
            a, b, lengte, nodig = lines[line_idx + j].strip().split()
            a = int(a)
            b = int(b)
            lengte = int(lengte)
            if nodig == "1":
                nodig = True
            elif nodig == "0":
                nodig = False
            else:
                ValueError("Should not happen")
            straat = Straat(kruispunt_a=a - 1, kruispunt_b=b - 1, lengte=lengte, nodig=nodig)  # zero-based indexing
            straten.append(straat)

        line_idx += aantal_straten
        depot = int(lines[line_idx].strip()) - 1  # Zero-based indexing
        print(f"{straten=},{depot=},{aantal_kruispunten=})")
        resultaat = vind_kortste_pad(straten, depot, aantal_kruispunten)
        print(resultaat)
        lines_out.append(f"{i + 1} {resultaat}\n")
        line_idx += 1

    with open("/workspaces/nn_toolbox/temp/opgaves/2022/cat4/ijsjes/wedstrijd2.uitvoer", "w") as f:
        f.writelines(lines_out)
