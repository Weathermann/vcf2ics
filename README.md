# vcf2ics
Python project to convert vcf contacts to an ics calendar file, which contains the **birthdays** of the contacts

Purpose of the application:
**Display birthdays in the Android calendar _without the need to use the Google Calendar_.**  
For this purpose it reads the `BDAY` tag from a vcf contacts file, writes the birthdays together with the calculated age into an ics calendar file.

This project was inspired by https://github.com/FoxP/VCF-to-ICS  
In comparison, the code has been modernized and simplified for the intended limited purpose.


## What you need
Contacts in VCF format with birthday data included (`BDAY` tag). All entries that have this tag will be processed, all others will be ignored.

```ini
BEGIN:VCARD
VERSION:3.0
BDAY:1993-06-28
FN:Weather Mann
N:Mann;Weather;;;
UID:3cf6bd87-dab0-4275-8790-4eaa205e1cad
END:VCARD
```

## My environment

### VCF file
The VCF file format comes from the KDE/Plasma *KAddressBook*, which can be integrated into *KOrganizer* as a birthday calendar.

### Phone

Samsung Phone with Android 13

On Android smartphones (perhaps others too?) this option is missing - it is not possible to import a VCF file into the calendar app **without using the Google calendar**.

It is, however, possible to integrate any CalDAV calendar using additional software such as [DAVx](https://www.davx5.com/). With the help of this Python script, you can create your own birthday calendar in ICS format, which can be loaded into CalDAV (e.g. mail.de) to then integrate it into the Android calendar.


### Workflow
**VCF -> this Script -> ICS (with calendar name) -> CalDAV -> smartphone calendar**

In the Android calendar, an entry is then displayed as follows:  
`Weather Mann 44`

## Usage

```python
#                     <input file>    <output cal file>  <cal name>
python3 vcf_to_ics.py -i contacts.vcf -o birthdays.ics -n birthdays
```

## Disadvantages
You need to renew the .ics file every year to get the correct pre-calculated age in the contact name, but this is not a big problem.
