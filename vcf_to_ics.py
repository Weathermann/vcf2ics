#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path
from string import ascii_letters
from string import digits
import argparse
import random
import time
import sys
from datetime import datetime
from typing import List

# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# CONFIGURATION

PROGRAM_NAME = "VCF to ICS"
PROGRAM_VERSION = "1.0"


@dataclass
class VCF2ICS:
    vcf_file: Path

    def process(self) -> list[str] | None:
        # Read VCF file content
        file_content = self.vcf_file.read_text(encoding="utf-8")
        # Separate VCards
        all_cards = file_content.split("END:VCARD")
        print(f"{len(all_cards)} VCards found")
        if not all_cards:
            return None

        list_formatted_entries = []
        for card in all_cards:
            dict_card = self._get_dict(card)
            if not dict_card:
                continue
            entry = self._parse_vcard_get_formatted_entry(dict_card)
            list_formatted_entries.append(entry)
        # for
        print(f"\n{len(list_formatted_entries)} usable entries")
        return list_formatted_entries

    def _get_dict(self, card: str) -> dict[str] | None:
        _dict = {}
        for line in card.split("\n"):
            elems = line.split(":")
            key = elems[0]
            if key in ("BDAY", "N", "FN", "UID"):
                _dict[key] = "".join(elems[1:])
        try:
            bday = _dict["BDAY"]
        except KeyError:
            return None  # not usable

        _dict["BDAY"] = bday.split("T")[0]  # '2000-07-01T000000'

        try:
            _dict["FN"]  # -> usable
        except KeyError:
            try:
                name = _dict["N"]
                elems = name.split(";")
                if elems[3]:
                    new_name = f"{elems[3]} {elems[1]} {elems[0]}"
                else:
                    new_name = f"{elems[1]} {elems[0]}"
                _dict["FN"] = new_name
            except KeyError:  # no information
                _dict = None
            else:
                del _dict["N"]

        return _dict

    def _parse_vcard_get_formatted_entry(self, vcard: dict[str]) -> str:
        # BDAY format:
        # BDAY:2000-07-01T00:00:00
        # or   2000-07-01
        bday = vcard["BDAY"]
        year, month, day = bday.split("-")
        dt_birth_start = datetime(int(year), int(month), int(day))
        dt_birth_end = datetime(int(time.strftime("%Y")), int(month), int(day))  # current year!
        name = vcard["FN"]

        dt_diff = dt_birth_end - dt_birth_start
        days = dt_diff.days + 1  # ein Tag zuwenig
        years = int(days / 365)
        # print(f"{name}: {dt_birth_start} {dt_birth_end} {years}")
        print(f"{name}: {years}")

        birth_start_str = dt_birth_start.strftime("%Y%m%d")
        try:
            uid = vcard["UID"]
        except KeyError:  # not a problem, can be generated later
            uid = self._generate_uid(birth_start_str)

        list_block = [f"BEGIN:VEVENT", f"DTSTART:{birth_start_str}", f"SUMMARY:{name} ({years})",
                      "RRULE:FREQ=YEARLY", "DURATION:P1D", f"UID:{uid}", "END:VEVENT"]
        entry = "\n".join(list_block)
        return entry

    def _generate_uid(self, birth_start_str: str):
        """Unique ID
        The UID purpose is to define a unique identifier across all the calendar components.
        It is basically a random generated sequence that will assure the uniqueness of every
        calendar component. This property is mandatory in defining calendar components.
        Everyone must assure that this unique identifier is added at the Creation Time
        of his calendar component, to be sure of the uniqueness of all the components.

        Consequences of not doing it right
        Because the UID globally identifies a calendar component, not having a good way of
        generating this property can cause a lot of problems. Using a simple UID generation
        algorithm might lead to overridden events with the same UID generated by others
        using the same generation mechanism. Every creation of a calendar component with
        a UID that is already contained by other component will lead in the end to the update
        of the older component. Once generated, the calendar component should keep the same
        UID all the time, so that no matter which part of the event is changed, the UID-Reference
        is the same and the calendar can be updated until that event will be deleted. """
        uid = ''.join([random.choice(list(ascii_letters + digits)) for _ in range(16)]) + "@VCFtoICS.com"
        return f"{birth_start_str}-{uid}"

    def write_ics_file(self, ics_file: Path, calendar_name: str, list_formatted_entries: list[str]):
        with ics_file.open("w") as f:
            # Write ICS calendar header
            f.write(f"BEGIN:VCALENDAR\nPRODID:-//{PROGRAM_NAME}//NONSGML {calendar_name} V1.0//EN\n"
                    f"X-WR-CALNAME:{calendar_name}\nVERSION:2.0\n")
            for entry in list_formatted_entries:
                f.write(f"{entry}\n")
            # Write ICS calendar footer
            f.write("END:VCALENDAR\n")
            print("\n->", ics_file)


if __name__ == "__main__":
    # Command-line interface
    argParser = argparse.ArgumentParser(description=f"{PROGRAM_NAME} {PROGRAM_VERSION}")
    argParser.add_argument('-i', '--input', metavar='PATH', help='Input .vcf file path', required=True)
    argParser.add_argument('-o', '--output', metavar='PATH', help='Output .ics file path', required=True)
    argParser.add_argument('-n', '--name', metavar='NAME', help='Desired calendar name', required=True)
    args = vars(argParser.parse_args())

    vcf_file = Path(args["input"])
    ics_file = Path(args["output"])
    calendar_name = args["name"]

    if not vcf_file.exists():
        print("Invalid input file path:", vcf_file)
        sys.exit(1)

    vcf2ics = VCF2ICS(vcf_file)
    list_formatted_entries = vcf2ics.process()

    if not list_formatted_entries:
        sys.exit(1)

    # Write ICS event:
    vcf2ics.write_ics_file(ics_file, calendar_name, list_formatted_entries)
