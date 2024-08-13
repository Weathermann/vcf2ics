from vcf_to_ics import create_vcard, Vcard

card_ok = """BEGIN:VCARD
VERSION:3.0
BDAY:1993-06-28
FN:Weather Mann
N:Mann;Weather;;;
UID:3cf6bd87-dab0-4275-8790-4eaa205e1cad
END:VCARD
"""

card_without_bday = """BEGIN:VCARD
VERSION:3.0
FN:Weather Mann
N:Mann;Weather;;;
UID:3cf6bd87-dab0-4275-8790-4eaa205e1cad
END:VCARD
"""

card_name_with_dr = """BEGIN:VCARD
VERSION:3.0
BDAY:1959-06-16T00:00:00
FN:Max Muster
N:Muster;Max;;Dr.;
UID:pas-id-4B5EFF8D0000005C
END:VCARD
"""


def test_should_create_vcard():
    vcard = create_vcard(card_ok)
    assert vcard.name == "Weather Mann"
    assert vcard.uid == "3cf6bd87-dab0-4275-8790-4eaa205e1cad"


def test_should_not_create_vcard():
    """without BDAY cannot create vcard"""
    vcard = create_vcard(card_without_bday)
    assert vcard is None


def test_without_uid():
    lines = card_ok.split("\n")
    lines_without_uid = [line for line in lines if not line.startswith("UID")]
    new_vcard_input = "\n".join(lines_without_uid)
    vcard = create_vcard(new_vcard_input)
    # print("###", vcard.uid)
    assert vcard.uid.startswith("19930628")


def test_name_with_doctorate():
    vcard = create_vcard(card_name_with_dr)
    assert vcard.name == "Dr. Max Muster"
